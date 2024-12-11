from fastapi import APIRouter
from models.quiz import Quiz
from pydantic import BaseModel

router = APIRouter()
quiz = Quiz(title="Student Quiz")
quiz.load_questions()


class AnswerRequest(BaseModel):
    id: int
    answer: int


@router.get("/ask-question/{index}")
def ask_question(index: int):

    if index < 0 or index >= len(quiz.questions):
        return {"message": "Invalid question index!"}
    question = quiz.questions[index]
    return {"question": question.get_formatted_question()}


@router.post("/submit-answer")
def submit_answer(request: AnswerRequest):
    target_question = {}

    # Find the target question by matching the ID
    for question in quiz.questions:
        if int(question.id) == int(request.id):
            target_question = {
                "id": question.id,
                "question": question.get_formatted_question(),
                "options": question.options,
                "correct_answer": question.correct_answer
            }
            break  # Exit loop once the question is found
 
    # If no question found
    if not target_question:
        return {"message": "Invalid question id!"}

    # Check if the answer is correct
    correct = question.check_answer(request.answer)

    return {
        "correct": correct,
        "message": "Answer checked!"
    }



@router.get("/all-questions")
def get_all_questions():
    all_questions = []

    for index, question in enumerate(quiz.questions):
        all_questions.append({
            "id": question.id,
            "question": question.get_formatted_question(),
            "options": question.options,
            "correct_answer": question.correct_answer
        })

    return {"questions": all_questions}
