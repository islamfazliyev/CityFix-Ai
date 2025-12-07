import os
from google import genai
from PIL import Image
from dotenv import load_dotenv

# 1. Configuration (Client automatically picks up API key from environment variables)
# Make sure your API key is set in your environment (e.g., GEMINI_API_KEY)
load_dotenv(dotenv_path="../config/.env")

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)
# Choose a multimodal model like gemini-2.5-flash
MODEL_NAME = "gemini-2.5-flash"

# --- Assuming you have an image file named 'sample_image.jpg' in the same directory ---

# 2. Load the Image using PIL
try:

    img = Image.open("sample3.png") 
except FileNotFoundError:
    print("Error: 'sample_image.jpg' not found. Please provide an image file.")
    exit()

# 3. Define the prompt
prompt = "fotoğrafa baktığında gördüğün şeyleri çok uzatmadan bir tag olarak yaz, tag ikonu # olacak"

# 4. Send the Multimodal Request
print("Sending request to Gemini...")
response = client.models.generate_content(
    model=MODEL_NAME,
    contents=[prompt, img]  # Pass both the text prompt and the PIL Image object
)

# 5. Print the response
print("\n--- Gemini Response ---")
print(response.text)
print("-----------------------")