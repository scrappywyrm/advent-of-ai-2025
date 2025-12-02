import subprocess
import json
import sys
import os

def test_direct():
    print("🤖 Debug: Connecting DIRECTLY to 'goose acp'...")
    
    # 1. Spawn Goose directly (No Operator)
    goose = subprocess.Popen(
        ['goose', 'acp'], 
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=sys.stderr,
        text=True,
        bufsize=1
    )

    # 2. Handshake
    print(">> Sending Initialize...")
    init_req = {
        "jsonrpc": "2.0", 
        "method": "initialize", 
        "id": 1, 
        "params": {
            "protocolVersion": "2024-11-05", 
            "capabilities": {},
            "clientInfo": {"name": "debug-client", "version": "1.0"}
        }
    }
    json.dump(init_req, goose.stdin)
    goose.stdin.write('\n')
    goose.stdin.flush()

    # 3. Simple Prompt (No Fortunes, No Mutation)
    print(">> Sending Prompt 'hello'...")
    req = {
        "jsonrpc": "2.0",
        "method": "session/prompt",
        "params": {
            "sessionId": "debug-session",
            "prompt": {"text": "hello"} 
        }
    }
    json.dump(req, goose.stdin)
    goose.stdin.write('\n')
    goose.stdin.flush()

    # 4. Read Loop
    print(">> Reading stream (Ctrl+C to stop)...")
    while True:
        line = goose.stdout.readline()
        if not line: break
        print(f"RECV: {line.strip()}")

if __name__ == "__main__":
    test_direct()
