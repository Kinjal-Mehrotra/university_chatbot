import requests
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "mistral-saba-24b"

UNIVERSITY_SCHEMA = """
1. authority_members (Authority_ID, Authority_Name, Authority_Designation, Authority_Department, Authority_Email, Authority_Phone_Number, Authority_Room_Number)
2. class_mentors (Mentor_ID, Mentor_Name, Mentor_Year, Mentor_Branch, Mentor_Section, Mentor_Room_Number, Mentor_Phone_Number)
3. holidays (Event, Date, Day)
4. locations (Class_Room_Number, Class_Floor, Class_Block, Class_Lab_Number)
5. offices (Office_Name, Office_Floor, Office_Block)
"""

EXAMPLE_QA = """
Q. Who is the dean of School of Computer Applications?
A. SELECT Authority_Name FROM authority_members WHERE Authority_Designation = 'Dean' AND Authority_Department = 'School of Computer Applications';

Q. What is the email ID of the dean of School of Computer Applications?
A. SELECT Authority_Email FROM authority_members WHERE Authority_Designation = 'Dean' AND Authority_Department = 'School of Computer Applications';

Q. Which holidays will come in May this year?
A. SELECT * FROM holidays WHERE MONTH(Date) = 5 AND YEAR(Date) = YEAR(CURDATE());

Q. Which holidays will come in this month?
A. SELECT * FROM holidays WHERE MONTH(Date) = MONTH(CURDATE()) AND YEAR(Date) = YEAR(CURDATE());

Q. Which holidays will come in October 2014?
A. SELECT CASE WHEN 2014 != YEAR(CURDATE()) THEN 'Holiday data is available only for the current year.' ELSE (SELECT GROUP_CONCAT(Event SEPARATOR '/') FROM holidays WHERE MONTH(Date) = 10 AND YEAR(Date) = 2014) END AS result;

Q. On which day is Ram Navami?
A. SELECT Day FROM holidays WHERE Event LIKE '%Ram Navami%' AND YEAR(Date) = YEAR(CURDATE());

Q. Which festival is on 19th April this year?
A. SELECT IFNULL((SELECT Event FROM holidays WHERE MONTH(Date) = 4 AND DAY(Date) = 19 AND YEAR(Date) = YEAR(CURDATE()) LIMIT 1), 'No holidays found for this date.') AS Event;

Q. Show details of the class mentor Mahesh Kumar Joshi.
A. SELECT * FROM class_mentors WHERE Mentor_Name LIKE '%Mahesh Kumar Joshi%';

Q. Who is the mentor of section O?
A. SELECT Mentor_Name FROM class_mentors WHERE Mentor_Section = 'O';

Q. Where is the seating of Mahesh sir?
A. SELECT Mentor_Room_Number FROM class_mentors WHERE Mentor_Name LIKE '%Mahesh%';

Q. Mahesh sir is the mentor of which year?
A. SELECT Mentor_Year FROM class_mentors WHERE Mentor_Name LIKE '%Mahesh%';

Q. Where is VIB-410?
A. SELECT Class_Floor, Class_Block FROM locations WHERE Class_Room_Number = 'VIB-410';

Q. Provide all the room numbers and lab numbers available on the third floor of Engineering block.
A. SELECT Class_Room_Number, Class_Lab_Number FROM locations WHERE Class_Floor = 'Third' AND Class_Block = 'Engineering';

Q. Where is the admission office?
A. SELECT Office_Floor, Office_Block FROM offices WHERE Office_Name LIKE '%Admission%';

Q. Which offices are present on Engineering block first floor?
A. SELECT Office_Name FROM offices WHERE Office_Floor = 'First' AND Office_Block = 'Engineering';

Q. Which holiday is on 15th August?
A. SELECT Event FROM holidays WHERE DAY(Date) = 15 AND MONTH(Date) = 8 AND YEAR(Date) = YEAR(CURDATE());

Q. List all upcoming holidays.
A. SELECT Event, Date FROM holidays WHERE Date >= CURDATE() ORDER BY Date;

Q. Which holiday falls on a Friday in October?
A. SELECT Event FROM holidays WHERE MONTH(Date) = 10 AND DAYNAME(Date) = 'Friday';

Q. Show the room numbers on second floor of Science block.
A. SELECT Class_Room_Number FROM locations WHERE Class_Floor = 'Second' AND Class_Block = 'Science';

Q. In which block and room number is Lab 10?
A. SELECT Class_Room_Number, Class_Block FROM locations WHERE Class_Lab_Number = 10;
"""

def generate_sql(question: str) -> str:
    prompt = f"""
    You are a MySQL expert assistant. Given the following university database schema:

    {UNIVERSITY_SCHEMA}

    Examples of question-to-SQL conversions:
    {EXAMPLE_QA}

    Now write a syntactically correct SQL query to answer:
    "{question}"

    Only return the SQL query (no explanations).
    """

    data = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are a MySQL query generator for a university chatbot. Based on the database schema and examples provided, generate a valid SQL query for the user’s question. Only return SQL — no explanations or comments."
            },
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
        sql_query = response.json()["choices"][0]["message"]["content"].strip()

        if not sql_query.lower().startswith("select"):
            raise ValueError("Generated query is not a SELECT statement.")

        return sql_query

    except Exception as e:
        return f"Error: {e}"
