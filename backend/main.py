from fastapi import FastAPI, HTTPException
from groq_api import generate_sql
from db import execute_sql
from pydantic import BaseModel

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

@app.get("/")
def root():
    return {"message": "University chatbot is running!"}

def convert_to_nlp_response(question: str, sql_result):
    if not sql_result:
        return "Sorry, I couldn't find any data related to your question."

    question_lower = question.lower()

    # Office location queries
    if "office" in question_lower:
        if "where" in question_lower or "location" in question_lower:
            row = sql_result[0]
            floor = row.get("Office_Floor", "")
            block = row.get("Office_Block", "")
            return f"The office is on the {floor} floor of the {block} block."
        else:
            offices = [row.get("Office_Name") for row in sql_result if "Office_Name" in row]
            return "Offices found: " + ", ".join(offices)

    # Holidays
    if "holiday" in question_lower or "festival" in question_lower:
        events = [row.get("Event") for row in sql_result if row.get("Event")]
        if not events:
            return "No holidays found for the given criteria."
        return "The holiday(s) are: " + ", ".join(events)

    # Mentor-related queries
    if "mentor" in question_lower:
        mentors = [row.get("Mentor_Name") for row in sql_result if row.get("Mentor_Name")]
        if mentors:
            return "The mentor(s) is/are: " + ", ".join(mentors)
        return str(sql_result)

    # Dean or authority queries
    if "dean" in question_lower or "authority" in question_lower:
        if "email" in question_lower or "mail" in question_lower:
            email = sql_result[0].get("Authority_Email")
            return f"The Dean's email is {email}." if email else "No email found."
        name = sql_result[0].get("Authority_Name")
        return f"The Dean is {name}." if name else str(sql_result)

    # Lab or classroom location queries
    if "lab" in question_lower or "class" in question_lower:
        response_parts = []
        for row in sql_result:
            room = row.get("Class_Room_Number")
            lab = row.get("Class_Lab_Number")
            if room or lab:
                part = f"{room}"
                if lab:
                    part += f" - Lab No: {lab}"
                response_parts.append(part)
        return "; ".join(response_parts) if response_parts else str(sql_result)

    # Generic location queries
    if any(term in question_lower for term in ["room", "floor", "block", "where"]):
        row = sql_result[0]
        floor = row.get("Class_Floor", "") or row.get("Office_Floor", "")
        block = row.get("Class_Block", "") or row.get("Office_Block", "")
        if floor or block:
            return f"The location is on the {floor} floor of the {block} block."
        return str(sql_result)

    # Fallback
    return str(sql_result)

@app.post("/ask")
def ask_question(request: QuestionRequest):
    question = request.question
    print("Received question:", question)
    sql = generate_sql(question)
    print("Generated SQL:", sql)
    try:
        if not sql.lower().startswith("select"):
            raise HTTPException(status_code=400, detail=f"Invalid query generated: {sql}")
        result = execute_sql(sql)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    print("SQL Result:", result)
    answer = convert_to_nlp_response(question, result)
    return {
        "sql_generated": sql,
        "answer": answer
    }











# from fastapi import FastAPI, HTTPException
# from groq_api import generate_sql
# from db import execute_sql
# from pydantic import BaseModel

# app = FastAPI()

# class QuestionRequest(BaseModel):
#     question: str


# @app.get("/")
# def root():
#     return {"message": "University chatbot is running!"}

# def convert_to_nlp_response(question: str, sql_result):
#     """
#     Converts the SQL result (list of dicts) into a natural language response.
#     """
#     if not sql_result:
#         return "Sorry, I couldn't find any data related to your question."

#     question_lower = question.lower()

#     # Handle office location queries first
#     if "office" in question_lower:
#         # Return the floor/block info or office names
#         if "where" in question_lower or "location" in question_lower:
#             # Example: "Where is the Admission office?"
#             row = sql_result[0]
#             floor = row.get("Floor", "")
#             block = row.get("Block", "")
#             return f"The office is on the {floor} floor of the {block} block."
#         else:
#             # Listing offices
#             offices = [row.get("Name") for row in sql_result if "Name" in row]
#             return "Offices found: " + ", ".join(offices)

#     # Handle holidays
#     if "holiday" in question_lower or "festival" in question_lower:
#         events = [row.get("Event") for row in sql_result if row.get("Event")]
#         if not events:
#             return "No holidays found for the given criteria."
#         return "The holiday(s) are: " + ", ".join(events)

#     # Class mentor queries
#     if "mentor" in question_lower:
#         mentors = [row.get("Name") for row in sql_result if row.get("Name")]
#         if mentors:
#             return "The mentor(s) is/are: " + ", ".join(mentors)
#         return str(sql_result)

#     # Dean queries (name or email)
#     if "dean" in question_lower:
#         # If asking specifically for email
#         if "email" in question_lower or "mail" in question_lower:
#             email = sql_result[0].get("Email")
#             return f"The Dean's email is {email}." if email else "No email found."
#         # Otherwise give name
#         name = sql_result[0].get("Name")
#         return f"The Dean is {name}." if name else str(sql_result)

