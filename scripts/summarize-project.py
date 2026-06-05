#!/usr/bin/env python3
import os
import sys
import re

IGNORE_DIRS = {'.git', 'node_modules', 'venv', '.agents', '.agents-local', 'dist', '__pycache__'}

def scan_backend_apis(root_dir):
    """Scans python backend code for FastAPI router endpoints."""
    endpoints = []
    
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                rel_path = os.path.relpath(path, root_dir)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                except Exception:
                    continue
                    
                for i, line in enumerate(lines):
                    # Match @router.get("/path"), @router.post(...)
                    route_match = re.search(r"@router\.(get|post|put|delete|patch)\(\s*[\"']([^\"']+)[\"']", line)
                    if route_match:
                        method = route_match.group(1).upper()
                        route_path = route_match.group(2)
                        
                        # Find the function definition immediately following the decorator
                        func_def = "unknown_function"
                        for j in range(i+1, min(i+5, len(lines))):
                            func_match = re.search(r"async\s+def\s+(\w+)\(|def\s+(\w+)\(", lines[j])
                            if func_match:
                                func_def = func_match.group(1) or func_match.group(2)
                                break
                        endpoints.append({
                            "file": rel_path,
                            "method": method,
                            "path": route_path,
                            "handler": func_def
                        })
    return endpoints

def scan_frontend_components(root_dir):
    """Scans frontend directories to catalog pages and features."""
    components = []
    
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for file in files:
            if file.endswith((".tsx", ".ts", ".jsx", ".js")):
                path = os.path.join(root, file)
                rel_path = os.path.relpath(path, root_dir)
                
                # Deduce if it's a Page or Component
                category = "Component"
                if "routes" in rel_path or "pages" in rel_path:
                    category = "Page"
                elif "features" in rel_path:
                    category = "Feature Component"
                elif "components/ui" in rel_path:
                    category = "UI Primitive"
                    
                components.append({
                    "file": rel_path,
                    "category": category
                })
    return components

def scan_rtm_requirements(project_root):
    """Summarizes requirements and status from RTM documents."""
    requirements = []
    req_dir = os.path.join(project_root, "docs", "requirements")
    if os.path.exists(req_dir):
        for file in os.listdir(req_dir):
            if file.startswith("rtm_") and file.endswith(".md"):
                path = os.path.join(req_dir, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    status_match = re.search(r"\*\s+\*\*상태 \(Status\)\*\*:\s*`?([^`\n]+)`?", content)
                    status = status_match.group(1) if status_match else "WIP"
                    title = "Unknown Requirement"
                    for line in content.split('\n'):
                        if line.startswith("# "):
                            title = line.replace("# ", "").strip()
                            break
                    requirements.append({
                        "file": os.path.join("docs", "requirements", file),
                        "title": title,
                        "status": status
                    })
                except Exception:
                    continue
    return requirements

def main():
    project_root = os.getcwd()
    print(f"Building project context summary for: {project_root}")
    
    # Locate apps/backend and apps/frontend
    backend_root = project_root
    frontend_root = project_root
    
    for folder in ["apps/backend", "backend", "src/backend"]:
        test_path = os.path.join(project_root, folder)
        if os.path.exists(test_path):
            backend_root = test_path
            break
            
    for folder in ["apps/frontend", "frontend", "src/frontend"]:
        test_path = os.path.join(project_root, folder)
        if os.path.exists(test_path):
            frontend_root = test_path
            break
            
    endpoints = scan_backend_apis(backend_root)
    components = scan_frontend_components(frontend_root)
    rtms = scan_rtm_requirements(project_root)
    
    output_path = os.path.join(project_root, "PROJECT_CONTEXT.md")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# 🧭 Project Context Summary (PROJECT_CONTEXT.md)\n\n")
        f.write("이 요약은 AI 에이전트가 코드를 탐색할 때 읽기 전용 가벼운 명세서(Lightweight Specification)로 활용하여 토큰을 절약하기 위해 자동으로 갱신됩니다.\n\n")
        
        # 1. RTM Requirements
        f.write("## 1. 📊 연관 요구사항 및 상태 (RTM Status)\n\n")
        if rtms:
            f.write("| 요구사항 (RTM) | 상태 |\n")
            f.write("| :--- | :--- |\n")
            for r in rtms:
                f.write(f"| [{r['title']}]({r['file']}) | `{r['status']}` |\n")
        else:
            f.write("등록된 RTM 기술 매핑 문서가 없습니다.\n")
        f.write("\n---\n\n")
        
        # 2. Backend APIs
        f.write("## 2. 🔌 백엔드 API 명세 (Backend Endpoints)\n\n")
        if endpoints:
            f.write("| Method | Path | Handler | File Location |\n")
            f.write("| :--- | :--- | :--- | :--- |\n")
            for ep in endpoints:
                f.write(f"| `{ep['method']}` | `{ep['path']}` | `{ep['handler']}` | `{ep['file']}` |\n")
        else:
            f.write("감지된 백엔드 API 엔드포인트가 없습니다.\n")
        f.write("\n---\n\n")
        
        # 3. Frontend Components
        f.write("## 3. 🖥️ 프론트엔드 컴포넌트 목록 (Frontend Catalog)\n\n")
        if components:
            f.write("| 분류 | 파일 경로 |\n")
            f.write("| :--- | :--- |\n")
            # Sort by category to group them nicely
            for category in ["Page", "Feature Component", "UI Primitive", "Component"]:
                cat_items = [c for c in components if c["category"] == category]
                # Limit output to 30 files per category to keep token usage small
                for c in cat_items[:30]:
                    f.write(f"| {c['category']} | `{c['file']}` |\n")
                if len(cat_items) > 30:
                    f.write(f"| {category} | ... 외 {len(cat_items)-30}개 파일 추가 감지됨 |\n")
        else:
            f.write("감지된 프론트엔드 파일이 없습니다.\n")
            
    print(f"Context summary written successfully to: {output_path}")

if __name__ == "__main__":
    main()
