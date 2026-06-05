#!/usr/bin/env python3
import os
import sys
import re

def parse_feature_file(filepath):
    """Parses Gherkin feature file into features, scenarios, and steps."""
    if not os.path.exists(filepath):
        print(f"Error: Feature file not found at {filepath}", file=sys.stderr)
        sys.exit(1)
        
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    feature_name = "Feature"
    scenarios = []
    current_scenario = None
    
    for line in lines:
        line_str = line.strip()
        if not line_str or line_str.startswith("#"):
            continue
            
        # Match Feature header
        feature_match = re.match(r"^Feature:\s*(.+)$", line_str)
        if feature_match:
            feature_name = feature_match.group(1).strip()
            continue
            
        # Match Scenario header
        scenario_match = re.match(r"^(?:Scenario|Scenario Outline):\s*(.+)$", line_str)
        if scenario_match:
            if current_scenario:
                scenarios.append(current_scenario)
            current_scenario = {
                "name": scenario_match.group(1).strip(),
                "steps": []
            }
            continue
            
        # Match steps: Given, When, Then, And, But
        step_match = re.match(r"^(Given|When|Then|And|But)\s+(.+)$", line_str)
        if step_match and current_scenario:
            step_type = step_match.group(1)
            step_text = step_match.group(2).strip()
            current_scenario["steps"].append((step_type, step_text))
            
    if current_scenario:
        scenarios.append(current_scenario)
        
    return feature_name, scenarios

def generate_frontend_stub(feature_name, scenarios):
    """Generates Vitest / RTL React testing stub code."""
    code = "import { render, screen } from '@testing-library/react';\n"
    code += "import { describe, it, expect } from 'vitest';\n\n"
    code += f"describe('{feature_name}', () => {{\n"
    
    for sc in scenarios:
        # Normalize scenario name for JS comments
        sc_name = sc["name"].replace("'", "\\'")
        code += f"  it('{sc_name}', async () => {{\n"
        code += "    // TODO: Setup components and renders\n"
        for step_type, step_text in sc["steps"]:
            code += f"    // {step_type} {step_text}\n"
        code += "    expect(true).toBe(true); // Placeholder assertion\n"
        code += "  });\n\n"
        
    code += "});\n"
    return code

def generate_backend_stub(feature_name, scenarios):
    """Generates pytest-bdd style backend python test stub code."""
    code = "import pytest\n"
    code += "from pytest_bdd import scenarios, given, when, then\n\n"
    code += "# Load scenarios from feature file\n"
    code += "# Replace with the actual path to the feature file relative to test file\n"
    code += "scenarios('../features/change_me.feature')\n\n"
    
    # Track step definitions to prevent duplicate definitions in the same file
    defined_steps = set()
    
    for sc in scenarios:
        code += f"# Scenario: {sc['name']}\n"
        for step_type, step_text in sc["steps"]:
            # Clean step text to use as python function name
            func_name = step_text.lower()
            func_name = re.sub(r'[^a-z0-9_]', '_', func_name)
            func_name = re.sub(r'_+', '_', func_name).strip('_')
            
            # Step decorator type (lower case given/when/then)
            dec_type = step_type.lower()
            if dec_type in ["and", "but"]:
                dec_type = "then" # Fallback to then for and/but or dynamically resolve
                
            step_key = (dec_type, step_text)
            if step_key in defined_steps:
                continue
            defined_steps.add(step_key)
            
            code += f"@{dec_type}('{step_text}')\ndef {dec_type}_{func_name}():\n"
            code += "    # TODO: Implement step logic\n"
            code += "    pass\n\n"
            
    return code

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 generate-test-stubs.py <path-to-feature-file> [output-dir]", file=sys.stderr)
        sys.exit(1)
        
    feature_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else os.getcwd()
    
    feature_name, scenarios = parse_feature_file(feature_file)
    base_name = os.path.splitext(os.path.basename(feature_file))[0]
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Generate Frontend Vitest Stub
    fe_code = generate_frontend_stub(feature_name, scenarios)
    fe_filename = f"stub_{base_name}.test.tsx"
    fe_path = os.path.join(output_dir, fe_filename)
    with open(fe_path, 'w', encoding='utf-8') as f:
        f.write(fe_code)
    print(f"Generated Frontend Vitest Stub: {fe_path}")
    
    # 2. Generate Backend pytest-bdd Stub
    be_code = generate_backend_stub(feature_name, scenarios)
    be_filename = f"stub_{base_name}_test.py"
    be_path = os.path.join(output_dir, be_filename)
    with open(be_path, 'w', encoding='utf-8') as f:
        f.write(be_code)
    print(f"Generated Backend pytest-bdd Stub: {be_path}")

if __name__ == "__main__":
    main()
