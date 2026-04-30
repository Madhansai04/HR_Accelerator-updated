from fastapi import FastAPI
from fastapi.responses import Response
from services.summarizer import summarize
from services.time_estimator import estimate_time
from services.evaluator import evaluate
from services.quiz_evaluator import evaluate_quiz
from services.quiz_generator import generate_smart_quiz
from services.polly_service import text_to_speech

app = FastAPI()

@app.get("/")
def home():
    return {"message": "HR Accelerator API running"}

@app.post("/summary")
def get_summary(data: dict):
    return {"result": summarize(data["content"])}

@app.post("/time")
def get_time(data: dict):
    return {"result": estimate_time(data["content"])}

@app.post("/speech")
def speech(data: dict):
    audio = text_to_speech(data["text"])
    return Response(content=audio, media_type="audio/mpeg")

@app.post("/evaluate")
def eval_summary(data: dict):
    return {"result": evaluate(data["content"], data["user_summary"])}

@app.post("/quiz")
def get_quiz(data: dict):
    return {"result": generate_smart_quiz(data["content"], data.get("summary", ""))}

@app.post("/evaluate-quiz")
def eval_quiz(data: dict):
    print("ANSWERS RECEIVED:", data["answers"])
    print("QUIZ:", data["quiz"])
    return {"result": evaluate_quiz(data["content"], data["quiz"], data["answers"])}

@app.post("/final-quiz")
def get_final_quiz(data: dict):
    combined = "\n\n".join(data["weak_areas"])
    return {"result": generate_smart_quiz(combined, combined)}