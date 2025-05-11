from fastapi import FastAPI, HTTPException
from groq_api import generate_sql_from_question, generate_nl_summary_from_sql_result
from db import execute_sql

app = FastAPI()

@app.get("/")
def root():
    return {"message": "University chatbot is running!"}


@app.post("/ask")
def ask_question(question: str):
    try:
        print("Received question:", question)  # Debug
        sql = generate_sql_from_question(question)
        print("Generated SQL:", sql)  # Debug
        result = execute_sql(sql)
        print("SQL Result:", result)  # Debug
        summary = generate_nl_summary_from_sql_result(result)
        print("Generated Summary:", summary)
        
        return {
            "sql_generated": sql,
            "sql_result": result,
            "summary": summary
        }
        #return summary
    except Exception as e:
        print("Error occurred:", e)  # Debug
        raise HTTPException(status_code=500, detail=str(e))
    

# def convert_to_nlp_response(question: str, sql_result) -> str:
#     """
#     Converts the SQL result into a natural language response based on the type of question asked.
#     """
#     if not sql_result or len(sql_result) == 0:
#         return "Sorry, I couldn't find any data related to your question."

#     # Flatten result if it's a single row/single column
#     if isinstance(sql_result, list):
#         if len(sql_result) == 1 and isinstance(sql_result[0], dict) and len(sql_result[0]) == 1:
#             return list(sql_result[0].values())[0]
    
#     question_lower = question.lower()

#     # Handle holidays
#     if "holiday" in question_lower or "festival" in question_lower:
#         events = [row.get("Event")  for row in sql_result if row]
#         if not events:
#             return "No holidays found for the given date."
#         return "The holiday(s) are: " + ", ".join(events)

#     # Class mentor queries
#     if "mentor" in question_lower:
#         mentors = [row.get("Mentor_Name") for row in sql_result if "Mentor_Name" in row]
#         return "The mentor is: " + ", ".join(mentors)

#     # Dean queries
#     if "dean" in question_lower:
#         for row in sql_result:
#             if "Name" in row:
#                 return f"The Dean is {row['Authority_Name']}."
#             if "Email" in row:
#                 return f"The Dean's email is {row['Authority_Email']}."

#     # Room/floor/block queries
#     if "room" in question_lower or "block" in question_lower or "floor" in question_lower or "where" in question_lower:
#         for row in sql_result:
#             floor = row.get("Class_Floor", "")
#             block = row.get("Class_Block", "")
#             return (f"The location is on the {floor} floor of the {block} block.")

#     # Office queries
#     if "office" in question_lower:
#         offices = [row.get("Office_Name") for row in sql_result if "Office_Name" in row]
#         return "Offices found: " + ", ".join(offices)

#     # Lab and room queries
#     if "lab" in question_lower:
#         response = []
#         for row in sql_result:
#             room = row.get("Class_Room_Number", "")
#             lab = row.get("Class_Lab_Number", "")
#             response.append(f"{room} - Lab No: {lab}")
#         return "; ".join(response)

#     # Fallback
#     return str(sql_result)

# # @app.post("/ask")
# # def ask_question(question: str):
# #     try:
# #         sql = get_sql_query(question)
# #         result = execute_sql(sql)
# #         return {
# #             "sql_generated": sql,
# #             "answer": result
# #         }
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=str(e))
