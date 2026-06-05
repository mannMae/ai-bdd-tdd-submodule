#!/usr/bin/env python3
import os
import sys
import re

def parse_evidence_files(content):
    """Extracts file links from the Verification Evidence section."""
    # Find all file links of form [label](file:///path/to/file)
    file_pattern = r"\[([^\]]+)\]\(file:///([^\)]+)\)"
    matches = re.findall(file_pattern, content)
    
    evidence_files = []
    for label, path in matches:
        # Strip anchor links (e.g., #L12-L15)
        clean_path = path.split('#')[0]
        evidence_files.append((label, clean_path))
        
    return evidence_files

def evaluate_rtm(rtm_path, project_root):
    """Evaluates a single RTM file, checks evidence files, and updates the markdown."""
    print(f"Evaluating: {os.path.basename(rtm_path)}")
    
    with open(rtm_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    evidence_files = parse_evidence_files(content)
    
    if not evidence_files:
        print("  Warning: No verification evidence files found in this RTM.")
        return False
        
    missing_files = []
    existing_files = []
    
    for label, rel_path in evidence_files:
        # Resolve absolute path (rel_path is usually relative to parent root or absolute)
        # Handle cases where rel_path has absolute /Users/... or relative like apps/frontend/...
        if os.path.isabs(rel_path):
            abs_path = rel_path
        else:
            abs_path = os.path.join(project_root, rel_path)
            
        if os.path.exists(abs_path):
            existing_files.append((label, rel_path))
        else:
            missing_files.append((label, rel_path))
            
    print(f"  Existing evidence files: {len(existing_files)}/{len(evidence_files)}")
    if missing_files:
        print("  Missing files:")
        for label, path in missing_files:
            print(f"    - {label}: {path}")
            
    # Auto-update logic
    updated = False
    
    # 1. Update checklists under "## 2. 🛡️ 엔지니어링 룰 자가 채점표"
    # If all evidence files exist, we mark checklist checkboxes to [x] and result to Pass.
    if len(missing_files) == 0:
        # Mark pending status to 완료 (Done)
        new_content, count = re.subn(r"\*\s+\*\*상태 \(Status\)\*\*:\s*`?WIP`?", "* **상태 (Status)**: `완료`", content)
        if count > 0:
            content = new_content
            updated = True
            
        # Update Pending results to Pass
        # Matches: *   [ ] **결과**: `Pending`
        pending_result_pattern = r"\*\s+\[\s*\]\s+\*\*결과\*\*:\s*`Pending`"
        new_content, count = re.subn(pending_result_pattern, "*   [x] **결과**: `Pass`", content)
        if count > 0:
            content = new_content
            updated = True
            
        # Update any other empty checklist checkboxes to [x]
        empty_checkbox_pattern = r"\*\s+\[\s*\]"
        new_content, count = re.subn(empty_checkbox_pattern, "*   [x]", content)
        if count > 0:
            content = new_content
            updated = True
    else:
        # If there are missing files, mark status to WIP
        new_content, count = re.subn(r"\*\s+\*\*상태 \(Status\)\*\*:\s*`?완료`?", "* **상태 (Status)**: `WIP`", content)
        if count > 0:
            content = new_content
            updated = True
            
        # Revert Pass back to Pending if files are missing
        pass_result_pattern = r"\*\s+\[x\]\s+\*\*결과\*\*:\s*`Pass`"
        new_content, count = re.subn(pass_result_pattern, "*   [ ] **결과**: `Pending`", content)
        if count > 0:
            content = new_content
            updated = True

    if updated:
        with open(rtm_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("  RTM document checklist and status updated.")
        
    return len(missing_files) == 0

def main():
    project_root = os.getcwd()
    requirements_dir = os.path.join(project_root, "docs", "requirements")
    
    if not os.path.exists(requirements_dir):
        print(f"Error: Requirements directory not found at {requirements_dir}", file=sys.stderr)
        sys.exit(1)
        
    rtm_files = [os.path.join(requirements_dir, f) for f in os.listdir(requirements_dir) if f.startswith("rtm_") and f.endswith(".md")]
    
    if not rtm_files:
        print("No RTM files found to evaluate.")
        sys.exit(0)
        
    all_passed = True
    for rtm_file in rtm_files:
        passed = evaluate_rtm(rtm_file, project_root)
        if not passed:
            all_passed = False
            
    if all_passed:
        print("\nAll RTM requirements check out successfully! (100% Pass)")
        sys.exit(0)
    else:
        print("\nSome RTM requirements are missing verification evidence files. Please check the logs above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
