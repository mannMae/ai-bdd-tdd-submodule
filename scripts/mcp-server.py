#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import traceback

# 1. Redirect sys.stdout to sys.stderr to prevent prints from polluting the JSON-RPC channel.
# Keep the original stdout for sending JSON-RPC packets.
rpc_stdout = sys.stdout
sys.stdout = sys.stderr

def log(msg):
    """Logs a message to stderr (which will show in client debugger logs)."""
    sys.stderr.write(f"[MCP-Server] {msg}\n")
    sys.stderr.flush()

def write_message(msg):
    """Writes a JSON-RPC message to the original stdout, followed by a newline."""
    try:
        rpc_stdout.write(json.dumps(msg) + "\n")
        rpc_stdout.flush()
    except Exception as e:
        log(f"Error writing message: {e}")

def send_error(req_id, code, message, data=None):
    res = {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {
            "code": code,
            "message": message
        }
    }
    if data:
        res["error"]["data"] = data
    write_message(res)

def send_response(req_id, result):
    res = {
        "jsonrpc": "2.0",
        "id": req_id,
        "result": result
    }
    write_message(res)

# List of supported tools
TOOLS = [
    {
        "name": "get_bdd_dashboard",
        "description": "Returns the current BDD & TDD development progress dashboard showing requirement checklists and verification status.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "check_cycles",
        "description": "Scans the project for cyclic import dependencies to prevent tight coupling and spaghetti code.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "check_boundaries",
        "description": "Enforces architectural import boundary rules configured in boundary-rules.json (e.g. preventing frontend from importing backend/database code).",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "evaluate_rtm",
        "description": "Runs the RTM (Requirements Traceability Matrix) evaluator to verify that implementation checklist markers match actual test status.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "run_self_heal",
        "description": "Performs self-healing on the project by running ESLint and Ruff auto-fixes and generating a SELF_HEAL_REPORT.md for remaining lint errors.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "summarize_project",
        "description": "Generates a compressed PROJECT_CONTEXT.md file summarizing component hierarchy and backend schema to minimize LLM token usage.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "update_project_map",
        "description": "Regenerates and updates the PROJECT_MAP.md directory tree mapping of the project.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "generate_test_stubs",
        "description": "Generates frontend/backend unit and E2E test stubs (Vitest, Playwright, pytest-bdd) from a Gherkin .feature file.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "feature_path": {
                    "type": "string",
                    "description": "Relative path to the Gherkin .feature file (e.g. docs/user-flow/monitoring.feature)"
                },
                "output_dir": {
                    "type": "string",
                    "description": "Destination directory where test stubs will be generated (e.g. src/features/monitoring/tests)"
                }
            },
            "required": ["feature_path", "output_dir"]
        }
    }
]

def run_script(script_name, args=None):
    """Executes a submodule python script and returns the stdout/stderr and exit code."""
    if args is None:
        args = []
        
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, script_name)
    
    if not os.path.exists(script_path):
        return f"Error: Script {script_name} not found at {script_path}", True
        
    cmd = [sys.executable, script_path] + args
    log(f"Executing command: {' '.join(cmd)}")
    
    try:
        # Run with the current environment and cwd
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
        output = ""
        if result.stdout:
            output += result.stdout
        if result.stderr:
            if output:
                output += "\n"
            output += f"--- Stderr ---\n{result.stderr}"
            
        return output.strip(), result.returncode != 0
    except Exception as e:
        return f"Exception executing script {script_name}: {e}\n{traceback.format_exc()}", True

def handle_tool_call(name, arguments):
    """Dispatches the tool call to the corresponding script execution."""
    if name == "get_bdd_dashboard":
        return run_script("bdd-dashboard.py")
    elif name == "check_cycles":
        return run_script("check-cycles.py")
    elif name == "check_boundaries":
        return run_script("check-boundaries.py")
    elif name == "evaluate_rtm":
        return run_script("rtm-evaluator.py")
    elif name == "run_self_heal":
        return run_script("self-heal.py")
    elif name == "summarize_project":
        return run_script("summarize-project.py")
    elif name == "update_project_map":
        return run_script("update-map.py")
    elif name == "generate_test_stubs":
        feature_path = arguments.get("feature_path")
        output_dir = arguments.get("output_dir")
        if not feature_path or not output_dir:
            return "Error: Both 'feature_path' and 'output_dir' arguments are required for generate_test_stubs.", True
        return run_script("generate-test-stubs.py", [feature_path, output_dir])
    else:
        return f"Unknown tool: {name}", True

def main():
    log("Starting MCP Server over Stdio...")
    
    initialized = False
    
    try:
        while True:
            line = sys.stdin.readline()
            if not line:
                log("Stdin closed, exiting...")
                break
                
            line = line.strip()
            if not line:
                continue
                
            try:
                request = json.loads(line)
            except json.JSONDecodeError as e:
                log(f"JSON Decode Error: {e}")
                send_error(None, -32700, "Parse error: Invalid JSON")
                continue
                
            if not isinstance(request, dict) or "method" not in request:
                send_error(request.get("id"), -32600, "Invalid Request: 'method' field is required")
                continue
                
            method = request["method"]
            req_id = request.get("id")
            params = request.get("params", {})
            
            log(f"Received request - Method: {method}, ID: {req_id}")
            
            # Protocol lifecycle methods
            if method == "initialize":
                initialized = True
                res = {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "ai-bdd-tdd-mcp-server",
                        "version": "1.0.0"
                    }
                }
                send_response(req_id, res)
                
            elif method == "notifications/initialized":
                log("Notification: Client initialized")
                
            elif method == "tools/list":
                if not initialized:
                    send_error(req_id, -32002, "Server not initialized")
                    continue
                send_response(req_id, {"tools": TOOLS})
                
            elif method == "tools/call":
                if not initialized:
                    send_error(req_id, -32002, "Server not initialized")
                    continue
                    
                tool_name = params.get("name")
                tool_args = params.get("arguments", {})
                
                if not tool_name:
                    send_error(req_id, -32602, "Invalid params: 'name' is required for tools/call")
                    continue
                    
                log(f"Calling tool: {tool_name}")
                output_text, is_err = handle_tool_call(tool_name, tool_args)
                
                tool_result = {
                    "content": [
                        {
                            "type": "text",
                            "text": output_text
                        }
                    ],
                    "isError": is_err
                }
                send_response(req_id, tool_result)
                
            else:
                send_error(req_id, -32601, f"Method not found: {method}")
                
    except Exception as e:
        log(f"Fatal server exception: {e}\n{traceback.format_exc()}")
        sys.exit(1)

if __name__ == "__main__":
    main()
