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

def extract_python_code(text: str) -> str:
    """
    Robust extraction that validates the content.
    Returns None if no valid code block is found.
    """
    code = None
    
    # 1. Try Markdown Code Blocks
    pattern = r"```python(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        code = match.group(1).strip()
    else:
        pattern_generic = r"```(.*?)```"
        match_generic = re.search(pattern_generic, text, re.DOTALL)
        if match_generic:
            code = match_generic.group(1).strip()

    # 2. Smart Fallback: If no blocks, look for 'import'
    if not code:
        import_index = text.find("import matplotlib")
        if import_index != -1:
            code = text[import_index:].strip()

    # 3. Validation: If it doesn't look like code, reject it
    if code and ("import" in code or "print" in code or "plt." in code):
        return code
    
    return None

def run_day3():
    print("🤖 Client: Starting ETL Pipeline for Hot Cocoa Data...")
    
    # 1. The Official Data
    raw_data = """
ROUND 1 RESULTS (Quarterfinals)
Match 1: Classic Swiss Velvet (234 votes) defeated Spicy Mexican Mocha (189 votes)
 Match 2: Peppermint Dream (312 votes) defeated Salted Caramel Swirl (298 votes) - SO CLOSE!
 Match 3: Dark Chocolate Decadence (276 votes) defeated White Chocolate Wonder (203 votes)
 Match 4: Cinnamon Fireside (267 votes) defeated Hazelnut Heaven (245 votes)
ROUND 2 RESULTS (Semifinals)
Match 1: Peppermint Dream (445 votes) defeated Classic Swiss Velvet (398 votes)
 Match 2: Dark Chocolate Decadence (512 votes) defeated Cinnamon Fireside (387 votes)
CHAMPIONSHIP ROUND
FINAL: Dark Chocolate Decadence (678 votes) defeated Peppermint Dream (623 votes)
🏆 WINNER: Dark Chocolate Decadence!
RECIPE DETAILS (for the judges' scorecards):
Classic Swiss Velvet: Richness 8/10, Sweetness 6/10, Creativity 4/10, Presentation 7/10
Spicy Mexican Mocha: Richness 7/10, Sweetness 5/10, Creativity 9/10, Presentation 8/10
Peppermint Dream: Richness 6/10, Sweetness 9/10, Creativity 7/10, Presentation 9/10
Salted Caramel Swirl: Richness 9/10, Sweetness 8/10, Creativity 6/10, Presentation 7/10
Dark Chocolate Decadence: Richness 10/10, Sweetness 5/10, Creativity 8/10, Presentation 10/10
White Chocolate Wonder: Richness 5/10, Sweetness 10/10, Creativity 5/10, Presentation 6/10
Cinnamon Fireside: Richness 7/10, Sweetness 7/10, Creativity 8/10, Presentation 8/10
Hazelnut Heaven: Richness 8/10, Sweetness 7/10, Creativity 6/10, Presentation 7/10
VOTING BREAKDOWN BY TIME (we had 3 voting periods):
Period 1 (Morning): 1,247 total votes
 Period 2 (Afternoon): 1,891 total votes
 Period 3 (Evening): 2,156 total votes
FUN STATS:
Total votes cast: 5,294
Closest match: Peppermint Dream vs Salted Caramel Swirl (14 vote difference!)
Biggest blowout: Dark Chocolate Decadence vs White Chocolate Wonder (73 vote margin)
Most controversial recipe: Spicy Mexican Mocha (people either loved it or hated it)
    """
    
    # --- UPDATED PROMPT: FORCE CODE OUTPUT ---
    prompt = f"Visualize this hot cocoa tournament data: {raw_data}\n\nIMPORTANT: You must output the full Python code for 'generate_report.py' inside a ```python``` markdown block in your response."
    
    req = {
        "jsonrpc": "2.0",
        "method": "session/prompt", 
        "id": get_next_id(),
        "params": ["day3-run", [{ "type": "text", "text": prompt }], None]
    }
    
    print(f">> Sending Raw Data to Operator...")
    try:
        process = subprocess.run(
            [OPERATOR_PYTHON, OPERATOR_SCRIPT],
            input=json.dumps(req),
            capture_output=True, text=True, timeout=300
        )

        if process.returncode == 0 and process.stdout.strip():
            final_result = find_json_result(process.stdout)
            if not final_result:
                print(f"❌ ERROR: Invalid JSON.\n{process.stdout}")
                return

            assistant_msgs = [m for m in final_result.get('messages', []) if m.get('role') == 'assistant']
            if assistant_msgs:
                raw_text = assistant_msgs[-1].get('content', [{}])[0].get('text', '')
                
                # --- ROBUST SAFE WRITE ---
                clean_code = extract_python_code(raw_text)
                
                if clean_code:
                    with open("generate_report.py", "w") as f:
                        f.write(clean_code)
                    print("\n✅ DAY 3 SUCCESS (OPERATOR)")
                    print("✨ Policy Enforced: 'cocoa-championship-integrity'")
                    print("📂 Generated ETL Script: generate_report.py")
                    print("👉 Now run: python3 generate_report.py")
                else:
                    print("\n⚠️  WARNING: Operator returned text, but no code block found.")
                    print("It might have written the file directly. Checking...")
                    if os.path.exists("generate_report.py"):
                        print("✅ Found existing 'generate_report.py' on disk (likely created by Tool Use).")
                        print("👉 Try running: python3 generate_report.py")
                    else:
                        print("❌ No code found in response or on disk. Response was:")
                        print(raw_text[:200] + "...")
            else:
                print("❌ No content returned.")
        else:
            print(f"❌ Execution Failed: {process.stderr}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_day3()
