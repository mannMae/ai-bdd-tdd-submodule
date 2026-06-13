#!/usr/bin/env python3
import os
import sys
import subprocess
import re

def get_git_status():
    """Runs git status to find added, modified, and deleted files."""
    try:
        # Get status of staged changes
        staged_out = subprocess.check_output(["git", "diff", "--cached", "--name-status"], text=True)
        # Get status of unstaged changes
        unstaged_out = subprocess.check_output(["git", "diff", "--name-status"], text=True)
        
        files = {"staged": [], "unstaged": []}
        
        for line in staged_out.strip().split('\n'):
            if line:
                parts = line.split('\t')
                if len(parts) >= 2:
                    files["staged"].append((parts[0], parts[1]))
                    
        for line in unstaged_out.strip().split('\n'):
            if line:
                parts = line.split('\t')
                if len(parts) >= 2:
                    files["unstaged"].append((parts[0], parts[1]))
                    
        return files
    except Exception as e:
        print(f"Warning: Could not check Git status: {e}", file=sys.stderr)
        return {"staged": [], "unstaged": []}

def get_rtm_checklist(project_root):
    """Collects requirements and checklist items from RTM files."""
    checklist = []
    req_dir = os.path.join(project_root, "docs", "requirements")
    if os.path.exists(req_dir):
        for file in os.listdir(req_dir):
            if (file.startswith("rtm_") or file.startswith("technical_rtm_")) and file.endswith(".md"):
                path = os.path.join(req_dir, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Match checkboxes under ## 2. 🛡️ 엔지니어링 룰 자가 채점표
                    lines = content.split('\n')
                    in_grading = False
                    for line in lines:
                        if line.startswith("## 2. "):
                            in_grading = True
                            continue
                        elif line.startswith("## ") and in_grading:
                            in_grading = False
                            
                        if in_grading:
                            # Match checklist items: * [x] or * [ ]
                            match = re.search(r"\*\s+\[(x|\s)\]\s+\*\*([^\*]+)\*\*", line)
                            if match:
                                checked = (match.group(1).lower() == 'x')
                                item_text = match.group(2).strip()
                                checklist.append({
                                    "file": file,
                                    "item": item_text,
                                    "passed": checked
                                })
                except Exception:
                    continue
    return checklist

def main():
    project_root = os.getcwd()
    print("Preparing commit & PR description metadata...")
    
    git_files = get_git_status()
    rtm_items = get_rtm_checklist(project_root)
    
    staged_list = git_files["staged"]
    unstaged_list = git_files["unstaged"]
    
    # 1. Deduce conventional commit scope and type
    commit_type = "feat"
    scope = "core"
    
    # Analyze files to guess type and scope
    all_files = [path for _, path in staged_list] + [path for _, path in unstaged_list]
    if all(path.endswith((".test.tsx", ".test.ts", "_test.py")) or "tests/" in path for path in all_files):
        commit_type = "test"
    elif all("docs/" in path or path.endswith(".md") for path in all_files):
        commit_type = "docs"
    elif all("configs/" in path or path.startswith(".") for path in all_files):
        commit_type = "chore"
        
    for path in all_files:
        if "frontend" in path:
            scope = "frontend"
            break
        elif "backend" in path:
            scope = "backend"
            break
            
    suggested_commit = f"{commit_type}({scope}): [여기에 작업 내용을 기입하세요]"
    
    # 2. Build PR_DESCRIPTION.md
    pr_path = os.path.join(project_root, "PR_DESCRIPTION.md")
    
    with open(pr_path, 'w', encoding='utf-8') as f:
        f.write("# 🚀 Pull Request Description\n\n")
        f.write("## 📝 작업 내용 요약 (Summary)\n")
        f.write("- \n")
        f.write("- \n\n")
        
        f.write("## 🛠️ 변경 파일 목록 (Modified Files)\n")
        if staged_list:
            f.write("### Staged for commit:\n")
            for status, path in staged_list:
                f.write(f"- `{status}` `{path}`\n")
        if unstaged_list:
            f.write("### Unstaged changes:\n")
            for status, path in unstaged_list:
                f.write(f"- `{status}` `{path}`\n")
        if not staged_list and not unstaged_list:
            f.write("변경사항이 감지되지 않았습니다.\n")
        f.write("\n")
        
        f.write("## 📊 RTM 요구사항 및 자가 채점 현황 (RTM Self-Grading)\n")
        if rtm_items:
            f.write("| 채점 항목 | 통과 여부 | 연관 문서 |\n")
            f.write("| :--- | :--- | :--- |\n")
            for item in rtm_items:
                status_icon = "✅ Pass" if item["passed"] else "⏳ Pending"
                f.write(f"| {item['item']} | {status_icon} | `{item['file']}` |\n")
        else:
            f.write("체크리스트 정보가 없습니다.\n")
        f.write("\n")
        
        f.write("## 💡 권장 커밋 메시지 (Suggested Commit Message)\n")
        f.write(f"```text\n{suggested_commit}\n```\n")
        
    print(f"\nMetadata collected. suggested commit message:\n  {suggested_commit}")
    print(f"PR draft generated at: {pr_path}")

if __name__ == "__main__":
    main()
