import os
import json
import time
from google import genai
from PIL import Image
from dotenv import load_dotenv

# Config yükle
load_dotenv(dotenv_path="./config/.env")

# API Key Kontrolü
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("HATA: GEMINI_API_KEY bulunamadı! .env dosyanı kontrol et.")

client = genai.Client(api_key=API_KEY)
MODEL_NAME = "gemini-2.5-flash"
DATA_PATH = "./data/data.json"

def img2tag(image_path):
    print(f"--- AI Tag İşlemi Başlıyor: {image_path} ---")
    
    if not os.path.exists(image_path):
        print(f"HATA: Resim dosyası bulunamadı -> {image_path}")
        return ""

    try:
        img = Image.open(image_path)
        prompt = "fotoğrafa baktığında gördüğün şeyleri çok uzatmadan önemli ve acil olan (mesela: bozuk yol, patlamış boru gibi. manzaralar vs bunlara dahil değildir) şeyleri bir tag olarak yaz, tag ikonu # olacak. yatay şekilde yaz. Örnek: #manzara #doğa"
        
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[prompt, img]
        )
        print(f"Gemini Yanıtı: {response.text}")
        return response.text.strip()
    except Exception as e:
        print(f"HATA (Gemini API): {e}")
        return ""

def add_ai_tags_to_data(item_id: int, image_path: str):
    time.sleep(1) 

    ai_tags_string = img2tag(image_path)
    if not ai_tags_string:
        print("Uyarı: AI tag üretilemedi.")
        return

    ai_tags = [tag.strip("#, ") for tag in ai_tags_string.split() if "#" in tag or tag.strip()]

    try:
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            d = json.load(f)
        
        if not isinstance(d, list):
            print("HATA: JSON dosyası bir liste formatında değil!")
            return

        found = False
        for item in d:
            if item.get("id") == item_id:
                existing_tags = set(item.get("tags", []))
                combined_tags = list(existing_tags.union(ai_tags))
                
                item["tags"] = combined_tags
                found = True
                print(f"BAŞARILI: ID {item_id} için tagler güncellendi: {combined_tags}")
                break

        if not found:
            print(f"HATA: ID {item_id} data.json içinde bulunamadı. (Senkronizasyon sorunu olabilir)")
            return

        with open(DATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(d, f, indent=4, ensure_ascii=False)
        
        print("Data dosyası kaydedildi.")

    except FileNotFoundError:
        print(f"HATA: Data dosyası bulunamadı -> {DATA_PATH}")
    except json.JSONDecodeError:
        print(f"HATA: JSON formatı bozuk! {DATA_PATH} dosyasını kontrol et.")
    except Exception as e:
        print(f"HATA (Genel): {e}")