#!/usr/bin/env python3
import sys
import re

# Allowed commit types
VALID_TYPES = {"feat", "fix", "docs", "style", "refactor", "test", "chore", "ci", "perf", "revert"}

def main():
    if len(sys.argv) < 2:
        print("Error: Commit message file path argument is missing.", file=sys.stderr)
        sys.exit(1)
        
    commit_msg_filepath = sys.argv[1]
    
    try:
        with open(commit_msg_filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except IOError:
        print(f"Error: Could not read commit message file: {commit_msg_filepath}", file=sys.stderr)
        sys.exit(1)
        
    if not lines:
        print("Error: Empty commit message.", file=sys.stderr)
        sys.exit(1)
        
    # Get the first line (commit subject)
    subject = lines[0].strip()
    
    # Allow automated Git merge/revert messages
    if subject.startswith("Merge ") or subject.startswith("Revert "):
        sys.exit(0)
        
    # Pattern to match Conventional Commits: type(scope)?: message
    # e.g., feat(auth): add login endpoint
    pattern = r"^([a-z]+)(?:\([a-zA-Z0-9_/-]+\))?:\s+(.+)$"
    match = re.match(pattern, subject)
    
    if not match:
        print("="*60, file=sys.stderr)
        print("❌ [INVALID COMMIT MESSAGE FORMAT]", file=sys.stderr)
        print("="*60, file=sys.stderr)
        print("올바른 커밋 메시지 형식을 지켜주세요.", file=sys.stderr)
        print("형식: <type>(<scope>): <subject>", file=sys.stderr)
        print("예시: feat(auth): 사용자 로그인 API 추가", file=sys.stderr)
        print("예시: fix(ui): 버튼 정렬 버그 수정", file=sys.stderr)
        print("\n사용 가능한 <type> 목록:", file=sys.stderr)
        print(f"  {', '.join(sorted(list(VALID_TYPES)))}", file=sys.stderr)
        print("="*60, file=sys.stderr)
        sys.exit(1)
        
    commit_type = match.group(1)
    if commit_type not in VALID_TYPES:
        print("="*60, file=sys.stderr)
        print(f"❌ [INVALID COMMIT TYPE: '{commit_type}']", file=sys.stderr)
        print("="*60, file=sys.stderr)
        print(f"허용되지 않은 커밋 타입입니다.", file=sys.stderr)
        print("사용 가능한 <type> 목록:", file=sys.stderr)
        print(f"  {', '.join(sorted(list(VALID_TYPES)))}", file=sys.stderr)
        print("="*60, file=sys.stderr)
        sys.exit(1)
        
    sys.exit(0)

if __name__ == "__main__":
    main()
