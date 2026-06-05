#!/usr/bin/env python3
import os
import sys
import re

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
    # Match imports starting with apps. or src.
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
        # Try TSX, TS, JSX, JS, and index files
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
        # Assuming '@/' maps to 'src/' of frontend or packages
        # Search for src/ folder in project_root to resolve
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

def find_cycles(graph):
    """Finds all simple cycles in a directed graph using DFS."""
    visited = {}
    path = []
    cycles = []
    
    def dfs(node):
        visited[node] = 1 # Visiting
        path.append(node)
        
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor)
            elif visited[neighbor] == 1:
                # Cycle detected!
                cycle_start_idx = path.index(neighbor)
                cycle = path[cycle_start_idx:] + [neighbor]
                cycles.append(cycle)
                
        path.pop()
        visited[node] = 2 # Visited
        
    for node in graph:
        if node not in visited:
            dfs(node)
            
    return cycles

def main():
    project_root = os.getcwd()
    print(f"Scanning for circular dependencies under: {project_root}")
    
    graph = {}
    
    # 1. Build import graph
    for root, dirs, files in os.walk(project_root):
        # Prune standard ignored directories and any dir ending in env/venv
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.endswith("env") and not d.endswith("venv")]
        
        # Skip if it is a python virtualenv or library path
        if "pyvenv.cfg" in files or "site-packages" in root or "node_modules" in root:
            dirs[:] = []  # Don't descend further
            continue
            
        for file in files:
            filepath = os.path.join(root, file)
            abs_filepath = os.path.abspath(filepath)
            
            if file.endswith(".py"):
                deps = get_imports_python(filepath, project_root)
                if deps:
                    graph[abs_filepath] = deps
            elif file.endswith((".ts", ".tsx", ".js", ".jsx")):
                deps = get_imports_js(filepath, project_root)
                if deps:
                    graph[abs_filepath] = deps
                    
    # 2. Detect cycles
    cycles = find_cycles(graph)
    
    if cycles:
        print("\n" + "="*80, file=sys.stderr)
        print("❌ [CIRCULAR DEPENDENCY DETECTED / 순환 참조 감지됨]", file=sys.stderr)
        print("="*80, file=sys.stderr)
        print("프로젝트 아키텍처 규칙 상 순환 참조는 허용되지 않습니다.", file=sys.stderr)
        print("다음 파일 간에 서로를 참조하는 고리가 발견되었습니다:\n", file=sys.stderr)
        
        for idx, cycle in enumerate(cycles):
            # Format paths relative to project root for clean display
            rel_cycle = [os.path.relpath(p, project_root) for p in cycle]
            chain = " ➔ ".join(rel_cycle)
            print(f"  Cycle #{idx+1}: {chain}", file=sys.stderr)
            
        print("="*80, file=sys.stderr)
        sys.exit(1)
        
    print("No circular dependencies detected. Architecture clean!")
    sys.exit(0)

if __name__ == "__main__":
    main()
