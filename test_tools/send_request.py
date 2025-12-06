import requests

cond = input()

if cond == "d":
    delete_id = int(input())
    url = f'http://127.0.0.1:5000/api/delete_form/{delete_id}'
    data_to_delete = {"id": delete_id}
    response = requests.delete(url, json=data_to_delete)

    print(f"Status Kodu: {response.status_code}")
    print(response.text)
if cond == "p":
    url = 'http://127.0.0.1:5000/api/create_form/'
    data_to_send = {
        "id": 12,
        "topic": "test", 
        "desc": "yeni veri", 
        "tags": ["python"] 
    }



    response = requests.post(url, json=data_to_send)

    print(f"Status Kodu: {response.status_code}")
    print(f"Yanıt: {response.json()}")
