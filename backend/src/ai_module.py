import os
from google import genai
from PIL import Image
import json
from dotenv import load_dotenv

load_dotenv(dotenv_path="./config/.env")
data = f"./data/data.json"
API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)
MODEL_NAME = "gemini-2.5-flash"

def img2tag(image_path):
    try:
        img = Image.open(image_path) 
    except FileNotFoundError:
        print("Error: " + image_path + "not found. Please provide an image file.")
        exit()
    
    prompt = "fotoğrafa baktığında gördüğün şeyleri çok uzatmadan bir tag olarak yaz, tag ikonu # olacak. yatay şekilde yaz"

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[prompt, img]
    )

    return response.text.strip()

def add_ai_tags_to_data(item_id: int, image_path: str):
    ai_tags_string = img2tag(image_path)
    ai_tags = [tag.strip("#") for tag in ai_tags_string.split() if tag.startswith("#")]

    try:
        with open(data, 'r', encoding='utf-8') as f:
            d = json.load(f)
        if not isinstance(d, list):
            print("Error: JSON file structure is not a list. Cannot search by ID.")
            return

        found = False
        for item in d:
            if item.get("id") == item_id:
                existing_tags = set(item.get("tags", []))
                combined_tags = list(existing_tags.union(ai_tags))
                
                item["tags"] = combined_tags
                found = True
                print(f"2. Successfully updated tags for item ID {item_id}.")
                break

        if not found:
            print(f"Error: Item with ID {item_id} not found in data.")
            return

        with open(data, 'w', encoding='utf-8') as f:
            json.dump(d, f, indent=4, ensure_ascii=False)
        
        print(f"3. Data saved successfully to {data}.")
    except FileNotFoundError:
        print(f"Error: Data file not found at {data}")
        return
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from {data}")
        return

