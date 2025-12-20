import json
try:
    with open('dmitris-sanity-saver.json', 'r') as f:
        data = json.load(f)
    print("✅ SUCCESS! Valid JSON detected.")
    print(f"Found {len(data['vendors'])} vendors.")
    print(f"First vendor: {data['vendors'][0]['name']}")
except Exception as e:
    print(f"❌ ERROR: {e}")
