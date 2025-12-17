import subprocess
import json
import sys
import os
import itertools
import re

# --- CONFIGURATION (Remote Ready) ---
# Defaults to local dev path, but allows override via GOOSE_OPERATOR_HOME
DEFAULT_HOME = "/home/brucee/goose-operator"
OPERATOR_DIR = os.getenv("GOOSE_OPERATOR_HOME", DEFAULT_HOME)

OPERATOR_PYTHON = f"{OPERATOR_DIR}/venv/bin/python3"
OPERATOR_SCRIPT = f"{OPERATOR_DIR}/goose_operator/main.py"

# Sanity Check
if not os.path.exists(OPERATOR_SCRIPT):
    print(f"❌ CRITICAL: Operator not found at {OPERATOR_SCRIPT}")
    print(f"   Run: export GOOSE_OPERATOR_HOME=/path/to/operator")
    sys.exit(1)

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

def extract_html_code(text: str) -> str:
    # 1. Try Markdown
    pattern = r"```html(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    if match: return match.group(1).strip()
    
    # 2. Try raw HTML
    start_tag = "<!DOCTYPE html>"
    end_tag = "</html>"
    start_index = text.find(start_tag)
    end_index = text.find(end_tag)
    if start_index != -1 and end_index != -1:
        return text[start_index : end_index + len(end_tag)]
    return None

def run_day5():
    print("✈️  Client: Requesting Gesture Control Interface...")
    print(f"   (Using Operator at: {OPERATOR_DIR})")
    
    prompt = "Generate a 'Homecoming Board' flight tracker HUD with Igloo and Reindeer visuals. It needs to track flights and be controlled by hand gestures via webcam."
    
    req = {
        "jsonrpc": "2.0",
        "method": "session/prompt", 
        "id": get_next_id(),
        "params": ["day5-run", [{ "type": "text", "text": prompt }], None]
    }
    
    print(f">> Sending Specs to Operator...")
    try:
        process = subprocess.run(
            [OPERATOR_PYTHON, OPERATOR_SCRIPT],
            input=json.dumps(req),
            capture_output=True, text=True, timeout=300
        )

        if process.returncode != 0:
            print(f"❌ Operator Crashed (Exit Code {process.returncode})")
            return

        final_result = find_json_result(process.stdout.strip())
        assistant_msgs = [m for m in final_result.get('messages', []) if m.get('role') == 'assistant']
        
        if assistant_msgs:
            raw_text = assistant_msgs[-1].get('content', [{}])[0].get('text', '')
            clean_code = extract_html_code(raw_text)
            
            if clean_code:
                with open("operator_hud.html", "w") as f:
                    f.write(clean_code)
                print("\n✅ DAY 5 SUCCESS (HTML Generated)")
                print("   Artifact: operator_hud.html")
            elif os.path.exists("operator_hud.html"):
                print("\n✅ DAY 5 SUCCESS (Found on disk)")
            else:
                print("\n⚠️  Operator responded, but no HTML found.")
        else:
            print("\n⚠️  Operator returned JSON, but no Assistant message.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_day5()
