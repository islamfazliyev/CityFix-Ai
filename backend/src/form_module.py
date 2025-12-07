import json
import flask_sqlalchemy
import random

data = f"./data/data.json"


def create_form(topic, description, tags, form):
    rand_id = random.randint(1,100000)
    existing_ids = {item["id"] for item in form}
    while rand_id in existing_ids:
        rand_id = random.randint(1,100000)
    form.append({
        "id": rand_id, 
        "topic": topic, 
        "description": description, 
        "tags": tags,
        "comments": [],
        "submit": False
    })
    with open(data, "w") as f:
        json.dump(form, f, indent=4, ensure_ascii=False)

def submit_form(id):
    with open(data, "r") as f:
        s = json.load(f)
    
    if isinstance(s, list):
        for item in s:
            if item.get("id") == id:
                item["submit"] = True
            else:
                return False
    else:
        return False
    
    with open(data, "w") as f:
        json.dump(s, f, indent=4, ensure_ascii=False)
    
    return True

def get_form():
    with open(data, "r", encoding="UTF-8") as f:
        d = json.load(f)
        return d

def delete_form(form, id):
    updated_form_list = [item for item in form if item["id"] != id]
    form.clear()
    form.extend(updated_form_list)

    with open(data, "w", encoding="UTF-8") as f:
        json.dump(form, f, indent=4, ensure_ascii=False)