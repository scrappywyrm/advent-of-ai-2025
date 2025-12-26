import json, sys, os

DB_FILE = "wishes.json"

def load_db():
    if not os.path.exists(DB_FILE): return []
    try:
        with open(DB_FILE, 'r') as f: return json.load(f)
    except: return []

def save_db(data):
    with open(DB_FILE, 'w') as f: json.dump(data, f, indent=2)

def list_wishes():
    wishes = load_db()
    if not wishes: print("The Wishbox is empty! ✨"); return
    print(json.dumps(wishes, indent=2))

def add_wish(item, category="General", priority="Hopeful"):
    wishes = load_db()
    new_wish = {
        "id": len(wishes) + 1,
        "item": item,
        "category": category,
        "priority": priority,
        "status": "pending"
    }
    wishes.append(new_wish)
    save_db(wishes)
    print(f"Wish added: {item}")

def grant_wish(item_name):
    wishes = load_db()
    found = False
    for w in wishes:
        if item_name.lower() in w["item"].lower():
            w["status"] = "granted"
            found = True
    save_db(wishes)
    if found: print(f"Wish granted: {item_name}")
    else: print(f"Wish not found: {item_name}")

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(0)
    cmd = sys.argv[1]
    if cmd == "list": list_wishes()
    elif cmd == "add": add_wish(sys.argv[2], sys.argv[3], sys.argv[4])
    elif cmd == "grant": grant_wish(sys.argv[2])
