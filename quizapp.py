# Backend: FastAPI Application
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from typing import List, Optional
from pymongo import MongoClient
from bson.objectid import ObjectId

# MongoDB Connection
class Database:
    def __init__(self, uri="mongodb://localhost:27017", db_name="quiz_app"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_collection(self, collection_name):
        return self.db[collection_name]

db_instance = Database()

# Question Model
class Question(BaseModel):
    question_type: str  # e.g., "multiple_choice", "yes_no"
    question_text: str
    options: Optional[List[str]] = None  # For multiple choice questions
    correct_answer: Optional[int]  # Index of the correct answer (for MCQs) or 1/2 (for yes/no)

# Quiz Service
class QuizService:
    def __init__(self):
        self.collection = db_instance.get_collection("questions")

    def add_question(self, question_data: dict):
        result = self.collection.insert_one(question_data)
        return str(result.inserted_id)

    def get_questions(self):
        return list(self.collection.find())

    def get_question_by_id(self, question_id: str):
        return self.collection.find_one({"_id": ObjectId(question_id)})

    def validate_answer(self, question_id: str, student_answer: int):
        question = self.get_question_by_id(question_id)
        if not question:
            return False
        return question.get("correct_answer") == student_answer

quiz_service = QuizService()

# FastAPI Application
app = FastAPI()
teacher_router = APIRouter()
student_router = APIRouter()

# Teacher API
@teacher_router.post("/teacher/add-question")
def add_question(question: Question):
    question_id = quiz_service.add_question(question.dict())
    return {"message": "Question added successfully!", "question_id": question_id}

# Student API
@student_router.get("/student/get-questions")
def get_questions():
    questions = quiz_service.get_questions()
    for q in questions:
        q["_id"] = str(q["_id"])  # Convert ObjectId to string
    return questions

@student_router.post("/student/validate-answer")
def validate_answer(question_id: str, student_answer: int):
    is_correct = quiz_service.validate_answer(question_id, student_answer)
    return {"correct": is_correct}

# Register routers
app.include_router(teacher_router, prefix="/api", tags=["Teacher"])
app.include_router(student_router, prefix="/api", tags=["Student"])

@app.get("/")
def root():
    return {"message": "Welcome to the Quiz Application!"}

# Frontend: Streamlit Application
import streamlit as st

st.title("Quiz Application")
mode = st.sidebar.selectbox("Choose mode:", ["Teacher", "Student"])

if mode == "Teacher":
    st.header("Teacher Mode")
    question_type = st.selectbox("Select Question Type:", ["multiple_choice", "yes_no"])
    question_text = st.text_input("Enter Question Text:")

    if question_type == "multiple_choice":
        options = [
            st.text_input(f"Option {i + 1}") for i in range(4)
        ]
        correct_answer = st.number_input("Correct Answer Index (1-4):", min_value=1, max_value=4)
        if st.button("Add Question"):
            question = Question(
                question_type=question_type,
                question_text=question_text,
                options=options,
                correct_answer=correct_answer
            )
            response = quiz_service.add_question(question.dict())
            st.success(f"Question added successfully! ID: {response}")
    elif question_type == "yes_no":
        correct_answer = st.selectbox("Correct Answer:", ["True", "False"])
        correct_answer = 1 if correct_answer == "True" else 2
        if st.button("Add Question"):
            question = Question(
                question_type=question_type,
                question_text=question_text,
                correct_answer=correct_answer
            )
            response = quiz_service.add_question(question.dict())
            st.success(f"Question added successfully! ID: {response}")

elif mode == "Student":
    st.header("Student Mode")
    questions = quiz_service.get_questions()
    if not questions:
        st.write("No questions available.")
    else:
        for question in questions:
            st.subheader(question["question_text"])
            if question["question_type"] == "multiple_choice":
                options = question["options"]
                student_answer = st.radio(
                    "Choose an answer:",
                    options=[f"{i + 1}. {opt}" for i, opt in enumerate(options)],
                    index=0
                )
                if st.button(f"Submit Answer for {question['_id']}"):
                    is_correct = quiz_service.validate_answer(
                        question_id=question["_id"],
                        student_answer=int(student_answer.split(".")[0])
                    )
                    if is_correct:
                        st.success("Correct Answer!")
                    else:
                        st.error("Wrong Answer!")
            elif question["question_type"] == "yes_no":
                student_answer = st.radio(
                    "Choose an answer:",
                    options=["1. True", "2. False"],
                    index=0
                )
                if st.button(f"Submit Answer for {question['_id']}"):
                    is_correct = quiz_service.validate_answer(
                        question_id=question["_id"],
                        student_answer=int(student_answer.split(".")[0])
                    )
                    if is_correct:
                        st.success("Correct Answer!")
                    else:
                        st.error("Wrong Answer!")
