import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "model": "mistral-saba-24b",
    "messages": [
        {"role": "system", "content": "Say hello"},
        {"role": "user", "content": "Hi"}
    ]
}

response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)

print("Status code:", response.status_code)
print("Response:")
print(response.json())
