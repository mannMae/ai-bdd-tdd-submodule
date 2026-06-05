#!/usr/bin/env python3
import os
import sys
import subprocess
import re

def run_command(args, cwd=None):
    """Runs a shell command and returns output, errors, and return code."""
    try:
        result = subprocess.run(args, capture_output=True, text=True, cwd=cwd, shell=True)
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return "", str(e), 1

def run_self_heal_python(project_root):
    """Runs ruff linter & formatter auto-fix and gets remaining errors."""
    print("Running Python Linter (Ruff) Auto-Fix...")
    # 1. Try to fix common issues
    run_command("ruff check --fix .", cwd=project_root)
    run_command("ruff format .", cwd=project_root)
    
    # 2. Get remaining errors
    stdout, stderr, code = run_command("ruff check .", cwd=project_root)
    
    errors = []
    if code != 0:
        # Parse ruff output
        # Format: path/to/file.py:line:col: RULE_ID Message
        lines = stdout.strip().split('\n')
        for line in lines:
            match = re.match(r"^([^:]+):(\d+):(\d+):\s+(\w+)\s+(.+)$", line.strip())
            if match:
                errors.append({
                    "file": match.group(1),
                    "line": match.group(2),
                    "rule": match.group(4),
                    "message": match.group(5)
                })
    return errors

def run_self_heal_js(project_root):
    """Runs ESLint / Prettier auto-fix and gets remaining errors."""
    print("Running JS/TS Linter (ESLint) Auto-Fix...")
    # 1. Try to fix issues
    run_command("npm run lint -- --fix", cwd=project_root)
    
    # 2. Get remaining errors
    stdout, stderr, code = run_command("npm run lint", cwd=project_root)
    
    errors = []
    if code != 0:
        # Parse typical ESLint output
        # Match lines like:   path/to/file.tsx: line 12, col 5, Error - Message (rule-id)
        # Or parse simple lines containing line/col
        lines = stdout.strip().split('\n')
        current_file = None
        for line in lines:
            line_str = line.strip()
            # If it's a file header path
            if line_str.startswith("/") or line_str.endswith(".tsx") or line_str.endswith(".ts"):
                current_file = line_str
                continue
                
            match = re.search(r"(\d+):(\d+)\s+(error|warning)\s+(.+?)\s+([a-zA-Z0-9_\-\/]+)$", line_str)
            if match and current_file:
                errors.append({
                    "file": current_file,
                    "line": match.group(1),
                    "rule": match.group(5),
                    "message": match.group(4)
                })
    return errors

def main():
    project_root = os.getcwd()
    
    py_errors = run_self_heal_python(project_root)
    js_errors = run_self_heal_js(project_root)
    
    all_errors = py_errors + js_errors
    
    report_path = os.path.join(project_root, "SELF_HEAL_REPORT.md")
    
    if not all_errors:
        print("All code successfully formatted and linted (0 errors). Code is clean!")
        if os.path.exists(report_path):
            os.remove(report_path)
        sys.exit(0)
        
    # Build clean markdown report for the AI agent
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# 🚨 Lint & Style Errors Remaining (Self-Heal Report)\n\n")
        f.write("공통 아키텍처 및 코딩 컨벤션에 부합하지 않는 아래 오류들이 발견되었습니다.\n")
        f.write("AI 에이전트는 즉시 아래 파일과 해당 라인의 오류 내용을 분석하고 자가 수정하십시오.\n\n")
        
        # Group by file
        grouped = {}
        for err in all_errors:
            grouped.setdefault(err["file"], []).append(err)
            
        for file, errs in grouped.items():
            f.write(f"### 📄 `{file}`\n")
            for e in errs:
                f.write(f"- **Line {e['line']}**: `{e['rule']}` - {e['message']}\n")
            f.write("\n")
            
    print(f"\n========================================================")
    print(f"❌ Lint check failed. Remaining errors compiled to:")
    print(f"   {report_path}")
    print(f"========================================================")
    sys.exit(1)

if __name__ == "__main__":
    main()
