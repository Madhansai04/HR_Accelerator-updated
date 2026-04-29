from fastapi import FastAPI
from services.summarizer import summarize
from services.time_estimator import estimate_time
from services.quiz_generator import generate_smart_quiz
from services.tutor import teach
from services.evaluator import evaluate
from fastapi.responses import Response
from services.polly_service import text_to_speech
app = FastAPI()

@app.get("/")
def home():
    return {"message": "API is running 🚀"}

@app.post("/summary")
def get_summary(data: dict):
    return {"result": summarize(data["content"])}

@app.post("/time")
def get_time(data: dict):
    return {"result": estimate_time(data["content"])}

@app.post("/quiz")
def get_quiz(data: dict):
    return {
        "result": generate_smart_quiz(
            data["content"],
            data["summary"]
        )
    }

@app.post("/explain")
def explain(data: dict):
    return {"result": teach(data["content"])}

@app.post("/evaluate")
def eval_summary(data: dict):
    return {
        "result": evaluate(
            data["content"],
            data["user_summary"]
        )
    }
from services.quiz_evaluator import evaluate_quiz

@app.post("/evaluate-quiz")
def eval_quiz(data: dict):
    return {
        "result": evaluate_quiz(
            data["content"],
            data["quiz"],
            data["answers"]
        )
    }
@app.post("/speech")
def speech(data: dict):
    audio = text_to_speech(data["text"])
    return Response(content=audio, media_type="audio/mpeg")
@app.post("/final-quiz")
def get_final_quiz(data: dict):
    from services.quiz_generator import generate_smart_quiz
    weak_areas = data["weak_areas"]
    combined = "\n\n".join(weak_areas)
    return {"result": generate_smart_quiz(combined, combined)}