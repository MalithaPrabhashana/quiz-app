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
    
class writeQuiz(Quiz):
    def ask_question(self, question):
        return f"{question.text} "

    def check_answer(self, question, answer):
        return str(answer).lower() == str(question.correct_answer).lower()