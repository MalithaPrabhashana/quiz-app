from fastapi import APIRouter
from models.quiz import Quiz

router = APIRouter()
quiz = Quiz(title="Student Quiz")


@router.get("/ask-question/{index}")
def ask_question(index: int):
    if index < 0 or index >= len(quiz.questions):
        return {"message": "Invalid question index!"}
    question = quiz.questions[index]
    return {"question": question.get_formatted_question()}

@router.post("/submit-answer/{index}")
def submit_answer(index: int, answer):
    if index < 0 or index >= len(quiz.questions):
        return {"message": "Invalid question index!"}
    question = quiz.questions[index]
    correct = question.check_answer(answer)
    return {"correct": correct, "message": "Answer checked!"}

@router.get("/all-questions")
def get_all_questions():
    all_questions = []

    for index, question in enumerate(quiz.questions):
        all_questions.append({
            "index": index,
            "question": question.get_formatted_question(),
            "options": question.options
        })
    return {"questions": all_questions}
