#!/usr/bin/env python3
import os
import sys
import re
import subprocess
from datetime import datetime

# Define Colors for terminal output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
BOLD = "\033[1m"
RESET = "\033[0m"

def get_git_status():
    """Returns a list of uncommitted files and their status."""
    try:
        res = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=True)
        lines = res.stdout.strip().split("\n")
        if not lines or lines == [""]:
            return []
        return [line.strip() for line in lines]
    except Exception:
        return []

def get_git_branch():
    """Returns the current git branch name."""
    try:
        res = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True, check=True)
        return res.stdout.strip()
    except Exception:
        return "unknown"

def parse_rtm_files(project_root):
    """Parses RTM files in docs/requirements/ and returns their status."""
    requirements_dir = os.path.join(project_root, "docs", "requirements")
    if not os.path.exists(requirements_dir):
        return []
    
    rtm_files = [f for f in os.listdir(requirements_dir) if (f.startswith("rtm_") or f.startswith("technical_rtm_")) and f.endswith(".md")]
    rtms = []
    
    for f_name in rtm_files:
        path = os.path.join(requirements_dir, f_name)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Parse Status
        status_match = re.search(r"\*\s+\*\*상태 \(Status\)\*\*:\s*`?([^`\n\r]+)`?", content)
        status = status_match.group(1).strip() if status_match else "Pending"
        
        # Parse Checklist Progress
        # Matches: [x] or [ ]
        checkboxes = re.findall(r"(?:-|\*)\s+\[([ xX/])\]", content)
        total_checks = len(checkboxes)
        completed_checks = sum(1 for c in checkboxes if c.lower() == 'x')
        in_progress_checks = sum(1 for c in checkboxes if c == '/')
        
        # Parse Evidence Files
        file_pattern = r"\[([^\]]+)\]\(file:///([^\)]+)\)"
        evidence_matches = re.findall(file_pattern, content)
        existing_evidence = 0
        total_evidence = len(evidence_matches)
        
        for label, rel_path in evidence_matches:
            clean_path = rel_path.split('#')[0]
            if os.path.isabs(clean_path):
                abs_path = clean_path
            else:
                abs_path = os.path.join(project_root, clean_path)
            if os.path.exists(abs_path):
                existing_evidence += 1
                
        rtms.append({
            "name": f_name,
            "status": status,
            "total_checks": total_checks,
            "completed_checks": completed_checks,
            "in_progress_checks": in_progress_checks,
            "total_evidence": total_evidence,
            "existing_evidence": existing_evidence
        })
    return rtms

