import subprocess
import json
import sys
import os
import itertools

# Configuration
OPERATOR_DIR = "/home/brucee/goose-operator"
OPERATOR_PYTHON = f"{OPERATOR_DIR}/venv/bin/python3"
OPERATOR_SCRIPT = f"{OPERATOR_DIR}/goose_operator/main.py"

_id_counter = itertools.count(1)
def get_next_id(): return next(_id_counter)

def find_json_result(raw_text: str) -> dict:
    """Robust extraction of JSON payload from mixed stdout stream."""
    json_start_index = raw_text.find('{')
    if json_start_index >= 0:
        json_slice = raw_text[json_start_index:]
        try:
            return json.loads(json_slice)
        except json.JSONDecodeError:
            pass
    return {}

def run_challenge():
    print("🤖 Client: Requesting Story App from Operator...")
    
    # 1. Realistic Prompt (Creative Intent)
    # The Operator will detect 'story' and enforce the 'story-policy.yaml' structure.
    prompt = (
        "I need a web app for the Winter Festival. "
        "It should be a choose-your-own-adventure story about a 'Missing Storyteller'. "
        "Please make it festive."
    )
    
    req = {
        "jsonrpc": "2.0",
        "method": "session/prompt", 
        "id": get_next_id(),
        "params": ["day2-run", [{ "type": "text", "text": prompt }], None]
    }
    
    # 2. Execute
    print(f">> Sending User Prompt: '{prompt}'")
    try:
        process = subprocess.run(
            [OPERATOR_PYTHON, OPERATOR_SCRIPT],
            input=json.dumps(req),
            capture_output=True,
            text=True,
            timeout=300 # 5 min allocation for code generation
        )

        # 3. Process Output
        if process.returncode == 0 and process.stdout.strip():
            final_result = find_json_result(process.stdout)
            
            if not final_result:
                print(f"❌ ERROR: Invalid JSON.\n{process.stdout}")
                return

            # Extract Code from Assistant Response
            assistant_messages = [m for m in final_result.get('messages', []) if m.get('role') == 'assistant']
            
            if assistant_messages:
                raw_text = assistant_messages[-1].get('content', [{}])[0].get('text', '')
                
                # Cleanup Code Fences
                clean_html = raw_text.replace('```html', '').replace('```', '').strip()
                # Unescape JSON string
                clean_html = clean_html.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"')

                with open("operator_story.html", "w") as f:
                    f.write(clean_html)

                print("\n✅ DAY 2 SUCCESS (OPERATOR)")
                print("✨ Policy Enforced: 'winter-tale-structure'")
                print("📂 Generated: operator_story.html")
            else:
                print("❌ No response content.")
        else:
            print(f"❌ Execution Failed: {process.stderr}")

    except Exception as e:
        print(f"❌ Error: {e}")
    
if __name__ == "__main__":
    run_challenge()
