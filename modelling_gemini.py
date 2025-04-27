import os
import base64
import json
import random
import time
import re
import matplotlib.pyplot as plt
from PIL import Image
from tqdm import tqdm
import requests

# Read Gemini API key from environment
GEMINI_API_KEY = os.getenv('GEMINI_KEY')

if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_KEY environment variable not set!")

# Gemini API endpoint
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key=" + GEMINI_API_KEY

# Folder containing preprocessed images
preprocessed_folder = 'dohee_preprocessed'

# Output folder to save JSON responses
output_json_folder = 'output_json_gemini'
os.makedirs(output_json_folder, exist_ok=True)

# Function to encode image in base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Build strong prompt
def build_prompt():
    return (
        "You are a highly accurate medical document parser.\n"
        "Analyze the attached prescription image carefully.\n"
        "Extract the following fields into a valid JSON object:\n"
        "- Patient Name\n"
        "- Doctor Name\n"
        "- Date (format: YYYY-MM-DD if possible)\n"
        "- Medications: a list of objects, each with Name, Dosage, Frequency, Duration\n"
        "- Special Instructions\n\n"
        "Strict rules:\n"
        "- If any field is missing or unreadable, set its value to null.\n"
        "- DO NOT add any text outside the JSON object.\n"
        "- DO NOT write explanations.\n"
        "- Start your output directly with '{' and end with '}'.\n"
        "- If you understand, proceed.\n"
    )

# Function to safely extract JSON string
def extract_json_from_text(text):
    json_pattern = r'\{.*\}'
    match = re.search(json_pattern, text, re.DOTALL)
    if match:
        return match.group(0)
    return None

# Function to send image and prompt to Gemini API with retries
def process_image(image_path, max_retries=5):
    base64_image = encode_image(image_path)
    prompt = build_prompt()

    request_body = {
        "contents": [
            {
                "parts": [
                    {"text": prompt},
                    {
                        "inlineData": {
                            "mimeType": "image/jpeg",
                            "data": base64_image
                        }
                    }
                ]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    backoff = 5  # initial wait 5 seconds on failures

    for attempt in range(max_retries):
        try:
            response = requests.post(GEMINI_API_URL, headers=headers, json=request_body)
            if response.status_code == 429:
                print(f"⚠️ Too Many Requests. Waiting {backoff} seconds before retry...")
                time.sleep(backoff)
                backoff *= 2
                continue
            response.raise_for_status()

            data = response.json()
            text_response = data['candidates'][0]['content']['parts'][0]['text']
            return text_response

        except Exception as e:
            print(f"⚠️ Attempt {attempt + 1} failed for {image_path}: {e}")
            time.sleep(backoff)
            backoff *= 2

    print(f"❌ All retries failed for {image_path}. Skipping...")
    return None

# Main loop to process all images
all_images = [os.path.join(preprocessed_folder, img) for img in os.listdir(preprocessed_folder) if img.lower().endswith(('.png', '.jpg', '.jpeg'))]

successful = 0
failed = 0

for image_path in tqdm(all_images, desc="Processing images with Gemini"):
    output_text = process_image(image_path)
    if output_text:
        image_name = os.path.basename(image_path).split('.')[0]
        output_file_path = os.path.join(output_json_folder, f"{image_name}.json")
        extracted_json = extract_json_from_text(output_text)

        if extracted_json:
            try:
                json_object = json.loads(extracted_json)
                with open(output_file_path, 'w') as f:
                    json.dump(json_object, f, indent=4)
                successful += 1
            except json.JSONDecodeError:
                print(f"⚠️ JSON parse error for {image_path}, skipping save.")
                failed += 1
        else:
            print(f"⚠️ No JSON found in model output for {image_path}.")
            failed += 1
    else:
        failed += 1

    # 💤 Wait between 20 to 40 seconds after each request
    sleep_time = random.uniform(20, 40)
    print(f"⏳ Sleeping for {sleep_time:.2f} seconds before next request...")
    time.sleep(sleep_time)

print(f"\n✅ Finished. Successful: {successful}, Failed: {failed}")

