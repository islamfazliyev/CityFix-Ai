import json
import flask_sqlalchemy
import random

data = f"./data/data.json"


def create_comment(text, id):
    with open(data, "r") as f:
        d = json.load(f)
    
    if isinstance(d, list):
        for item in d:
            if item.get("id") == id:
                item.setdefault("comments", [])
                new_comment_id = random.randint(1,100000)
                existing_ids = {c["id"] for c in item["comments"]}
                while new_comment_id in existing_ids:
                    new_comment = random.randint(1,100000)

                new_comment = {
                    "id": new_comment_id,
                    "text": text
                }

                item["comments"].append(new_comment)
                break
        else:
            return False
    else:
        return False
    
    with open(data, "w") as f:
        json.dump(d, f, indent=4, ensure_ascii=False)
    
    return True

def delete_comment(forum_id, comment_id):
    with open(data, "r") as f:
        d = json.load(f)

    if not isinstance(d, list):
        return False

    for item in d:
        if item.get("id") == forum_id:

            comments = item.setdefault("comments", [])

            new_comments = [c for c in comments if c.get("id") != comment_id]

            if len(new_comments) == len(comments):
                return False  

            item["comments"] = new_comments

            with open(data, "w") as f:
                json.dump(d, f, indent=4, ensure_ascii=False)

            return True

    return False