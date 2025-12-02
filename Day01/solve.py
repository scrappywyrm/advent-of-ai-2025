import subprocess
import json
import sys
import os
import time
import itertools

# CONFIGURATION: External Paths
OPERATOR_DIR = "/home/brucee/goose-operator"
OPERATOR_PYTHON = f"{OPERATOR_DIR}/venv/bin/python3"
OPERATOR_SCRIPT = f"{OPERATOR_DIR}/goose_operator/main.py"
POLICY_PATH = f"{OPERATOR_DIR}/fortune-policy.yaml"

# JSON-RPC ID Counter (unique per request)
_id_counter = itertools.count(1)
def get_next_id(): return next(_id_counter)

def find_json_result(raw_text: str) -> dict:
    """Surgically extracts the complete JSON payload by skipping leading noise."""
    json_start_index = raw_text.find('{')
    if json_start_index >= 0:
        json_slice = raw_text[json_start_index:]
        try:
            return json.loads(json_slice)
        except json.JSONDecodeError:
            pass
    return {}

def render_and_exit(final_result):
    """Extracts the final assistant message and renders the clean output."""
    
    # 1. Extract the final assistant message
    assistant_messages = [ m for m in final_result.get('messages', []) if m.get('role') == 'assistant' ]
    
    if assistant_messages:
        full_text_parts = []
        for message in assistant_messages:
            # Content is often a list, so we check the first element
            content_blocks = message.get('content', [])
            if content_blocks and content_blocks[0].get('type') == 'text':
                full_text_parts.append(content_blocks[0].get('text'))

        # Join all message parts
        raw_fortune_text = "\n".join(full_text_parts)
        # --------------------------------------------------
        
        if not raw_fortune_text.strip():
            # Check if the final response was an error or empty
            print(f"❌ Error: Final content was empty. Check Stderr for tool errors.")
            return

        clean_text = raw_fortune_text.replace('\\n', '\n').replace('\\t', '\t')

        print("\n--- AOAI Day 1 ---")
        print("✨ **Admission Controller**: Mutated prompt and executed.")
        print("\n*** FINAL FORTUNE OUTPUT ***")
        print(clean_text) 
        print("----------------------------")
        
    else:
        print(f"❌ Error: No final assistant response found in JSON.")

def run_challenge():
    print("🤖 Client: Connecting to Goose Operator (Admission Controller)...")
    
    # Prepare Environment (Pass Policy Path)
    env = os.environ.copy()
    env["RECONCILER_CRDS"] = POLICY_PATH

    # Define the FINAL prompt request structure 
    prompt = "I need fortunes for Zelda."
    
    req = {
        "jsonrpc": "2.0",
        "method": "session/prompt", 
        "id": get_next_id(),
        "params": [
            "day1-run", 
            [{ "type": "text", "text": prompt }],
            None
        ]
    }
    
    # EXECUTE SYNCHRONOUSLY
    print(f">> Sending Mutated Prompt Request...")
    
    try:
        process = subprocess.run(
            [OPERATOR_PYTHON, OPERATOR_SCRIPT],
            input=json.dumps(req),
            capture_output=True,
            text=True,
            env=env,
            timeout=130
        )

        # PROCESS OUTPUT
        if process.returncode == 0 and process.stdout.strip():
            final_result = find_json_result(process.stdout)
            
            if not final_result:
                print(f"❌ ERROR: Operator failed to return valid JSON. Raw output:\n{process.stdout}")
                return

            render_and_exit(final_result)
            
        else:
            print(f"❌ EXECUTION FAILED (RC={process.returncode}). Stderr:\n{process.stderr}")

    except subprocess.TimeoutExpired:
        print(f"❌ ERROR: Timeout expired after 130s. LLM was too slow.")
    except Exception as e:
        print(f"❌ ERROR: Critical failure during execution: {e}")
    
if __name__ == "__main__":
    if not os.path.exists(f"{OPERATOR_DIR}/goose_operator/main.py"):
        print(f"Error: Operator main script not found at {OPERATOR_DIR}/goose_operator/main.py")
        sys.exit(1)
    run_challenge()
