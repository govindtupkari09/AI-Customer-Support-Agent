import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

# Read Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing in .env file")

# Initialize Gemini Client


client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options=types.HttpOptions(
        timeout=180000
    )
)

# Generate AI response
import time

def generate_answer(prompt: str):
    start_time = time.time()

    print("\n========== GEMINI DEBUG ==========")
    print("Sending request to Gemini...")

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    end_time = time.time()

    print(f"Gemini response received in {end_time - start_time:.2f} seconds")
    print("==================================")

    return response.text