#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import time

STATE_DIR = os.path.expanduser("~/.gemini/antigravity-ide/state")
STATE_FILE = os.path.join(STATE_DIR, "test_failure_states.json")
MAX_FAILURES = 5

def load_states():
    if not os.path.exists(STATE_FILE):
        return {}
    try:
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

def save_states(states):
    os.makedirs(STATE_DIR, exist_ok=True)
    try:
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(states, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not save loop detector state: {e}", file=sys.stderr)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 test-runner-guard.py <test-command> [args...]", file=sys.stderr)
        sys.exit(1)

    # Reconstruct the test command
    test_args = sys.argv[1:]
    # If the first argument contains space, assume it's a full shell command
    if len(test_args) == 1 and " " in test_args[0]:
        command_str = test_args[0]
        shell = True
    else:
        command_str = " ".join(test_args)
        shell = False

    print(f"Executing guarded test command: {command_str}")
    
    # Run the test command
    start_time = time.time()
    try:
        if shell:
            result = subprocess.run(command_str, shell=True)
        else:
            result = subprocess.run(test_args)
        exit_code = result.returncode
    except Exception as e:
        print(f"Error running command: {e}", file=sys.stderr)
        exit_code = 1

    states = load_states()
    
    # Normalize command name to use as key
    cmd_key = command_str.strip()

    if exit_code == 0:
        # Success: Clear failure count for this command
        if cmd_key in states:
            del states[cmd_key]
            save_states(states)
        print("Test passed successfully. Loop detector state cleared.")
        sys.exit(0)
    else:
        # Failure: Increment count
        cmd_state = states.get(cmd_key, {"count": 0, "failures": []})
        cmd_state["count"] += 1
        cmd_state["failures"].append({
            "timestamp": time.time(),
            "formatted_time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        })
        
        states[cmd_key] = cmd_state
        save_states(states)
        
        print(f"\n[LOOP DETECTOR] Test failed (Consecutive failure count: {cmd_state['count']}/{MAX_FAILURES})")
        
        if cmd_state["count"] >= MAX_FAILURES:
            print("\n" + "="*80, file=sys.stderr)
            print("🚨🚨🚨 [AI AGENT INFINITE LOOP DETECTED / AI 에이전트 무한 루프 감지] 🚨🚨🚨", file=sys.stderr)
            print("="*80, file=sys.stderr)
            print(f"동일한 테스트 명령어 '{cmd_key}'가 연속으로 {cmd_state['count']}회 이상 실패했습니다.", file=sys.stderr)
            print("무분별한 자동 코드 수정 시도는 심각한 API 비용 낭비를 유발할 수 있습니다.", file=sys.stderr)
            print("\n[지침] AI 에이전트는 즉시 작업을 멈추고:", file=sys.stderr)
            print("1. 현재 상태와 테스트 에러 로그를 분석하여 사용자에게 요약 보고하십시오.", file=sys.stderr)
            print("2. 무엇이 문제인지, 어떻게 해결할지에 대해 사용자의 개입과 피드백을 구하십시오.", file=sys.stderr)
            print("3. 사용자의 명시적인 승인/가이드가 있을 때까지 추가 코드 대안 수정을 멈추십시오.", file=sys.stderr)
            print("="*80 + "\n", file=sys.stderr)
            
            # Reset failure count so that the agent has a chance to retry after user intervention
            del states[cmd_key]
            save_states(states)
            
        sys.exit(exit_code)

if __name__ == "__main__":
    main()
