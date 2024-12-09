from fastapi import APIRouter
from database import Database

router = APIRouter()

db = Database()

@router.get("/get-questions")
def get_questions():
    return db.get_all_questions()


@router.post("/submit-answer")
def submit_answer(question_id: int, answer):
    question = db.get_question_by_id(question_id)
    if not question:
        return {"message": "Question not found!"}

    correct = question.correct_answer == answer
    return {"correct": correct, "message": "Answer checked!"}