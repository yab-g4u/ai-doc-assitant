import os
import requests
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def generate_gemini_response(prompt: str) -> str:
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": API_KEY
    }
    body = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    response = requests.post(GEMINI_URL, headers=headers, json=body)
    if response.status_code == 200:
        content = response.json()
        try:
            return content["candidates"][0]["content"]["parts"][0]["text"]
        except:
            return "Gemini response formatting error."
    else:
        return f"Gemini API Error: {response.status_code}"