#     # Lab queries (room and lab number)
#     if "lab" in question_lower:
#         response_parts = []
#         for row in sql_result:
#             room = row.get("Room_Number")
#             lab = row.get("Lab_Number")
#             if room or lab:
#                 part = f"{room}"
#                 if lab:
#                     part += f" - Lab No: {lab}"
#                 response_parts.append(part)
#         return "; ".join(response_parts) if response_parts else str(sql_result)

#     # Generic location queries (rooms, floor, block)
#     if any(term in question_lower for term in ["room", "floor", "block", "where"]):
#         row = sql_result[0]
#         floor = row.get("Floor", "")
#         block = row.get("Block", "")
#         # If it's a room-to-location query, mention the block and floor
#         if floor or block:
#             return f"The location is on the {floor} floor of the {block} block."
#         return str(sql_result)

#     # Fallback: just show raw data
#     return str(sql_result)

# @app.post("/ask")
# def ask_question(request: QuestionRequest):
#     question = request.question
#     print("Received question:", question)
#     sql = generate_sql(question)
#     print("Generated SQL:", sql)
#     try:
#         if not sql.lower().startswith("select"):
#             raise HTTPException(status_code=400, detail=f"Invalid query generated: {sql}")

#         result = execute_sql(sql)
#     except Exception as e:
#         # Return an HTTP 500 if SQL execution failed
#         raise HTTPException(status_code=500, detail=f"Database error: {e}")
#     print("SQL Result:", result)
#     answer = convert_to_nlp_response(question, result)
#     return {
#         "sql_generated": sql,
#         "answer": answer
#     }











# # from fastapi import FastAPI, HTTPException
# # from groq_api import generate_sql
# # from db import execute_sql
# # from pydantic import BaseModel

# # class QuestionRequest(BaseModel):
# #     question: str

# # app = FastAPI()

# # @app.get("/")
# # def root():
# #     return {"message": "University chatbot is running!"}


# # def convert_to_nlp_response(question: str, sql_result) :
# #     """
# #     Converts the SQL result into a natural language response based on the type of question asked.
# #     """
# #     if not sql_result or len(sql_result) == 0:
# #         return "Sorry, I couldn't find any data related to your question."
    
# #     question_lower = question.lower()


# #     # Flatten result if it's a single row/single column
# #     if isinstance(sql_result, list):
# #         if len(sql_result) == 1 and isinstance(sql_result[0], dict) and len(sql_result[0]) == 1:
# #             return list(sql_result[0].values())[0]
    
# #     question_lower = question.lower()

# #     # Handle holidays
# #     if "holiday" in question_lower or "festival" in question_lower:
# #         events = [row.get("Event") or row.get("holiday_name") for row in sql_result if row]
# #         if not events:
# #             return "No holidays found for the given date."
# #         return "The holiday(s) are: " + ", ".join(events)

# #     # Class mentor queries
# #     if "mentor" in question_lower:
# #         mentors = [row.get("Name") for row in sql_result if "Name" in row]
# #         return "The mentor is: " + ", ".join(mentors)

# #     # Dean queries
# #     if "dean" in question_lower:
# #         for row in sql_result:
# #             if "Name" in row:
# #                 return f"The Dean is {row['Name']}."
# #             if "Email" in row:
# #                 return f"The Dean's email is {row['Email']}."

# #     # Room/floor/block queries
# #     if "room" in question_lower or "block" in question_lower or "floor" in question_lower or "where" in question_lower:
# #         for row in sql_result:
# #             floor = row.get("Floor", "")
# #             block = row.get("Block", "")
# #             return f"The location is on the {floor} floor of the {block} block."

# #     # Office queries
# #     if "office" in question_lower:
# #         offices = [row.get("Name") for row in sql_result if "Name" in row]
# #         return "Offices found: " + ", ".join(offices)

# #     # Lab and room queries
# #     if "lab" in question_lower:
# #         response = []
# #         for row in sql_result:
# #             room = row.get("Room_Number", "")
# #             lab = row.get("Lab_Number", "")
# #             response.append(f"{room} - Lab No: {lab}")
# #         return "; ".join(response)

# #     # Fallback
# #     return str(sql_result)


# # @app.post("/ask")
# # def ask_question(request: QuestionRequest):
# #     try:
# #         question = request.question
# #         print("Received question:", question)
# #         sql = get_sql_query(question)
# #         print("Generated SQL:", sql)
# #         result = execute_sql(sql)
# #         print("SQL Result:", result)
# #         answer = convert_to_nlp_response(question, result)
# #         return {
# #             "sql_generated": sql,
# #             "answer": answer
# #         }
# #     except Exception as e:
# #         print("Error occurred:", e)
# #         raise HTTPException(status_code=500, detail=str(e))
    

# # # @app.post("/ask")
# # # def ask_question(question: str):
# # #     try:
# # #         sql = get_sql_query(question)
# # #         result = execute_sql(sql)
# # #         return {
# # #             "sql_generated": sql,
# # #             "answer": result
# # #         }
# # #     except Exception as e:
# # #         raise HTTPException(status_code=500, detail=str(e))
