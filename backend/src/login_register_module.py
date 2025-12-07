import json
import flask_sqlalchemy
import random

data = f"./data/accounts.json"

def login(tc, password):
    with open(data, "r") as f:
        d = json.load(f)

    if not isinstance(d, list):
        return False
    

    for user in d:
        if user.get("tc") == tc:
            if user.get("password") == password:
                return {"status": "success", "user": user}
            else:
                return {"status": "wrong_password"}

    return {"status": "user_not_found"}

            

def register(tc, name, last_name, phone_number, password):
    with open(data, "r") as f:
        d = json.load(f)
    
    if not isinstance(d, list):
        return False
    
    for user in d:
        if user.get("tc") == tc:
            return "tc_exists"
        if user.get("phone_number") == phone_number:
            return "phone_exists"
    
    d.append({
        "id": random.randint(1, 100000),
        "tc": tc,
        "name": name,
        "last_name": last_name,
        "phone_number": phone_number,
        "password": password
    })
    
    with open(data, "w") as f:
        json.dump(d, f, indent=4, ensure_ascii=False)
    
    return True
    
    