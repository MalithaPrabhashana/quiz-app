### Directory structure:
# - quiz_app/
#   - main.py
#   - models/
#       - __init__.py
#       - quiz.py
#       - question.py
#   - routes/
#       - __init__.py
#       - teacher.py
#       - student.py
#   - database.py

# main.py
from fastapi import FastAPI
from routes import teacher, student

app = FastAPI()

app.include_router(teacher.router, prefix="/teacher", tags=["Teacher"])
app.include_router(student.router, prefix="/student", tags=["Student"])

# models/quiz.py
from abc import ABC, abstractmethod

class Quiz(ABC):
    def __init__(self, title: str):
        self.title = title
        self.score = 0

    @abstractmethod
    def ask_question(self, question):
        pass

    @abstractmethod
    def check_answer(self, question, answer):
        pass

class MultipleChoiceQuiz(Quiz):
    def ask_question(self, question):
        options = "\n".join(f"{idx}. {option}" for idx, option in enumerate(question.options, 1))
        return f"{question.text}\n{options}"

    def check_answer(self, question, answer):
        return answer == question.correct_answer

class TrueFalseQuiz(Quiz):
    def ask_question(self, question):
        return f"{question.text} (True/False)"

    def check_answer(self, question, answer):
        return str(answer).lower() == str(question.correct_answer).lower()

# models/question.py
class Question:
    def __init__(self, text: str, options: list = None, correct_answer=None):
        self.text = text
        self.options = options or []
        self.correct_answer = correct_answer

# routes/teacher.py
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

# routes/student.py
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

# database.py
import sqlite3
from models.question import Question

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("quiz.db")
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    options TEXT,
                    correct_answer TEXT
                )
                """
            )

    def add_question(self, question: Question):
        options = "|".join(question.options) if question.options else None
        with self.conn:
            self.conn.execute(
                "INSERT INTO questions (text, options, correct_answer) VALUES (?, ?, ?)",
                (question.text, options, question.correct_answer),
            )

    def get_all_questions(self):
        with self.conn:
            cursor = self.conn.execute("SELECT id, text, options, correct_answer FROM questions")
            return [
                {
                    "id": row[0],
                    "text": row[1],
                    "options": row[2].split("|") if row[2] else None,
                    "correct_answer": row[3],
                }
                for row in cursor.fetchall()
            ]

    def get_question_by_id(self, question_id):
        with self.conn:
            cursor = self.conn.execute(
                "SELECT id, text, options, correct_answer FROM questions WHERE id = ?", (question_id,)
            )
            row = cursor.fetchone()
            if not row:
                return None
            return {
                "id": row[0],
                "text": row[1],
                "options": row[2].split("|") if row[2] else None,
                "correct_answer": row[3],
            }
