import requests

while True:
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

    if cond == "s":
        target_id = int(input())
        url = f'http://127.0.0.1:5000/api/submit_form/{target_id}'

        data_to_send = {"submit": True}
        response = requests.post(url, json=data_to_send)

        print(f"Status Kodu: {response.status_code}")
        print(f"Yanıt: {response.json()}")

    if cond == "cc":
        target_id = int(input("Yorum ekleyeceğin ID: "))
        comment = input("Yorum: ")

        url = f'http://127.0.0.1:5000/api/create_comment/{target_id}'

        data_to_send = {
            "comment": comment
        }

        response = requests.post(url, json=data_to_send)

        print(f"Status Kodu: {response.status_code}")

        try:
            print("Yanıt:", response.json())
        except:
            print("Sunucu JSON formatında bir yanıt döndürmedi.")
            print("Ham yanıt:", response.text)

    if cond == "dc":
        forum_id = int(input("Forum ID: "))
        comment_id = int(input("Silinecek yorum ID: "))

        url = f"http://127.0.0.1:5000/api/delete_comment/{forum_id}/{comment_id}"

        response = requests.delete(url)

        print(f"Status Kodu: {response.status_code}")

        try:
            print(f"Yanıt: {response.json()}")
        except:
            print("Sunucu JSON döndürmedi.")
