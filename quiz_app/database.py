import sqlite3
from models.question import Question

class Database:
    def __init__(self):
        # Enable thread-safety for SQLite
        self.conn = sqlite3.connect("quiz.db", check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    type TEXT NOT NULL,
                    options TEXT,
                    correct_answer TEXT
                )
                """
            )

    def add_question(self, question: Question):
        options = "|".join(question.options) if hasattr(question, "options") else None
        question_type = type(question).__name__.replace("Question", "").lower()
        with self.conn:
            self.conn.execute(
                "INSERT INTO questions (text, type, options, correct_answer) VALUES (?, ?, ?, ?)",
                (question.text, question_type, options, question.correct_answer),
            )

    def get_all_questions(self):
        with self.conn:
            cursor = self.conn.execute("SELECT id, text, type, options, correct_answer FROM questions")
            return [
                {
                    "id": row[0],       
                    "text": row[1],
                    "type": row[2],
                    "options": row[3].split("|") if row[3] else None,
                    "correct_answer": row[4],
                }
                for row in cursor.fetchall()
            ]
