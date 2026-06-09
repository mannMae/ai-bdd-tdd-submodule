#!/usr/bin/env python3
import os
import sys
import re
import json
import fnmatch

IGNORE_DIRS = {'.git', 'node_modules', 'venv', '.venv', '.agents', '.agents-local', 'dist', '__pycache__', '.pytest_cache'}

def get_imports_python(filepath, project_root):
    """Parses python import statements and resolves them to file paths."""
    imports = []
    dir_path = os.path.dirname(filepath)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return []
        
    # Pattern 1: from .relative import something
    rel_import_pattern = r"from\s+(\.+)([a-zA-Z0-9_]*)\s+import"
    for match in re.finditer(rel_import_pattern, content):
        dots = match.group(1)
        mod = match.group(2)
        
        # Resolve path based on dots
        target_dir = dir_path
        for _ in range(len(dots) - 1):
            target_dir = os.path.dirname(target_dir)
            
        target_file_base = os.path.join(target_dir, mod) if mod else target_dir
        
        # Check potential extensions
        resolved = None
        for ext in ['.py', '/__init__.py']:
            if os.path.exists(target_file_base + ext):
                resolved = os.path.abspath(target_file_base + ext)
                break
        if resolved:
            imports.append(resolved)
            
    # Pattern 2: from apps.backend... or local packages
    abs_import_pattern = r"(?:from|import)\s+((?:apps|src|packages)\.[a-zA-Z0-9_\.]+)"
    for match in re.finditer(abs_import_pattern, content):
        mod_path = match.group(1).replace('.', '/')
        target_file_base = os.path.join(project_root, mod_path)
        
        resolved = None
        for ext in ['.py', '/__init__.py', '/service.py', '/router.py']:
            if os.path.exists(target_file_base + ext):
                resolved = os.path.abspath(target_file_base + ext)
                break
        if resolved:
            imports.append(resolved)
            
    return imports

def get_imports_js(filepath, project_root):
    """Parses JS/TS import statements and resolves them to file paths."""
    imports = []
    dir_path = os.path.dirname(filepath)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return []
        
    # Match imports with relative paths: from './something' or from '../something'
    js_import_pattern = r"from\s+[\"'](\.\.?[/a-zA-Z0-9_\-\.]+)[\"']"
    for match in re.finditer(js_import_pattern, content):
        import_path = match.group(1)
        target_file_base = os.path.normpath(os.path.join(dir_path, import_path))
        
        resolved = None
        for ext in ['.tsx', '.ts', '.jsx', '.js', '/index.tsx', '/index.ts', '/index.js']:
            if os.path.exists(target_file_base + ext):
                resolved = os.path.abspath(target_file_base + ext)
                break
        if resolved:
            imports.append(resolved)
            
    # Match imports with absolute/alias paths: from '@/something' or from 'features/something'
    alias_import_pattern = r"from\s+[\"']@/([/a-zA-Z0-9_\-\.]+)[\"']"
    for match in re.finditer(alias_import_pattern, content):
        import_path = match.group(1)
        for src_folder in ["apps/frontend/src", "frontend/src", "src"]:
            src_path = os.path.join(project_root, src_folder)
            if os.path.exists(src_path):
                target_file_base = os.path.normpath(os.path.join(src_path, import_path))
                resolved = None
                for ext in ['.tsx', '.ts', '.jsx', '.js', '/index.tsx', '/index.ts', '/index.js']:
                    if os.path.exists(target_file_base + ext):
                        resolved = os.path.abspath(target_file_base + ext)
                        break
                if resolved:
                    imports.append(resolved)
                    break
                    
    return imports

def match_path(path, pattern):
    """Matches a file path against a pattern, supporting globs and cross-platform slashes."""
    path = path.replace('\\', '/').strip('/')
    pattern = pattern.replace('\\', '/').strip('/')
    
    # Standardize recursive glob ** to * for fnmatch since python fnmatch handles multi-level matching with *
    pattern = pattern.replace('**/', '*').replace('**', '*')
    
    # If the pattern points to a directory without wildcards (e.g. apps/frontend)
    # let's treat it as a directory prefix match
    if '*' not in pattern and '?' not in pattern and not os.path.basename(pattern).count('.'):
        return path == pattern or path.startswith(pattern + '/')
        
    return fnmatch.fnmatch(path, pattern)

def load_rules(project_root):
    """Loads boundary-rules.json from the project root or fallback templates."""
    paths_to_try = [
        os.path.join(project_root, 'boundary-rules.json'),
        os.path.join(project_root, '.agents', 'configs', 'boundary-rules.template.json')
    ]
    
    for path in paths_to_try:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('rules', [])
            except Exception as e:
                print(f"Warning: Failed to parse boundary rules file {path}: {e}", file=sys.stderr)
                
    return []

def main():
    project_root = os.getcwd()
    
    # Load rules
    rules = load_rules(project_root)
    if not rules:
        print("No architecture boundary rules found. Skipping boundary check.")
        sys.exit(0)
        
    print(f"Scanning for architecture boundary violations under: {project_root}")
    
    violations = []
    
    # 1. Scan files and check rules
    for root, dirs, files in os.walk(project_root):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.endswith("env") and not d.endswith("venv")]
        
        if "pyvenv.cfg" in files or "site-packages" in root or "node_modules" in root:
            dirs[:] = []
            continue
            
        for file in files:
            filepath = os.path.join(root, file)
            abs_filepath = os.path.abspath(filepath)
            rel_filepath = os.path.relpath(abs_filepath, project_root)
            
            deps = []
            if file.endswith(".py"):
                deps = get_imports_python(filepath, project_root)
            elif file.endswith((".ts", ".tsx", ".js", ".jsx")):
                deps = get_imports_js(filepath, project_root)
                
            if not deps:
                continue
                
            # Check rules against this file
            for rule in rules:
                source_pattern = rule.get('source')
                if not source_pattern:
                    continue
                    
                if match_path(rel_filepath, source_pattern):
                    forbidden_imports = rule.get('forbidden_imports', [])
                    description = rule.get('description', 'Forbidden import boundary violation')
                    
                    for dep in deps:
                        rel_dep = os.path.relpath(dep, project_root)
                        
                        for forbidden_pattern in forbidden_imports:
                            if match_path(rel_dep, forbidden_pattern):
                                violations.append({
                                    'file': rel_filepath,
                                    'dependency': rel_dep,
                                    'description': description,
                                    'pattern': forbidden_pattern
                                })
                                
    # 2. Report violations
    if violations:
        print("\n" + "="*80, file=sys.stderr)
        print("❌ [ARCHITECTURE BOUNDARY VIOLATION DETECTED / 아키텍처 경계 위반 감지됨]", file=sys.stderr)
        print("="*80, file=sys.stderr)
        print("프로젝트 설계 규칙 상 허용되지 않는 의존성 가져오기가 발견되었습니다:\n", file=sys.stderr)
        
        for idx, v in enumerate(violations):
            print(f"  Violation #{idx+1}:", file=sys.stderr)
            print(f"    Source File:  {v['file']}", file=sys.stderr)
            print(f"    Imported:     {v['dependency']} (matches pattern '{v['pattern']}')", file=sys.stderr)
            print(f"    Rule:         {v['description']}", file=sys.stderr)
            print("-" * 60, file=sys.stderr)
            
        print("="*80, file=sys.stderr)
        sys.exit(1)
        
    print("No architecture boundary violations detected. Boundaries clean!")
    sys.exit(0)

if __name__ == "__main__":
    main()
