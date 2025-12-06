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
        "tags": tags
    })
    with open(data, "w") as f:
        json.dump(form, f, indent=4, ensure_ascii=False)


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