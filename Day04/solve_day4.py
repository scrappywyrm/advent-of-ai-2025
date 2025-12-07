import subprocess
import json
import sys
import os
import itertools
import re

# CONFIGURATION
OPERATOR_DIR = "/home/brucee/goose-operator"
OPERATOR_PYTHON = f"{OPERATOR_DIR}/venv/bin/python3"
OPERATOR_SCRIPT = f"{OPERATOR_DIR}/goose_operator/main.py"

_id_counter = itertools.count(1)
def get_next_id(): return next(_id_counter)

def find_json_result(raw_text: str) -> dict:
    json_start = raw_text.find('{')
    if json_start >= 0:
        try:
            return json.loads(raw_text[json_start:])
        except json.JSONDecodeError:
            pass
    return {}

def extract_bash_code(text: str) -> str:
    """Robust extraction for Bash Scripts"""
    code = None
    pattern = r"```bash(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        code = match.group(1).strip()
    else:
        pattern_generic = r"```sh(.*?)```"
        match_generic = re.search(pattern_generic, text, re.DOTALL)
        if match_generic:
            code = match_generic.group(1).strip()
    
    # Validation: Ensure it looks like a Vercel script
    if code and "vercel" in code:
        return code
    return None

def run_day4():
    print("🚀 Client: Requesting Vercel Deployment Script...")
    
    # We explicitly point to the Day02 folder relative to Day04
    prompt = "Deploy the static website located in '../Day02' to Vercel Production. Generate a non-interactive deployment script."
    
    req = {
        "jsonrpc": "2.0",
        "method": "session/prompt", 
        "id": get_next_id(),
        "params": ["day4-run", [{ "type": "text", "text": prompt }], None]
    }
    
    print(f">> Sending Request to Operator...")
    try:
        process = subprocess.run(
            [OPERATOR_PYTHON, OPERATOR_SCRIPT],
            input=json.dumps(req),
            capture_output=True, text=True, timeout=300
        )

        if process.returncode == 0 and process.stdout.strip():
            final_result = find_json_result(process.stdout)
            
            assistant_msgs = [m for m in final_result.get('messages', []) if m.get('role') == 'assistant']
            if assistant_msgs:
                raw_text = assistant_msgs[-1].get('content', [{}])[0].get('text', '')
                
                clean_code = extract_bash_code(raw_text)
                
                if clean_code:
                    with open("deploy_site.sh", "w") as f:
                        f.write(clean_code)
                    os.chmod("deploy_site.sh", 0o755) # Make executable
                    
                    print("\n✅ DAY 4 SUCCESS (OPERATOR)")
                    print("✨ Policy Enforced: 'winter-festival-launch' (Vercel)")
                    print("📂 Generated Script: deploy_site.sh")
                    print("👉 Now run: ./deploy_site.sh")
                else:
                    print("❌ No valid bash script found.")
                    print(raw_text[:200])
        else:
            print(f"❌ Execution Failed: {process.stderr}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_day4()
