import requests
import os
from dotenv import load_dotenv

# Load environment variables from the .env file (if using one)
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "mistral-saba-24b"

# Define your actual database schema
UNIVERSITY_SCHEMA = """
Tables and their columns:

1. authority_members (ID, Name, Designation, Department, Email, Phone_Number, Room_Number)
2. class_mentors (ID, Name, Year, Branch, Section, Room_Number, Phone_Number)
3. holidays (Event, Date, Day)
4. locations (Room_Number, Floor, Block, Lab_Number)
5. offices (Name, Floor, Block)
"""

def generate_sql(question: str) -> str:

    example_ques="""
    Q. who is the dean of school of computer applications?
    A. SELECT Name FROM authority_members WHERE Designation = 'Dean' AND Department = 'School of Computer Applications';

"""
    
    prompt = f"""
You are a MySQL expert assistant. Given the following database schema:

{UNIVERSITY_SCHEMA}

Write a syntactically correct SQL query to answer the following user question:
"{question}"

Only return the SQL query.
Do not include explanations, markdown, or comments.
Use correct column and table names from the schema above.
"""

    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You generate MySQL queries for a university database based on user questions. Only return SQL."},
            {"role": "user", "content": prompt}
        ]
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content'].strip()
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
get_sql_query = generate_sql


# # backend/groq_api.py

# import os
# import requests
# from dotenv import load_dotenv

# load_dotenv()

# def get_sql_query(question):
#     system_prompt = "You are a university assistant who converts questions into MySQL queries. Only return the SQL query with no explanation."

#     payload = {
#         "messages": [
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": question}
#         ],
#         "model": "mistral-saba-24b",
#     }

#     headers = {
#         "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
#         "Content-Type": "application/json"
#     }

#     response = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers)
#     response.raise_for_status()
#     return response.json()["choices"][0]["message"]["content"]
