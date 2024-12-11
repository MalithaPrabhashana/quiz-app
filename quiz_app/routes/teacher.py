from fastapi import APIRouter
from models.quiz import Quiz
from pydantic import BaseModel
from typing import List, Union
    
# Define Pydantic models
class QuestionData(BaseModel):
    text: str
    options: List[str]
    correct_answer: Union[int, str]

class AddQuestionRequest(BaseModel):
    question_type: str
    question_data: QuestionData

router = APIRouter()
quiz = Quiz(title="Teacher's Quiz")

@router.post("/add-question")
def add_question(request: AddQuestionRequest):
    question_type = request.question_type
    question_data = request.question_data.dict()
    quiz.add_question(question_type, question_data) 
    return {"message": "Question added successfully!"}
