import requests
from requests_toolbelt import MultipartEncoder
import os

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
        
    if cond == "login":
        tc = input("TC: ")
        pwd = input("Şifre: ")

        url = "http://127.0.0.1:5000/api/login"
        payload = {"tc": tc, "password": pwd}

        response = requests.post(url, json=payload)

        print("Status:", response.status_code)
        print("Yanıt:", response.json())
    
    if cond == "reg":
        print("Kayıt oluşturma")

        tc = input("TC: ")
        name = input("Ad: ")
        last_name = input("Soyad: ")
        phone = input("Telefon: ")
        password = input("Şifre: ")

        url = "http://127.0.0.1:5000/api/register"

        payload = {
            "tc": tc,
            "name": name,
            "last_name": last_name,
            "phone_number": phone,
            "password": password
        }

        response = requests.post(url, json=payload)

        print(f"Status Kodu: {response.status_code}")

        try:
            print("Yanıt:", response.json())
        except:
            print("Sunucu JSON döndürmedi.")
    
    if cond == "t":
        # Get necessary inputs from the user
        target_id = input("Etiket eklenecek veri ID'si: ")
        image_path = input("Analiz edilecek resim yolu (e.g., 'test_image.jpg'): ")
        
        try:
            target_id = int(target_id)
        except ValueError:
            print("Hata: ID geçerli bir sayı olmalıdır.")
            continue

        if not os.path.exists(image_path):
            print(f"Hata: Belirtilen resim yolu bulunamadı: {image_path}")
            continue

        url = 'http://127.0.0.1:5000/api/txt2tag'
        
        # Prepare the request payload as multipart/form-data
        # This is necessary when sending both form fields (ID) and a file (image)
        try:
            m = MultipartEncoder(
                fields={
                    # 'id' is sent as form data (plain text)
                    'id': str(target_id), 
                    # 'image' is sent as a file object
                    'image': (os.path.basename(image_path), open(image_path, 'rb'), 'image/jpeg') 
                    # NOTE: 'image/jpeg' should be adjusted based on the actual file type
                }
            )

            response = requests.post(url, data=m, headers={'Content-Type': m.content_type})

            print(f"Status Kodu: {response.status_code}")
            
            try:
                print("Yanıt:", response.json())
            except requests.exceptions.JSONDecodeError:
                print("Sunucu JSON formatında bir yanıt döndürmedi.")
                print("Ham yanıt:", response.text)

        except FileNotFoundError:
            print(f"Hata: Resim dosyası okunamadı: {image_path}")
        except Exception as e:
            print(f"İstek gönderilirken bir hata oluştu: {e}")


