from dotenv import load_dotenv
import os, requests

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Use your actual schema + example block
prompt = """
You are a MySQL expert assistant. Given the following schema:

1. holidays (Event, Date, Day)

Q. Which holidays will come in May this year?
A. SELECT * FROM holidays WHERE MONTH(Date) = 5 AND YEAR(Date) = YEAR(CURDATE());

Now write a SQL query for:
"Which holidays are in October this year?"
Only return the SQL.
"""

payload = {
    "model": "mistral-saba-24b",
    "messages": [
        {"role": "system", "content": "You are a MySQL query generator. Only return SQL."},
        {"role": "user", "content": prompt}
    ]
}

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
print(response.status_code)
print(response.json()['choices'][0]['message']['content'])





# import requests
# import os
# from dotenv import load_dotenv

# load_dotenv()

# api_key = os.getenv("GROQ_API_KEY")

# headers = {
#     "Authorization": f"Bearer {api_key}",
#     "Content-Type": "application/json"
# }

# payload = {
#     "model": "mistral-saba-24b",
#     "messages": [
#         {"role": "system", "content": "Hello user."},
#         {"role": "user", "content": "Hi"}
#     ]
# }

# response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)

# print("Status code:", response.status_code)
# print("Response:")
# print(response.json())
