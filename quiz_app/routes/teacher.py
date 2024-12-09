from fastapi import APIRouter
from database import Database
from models.question import Question

router = APIRouter()

db = Database()

@router.post("/add-question")
def add_question(question: dict):
    new_question = Question(**question)
    db.add_question(new_question)
    return {"message": "Question added successfully!"}