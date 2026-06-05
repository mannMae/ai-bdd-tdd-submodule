#!/usr/bin/env python3
import os
import sys
import re

# Ignore list for directory scanning
IGNORE_DIRS = {
    '.git', 'node_modules', 'venv', '.venv', '.agents', '.agents-local',
    'dist', '.next', 'build', '__pycache__', '.pytest_cache', '.mypy_cache',
    '.vscode', '.idea', 'out', '.DS_Store'
}

IGNORE_FILES = {
    '.DS_Store', 'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml', 'poetry.lock'
}

def generate_tree(dir_path, prefix="", depth=0, max_depth=4):
    """Recursively generates a visual directory tree string."""
    if depth >= max_depth:
        return ""
    
    try:
        entries = sorted(os.listdir(dir_path))
    except OSError:
        return ""
        
    # Filter ignored items
    entries = [e for e in entries if e not in IGNORE_DIRS and e not in IGNORE_FILES]
    
    tree_str = ""
    for i, entry in enumerate(entries):
        path = os.path.join(dir_path, entry)
        is_last = (i == len(entries) - 1)
        connector = "└── " if is_last else "├── "
        
        # Add visual markers for directories vs files
        visual_name = entry
        if os.path.isdir(path):
            visual_name += "/"
            
        tree_str += f"{prefix}{connector}{visual_name}\n"
        
        if os.path.isdir(path):
            new_prefix = prefix + ("    " if is_last else "│   ")
            tree_str += generate_tree(path, new_prefix, depth + 1, max_depth)
            
    return tree_str

def detect_tech_stacks(root_dir):
    """Detects technologies and frameworks in the workspace."""
    stacks = []
    
    # Check for frontend indicators
    has_package_json = False
    for r, d, f in os.walk(root_dir):
        # Skip ignore directories
        d[:] = [dirname for dirname in d if dirname not in IGNORE_DIRS]
        if "package.json" in f:
            has_package_json = True
            break
            
    if has_package_json:
        stacks.append("React / TypeScript / JavaScript (Node.js)")
        
    # Check for python indicators
    has_python = False
    for r, d, f in os.walk(root_dir):
        d[:] = [dirname for dirname in d if dirname not in IGNORE_DIRS]
        if any(filename.endswith(".py") or filename in ["pyproject.toml", "requirements.txt"] for filename in f):
            has_python = True
            break
            
    if has_python:
        stacks.append("Python")
        
    return stacks

def main():
    # Since this script runs inside parent repository root (pwd), or is called from it.
    # We resolve the target parent root.
    parent_root = os.getcwd()
    map_path = os.path.join(parent_root, "PROJECT_MAP.md")
    
    if not os.path.exists(map_path):
        # Try to copy from sample if available
        sample_path = os.path.join(parent_root, ".agents", "PROJECT_MAP.sample.md")
        if os.path.exists(sample_path):
            print(f"Creating PROJECT_MAP.md from sample...")
            with open(sample_path, 'r', encoding='utf-8') as f:
                content = f.read()
            with open(map_path, 'w', encoding='utf-8') as f:
                f.write(content)
        else:
            print("Error: PROJECT_MAP.md not found and .agents/PROJECT_MAP.sample.md not available.", file=sys.stderr)
            sys.exit(1)
            
    print(f"Scanning directory tree under: {parent_root}")
    tree_diagram = "root/\n" + generate_tree(parent_root)
    
    # Read existing map
    with open(map_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # 1. Update the tree block under "### 시각적 프로젝트 구조 예시 (Visual Directory Tree Example)"
    tree_header_pattern = r"(### 시각적 프로젝트 구조 예시 \(Visual Directory Tree Example\)\s*\n+)(```text\n[\s\S]*?\n```|```\n[\s\S]*?\n```)"
    
    new_tree_block = f"\\1```text\n{tree_diagram}```"
    
    updated_content, count = re.subn(tree_header_pattern, new_tree_block, content, flags=re.MULTILINE)
    
    if count == 0:
        print("Warning: Could not find tree block placeholder. Appending to end of file.")
        updated_content = content + f"\n\n### 시각적 프로젝트 구조 예시\n```text\n{tree_diagram}```\n"
        
    # 2. Detect and format tech stacks in the header if possible
    detected_tech = detect_tech_stacks(parent_root)
    if detected_tech:
        print(f"Detected Technology Stacks: {', '.join(detected_tech)}")
        
    # Write back the updated map
    with open(map_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
        
    print("PROJECT_MAP.md directory tree updated successfully.")

if __name__ == "__main__":
    main()
