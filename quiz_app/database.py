import sqlite3
from models.question import Question

class Database:
    def __init__(self):
        self.db_path = "quiz.db"
        self.create_tables()

    def get_connection(self):
        """Creates a new SQLite connection for the current request."""
        return sqlite3.connect(self.db_path)

    def create_tables(self):
        with self.get_connection() as conn:
            conn.execute(
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
        with self.get_connection() as conn:
            conn.execute(
                "INSERT INTO questions (text, options, correct_answer) VALUES (?, ?, ?)",
                (question.text, options, question.correct_answer),
            )

    def get_all_questions(self):
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT id, text, options, correct_answer FROM questions")
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
        with self.get_connection() as conn:
            cursor = conn.execute(
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
