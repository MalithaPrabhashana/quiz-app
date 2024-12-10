from models.question import MultipleChoiceQuestion, SingleAnswerQuestion, TrueFalseQuestion
from database import Database

class Quiz:
    def __init__(self, title: str):
        self.title = title
        self.questions = []
        self.db = Database()

    def add_question(self, question_type: str, data: dict):
        """Add a question to the quiz and database."""
        if question_type == "multiple_choice":
            question = MultipleChoiceQuestion(data["text"], data["options"], data["correct_answer"])
        elif question_type == "single_answer":
            question = SingleAnswerQuestion(data["text"], data["correct_answer"])
        elif question_type == "true_false":
            question = TrueFalseQuestion(data["text"], data["correct_answer"])
        else:
            raise ValueError("Invalid question type!")
    
        self.questions.append(question)
        self.db.add_question(question)  # Save to database

    def load_questions(self):
        """Load questions from the database."""
        raw_questions = self.db.get_all_questions()

        for raw in raw_questions:
            if raw["type"] == "multiple_choice":
                question = MultipleChoiceQuestion(raw["text"], raw["options"], raw["correct_answer"])
            elif raw["type"] == "single_answer":
                question = SingleAnswerQuestion(raw["text"], raw["correct_answer"])
            elif raw["type"] == "true_false":
                question = TrueFalseQuestion(raw["text"], raw["correct_answer"])
            else:
                continue
            self.questions.append(question)
            return question