def parse_task_md(project_root):
    """Parses task.md in the root directory and returns progress."""
    task_path = os.path.join(project_root, "task.md")
    if not os.path.exists(task_path):
        return None
    
    with open(task_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    tasks = []
    current_section = "General"
    
    for line in lines:
        line_str = line.strip()
        if line_str.startswith("#"):
            current_section = line_str.lstrip("#").strip()
        elif line_str.startswith("- ["):
            match = re.match(r"^-\s+\[([ xX/])\]\s+(.+)$", line_str)
            if match:
                status_char = match.group(1)
                desc = match.group(2)
                status = "todo"
                if status_char.lower() == 'x':
                    status = "done"
                elif status_char == '/':
                    status = "wip"
                tasks.append({"section": current_section, "desc": desc, "status": status})
                
    return tasks

def make_progress_bar(completed, total, width=20):
    if total == 0:
        return "[" + "░" * width + "] 0%"
    percent = int((completed / total) * 100)
    filled_width = int((completed / total) * width)
    bar = "█" * filled_width + "░" * (width - filled_width)
    return f"[{bar}] {percent}%"

def generate_markdown_dashboard(project_root, rtms, tasks, git_status, branch):
    """Generates docs/BDD_DASHBOARD.md file for IDE live preview."""
    docs_dir = os.path.join(project_root, "docs")
    os.makedirs(docs_dir, exist_ok=True)
    dashboard_path = os.path.join(docs_dir, "BDD_DASHBOARD.md")
    
    # Calculate global progress
    total_rtm_checks = sum(r["total_checks"] for r in rtms)
    completed_rtm_checks = sum(r["completed_checks"] for r in rtms)
    rtm_progress_bar = make_progress_bar(completed_rtm_checks, total_rtm_checks, 25)
    
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    md_content = f"""# 📊 BDD & TDD Development Progress Dashboard
*마지막 갱신 시간: {now_str}*

---

## 📈 전체 진원도 (RTM Progress)
**요구사항 자가 검정률**: `{completed_rtm_checks}/{total_rtm_checks} 체크 완료`
> `{rtm_progress_bar}`

---

## 🔨 현재 활성 작업 (Active Tasks from task.md)
"""
    if not tasks:
        md_content += "_`task.md` 파일이 프로젝트 루트에 존재하지 않거나 태스크가 정의되지 않았습니다._\n"
    else:
        for t in tasks:
            status_icon = "⬜"
            if t["status"] == "done":
                status_icon = "✅"
            elif t["status"] == "wip":
                status_icon = "⏳"
            md_content += f"- {status_icon} **[{t['section']}]** {t['desc']}\n"
            
    md_content += """
---

## 📋 요구사항 추적성 매핑 (RTM Traceability Matrix)
| RTM 요구사항 명세서 | 상태 | 자가 채점 진행률 | 검증 파일 존재 여부 |
| :--- | :--- | :--- | :--- |
"""
    if not rtms:
        md_content += "| _등록된 RTM 문서 없음_ | - | - | - |\n"
    else:
        for r in rtms:
            status_badge = f"`{r['status']}`"
            if r["status"] == "완료":
                status_badge = "🟢 `완료`"
            elif r["status"] == "WIP":
                status_badge = "🟡 `WIP`"
            
            checks_str = f"{r['completed_checks']}/{r['total_checks']} ({int((r['completed_checks']/r['total_checks'])*100) if r['total_checks'] > 0 else 0}%)"
            evidence_str = f"📁 {r['existing_evidence']}/{r['total_evidence']} 파일 검증"
            if r["existing_evidence"] == r["total_evidence"] and r["total_evidence"] > 0:
                evidence_str = "✅ " + evidence_str
            else:
                evidence_str = "⚠️ " + evidence_str
                
            md_content += f"| [{r['name']}](file:///{os.path.join(project_root, 'docs', 'requirements', r['name'])}) | {status_badge} | {checks_str} | {evidence_str} |\n"
            
    md_content += f"""
---

## 🌿 Git 개발 환경 현황
*   **현재 브랜치**: `{branch}`
*   **미커밋 변경 파일 (git status)**:
"""
    if not git_status:
        md_content += "✅ *작업 디렉토리가 깨끗합니다. (No uncommitted changes)*\n"
    else:
        for line in git_status:
            md_content += f"- `{line}`\n"
            
    md_content += """
---
*본 대시보드는 `.agents/scripts/bdd-dashboard.py` 스크립트를 통해 실시간 또는 빌드 시점에 자동 갱신됩니다.*
"""
    
    with open(dashboard_path, "w", encoding="utf-8") as f:
        f.write(md_content)

def print_cli_dashboard(rtms, tasks, git_status, branch):
    """Prints a beautiful colored dashboard directly to terminal."""
    print(f"\n{BOLD}{BLUE}===================================================================={RESET}")
    print(f"       📊  {BOLD}{BLUE}BDD & TDD DEVELOPMENT PROGRESS DASHBOARD{RESET}")
    print(f"{BOLD}{BLUE}===================================================================={RESET}")
    
    # RTM Summary
    total_rtm_checks = sum(r["total_checks"] for r in rtms)
    completed_rtm_checks = sum(r["completed_checks"] for r in rtms)
    progress_bar = make_progress_bar(completed_rtm_checks, total_rtm_checks, 30)
    
    print(f"\n{BOLD}▶ RTM Requirements Self-Grading Status{RESET}")
    print(f"  Progress:  {progress_bar}")
    print(f"  Checked:   {completed_rtm_checks}/{total_rtm_checks} steps completed\n")
    
    print(f"  {BOLD}{'RTM Specification Document':<40} {'Status':<10} {'Evidence':<10}{RESET}")
    print("  " + "-" * 64)
    for r in rtms:
        status_color = YELLOW if r["status"] == "WIP" else (GREEN if r["status"] == "완료" else RESET)
        status_str = f"{status_color}{r['status']:<10}{RESET}"
        
        evidence_color = GREEN if r["existing_evidence"] == r["total_evidence"] and r["total_evidence"] > 0 else RED
        evidence_str = f"{evidence_color}{r['existing_evidence']}/{r['total_evidence']} files{RESET}"
        
        print(f"  {r['name']:<40} {status_str:<18} {evidence_str}")
        
    # Task list summary
    print(f"\n{BOLD}▶ Current Active Tasks (task.md){RESET}")
    print("  " + "-" * 64)
    if not tasks:
        print("  No tasks parsed from task.md or file is missing.")
    else:
        for t in tasks:
            status_symbol = f"{GREEN}[x]{RESET}" if t["status"] == "done" else (f"{YELLOW}[/]{RESET}" if t["status"] == "wip" else "[ ]")
            print(f"  {status_symbol} {BOLD}[{t['section']}]{RESET} {t['desc']}")
            
    # Git status summary
    print(f"\n{BOLD}▶ Git Branch & Working Status{RESET}")
    print("  " + "-" * 64)
    print(f"  Current Branch: {BOLD}{branch}{RESET}")
    if not git_status:
        print(f"  Status:         {GREEN}Clean working directory{RESET}")
    else:
        print(f"  Status:         {YELLOW}Uncommitted changes ({len(git_status)} files){RESET}")
        for line in git_status[:5]:
            print(f"    {line}")
        if len(git_status) > 5:
            print(f"    ... and {len(git_status) - 5} more files.")
            
    print(f"{BOLD}{BLUE}===================================================================={RESET}\n")

def main():
    project_root = os.getcwd()
    
    rtms = parse_rtm_files(project_root)
    tasks = parse_task_md(project_root)
    git_status = get_git_status()
    branch = get_git_branch()
    
    # 1. Output terminal representation
    print_cli_dashboard(rtms, tasks, git_status, branch)
    
    # 2. Output markdown representation in docs/BDD_DASHBOARD.md
    generate_markdown_dashboard(project_root, rtms, tasks, git_status, branch)
    print(f"Dashboard markdown file successfully updated at: docs/BDD_DASHBOARD.md")

if __name__ == "__main__":
    main()
