import json
import random
import os

data = f"./data/data.json"

def create_form(image_filename, topic, description, tags):
    current_data = []
    try:
        with open(data, "r", encoding="utf-8") as f:
            current_data = json.load(f)
            if not isinstance(current_data, list):
                current_data = []
    except (FileNotFoundError, json.JSONDecodeError):
        current_data = []

    rand_id = random.randint(1,100000)
    existing_ids = {item["id"] for item in current_data}
    while rand_id in existing_ids:
        rand_id = random.randint(1,100000)
    
    new_entry = {
        "id": rand_id,
        "image": image_filename,
        "topic": topic, 
        "description": description, 
        "tags": tags,
        "comments": [],
        "submit": False
    }

    current_data.append(new_entry)
    
    try:
        with open(data, "w", encoding="utf-8") as f:
            json.dump(current_data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"JSON yazma hatası: {e}")
        return False

    return rand_id

    return rand_id

def submit_form(id):
    with open(data, "r", encoding="UTF-8") as f:
        s = json.load(f)
    
    if isinstance(s, list):
        found = False
        for item in s:
            if item.get("id") == id:
                item["submit"] = True
                found = True
                break
        if not found: return False
    else:
        return False
    
    with open(data, "w", encoding="UTF-8") as f:
        json.dump(s, f, indent=4, ensure_ascii=False)
    
    return True

def get_form():
    try:
        with open(data, "r", encoding="UTF-8") as f:
            d = json.load(f)
            return d
    except FileNotFoundError:
        return []

def delete_form(form, id):
    form[:] = [item for item in form if item.get("id") != id]

    with open(data, "w", encoding="UTF-8") as f:
        json.dump(form, f, indent=4, ensure_ascii=False)