from fastapi import FastAPI, HTTPException
from groq_api import get_sql_query
from db import execute_sql

app = FastAPI()

@app.get("/")
def root():
    return {"message": "University chatbot is running!"}


@app.post("/ask")
def ask_question(question: str):
    try:
        print("Received question:", question)  # Debug
        sql = get_sql_query(question)
        print("Generated SQL:", sql)  # Debug
        result = execute_sql(sql)
        print("SQL Result:", result)  # Debug
        return {
            "sql_generated": sql,
            "answer": result
        }
    except Exception as e:
        print("Error occurred:", e)  # Debug
        raise HTTPException(status_code=500, detail=str(e))

# @app.post("/ask")
# def ask_question(question: str):
#     try:
#         sql = get_sql_query(question)
#         result = execute_sql(sql)
#         return {
#             "sql_generated": sql,
#             "answer": result
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
