from abc import ABC, abstractmethod

class Question(ABC):
    def __init__(self, text: str, correct_answer):
        self.text = text
        self.correct_answer = correct_answer

    @abstractmethod
    def get_formatted_question(self):
        """Format the question for display."""
        pass

    @abstractmethod
    def check_answer(self, answer):
        """Validate the provided answer."""
        pass
    

class MultipleChoiceQuestion(Question):
    def __init__(self, text: str, options: list, correct_answer: int):
        super().__init__(text, correct_answer)
        self.options = options

    def get_formatted_question(self):
        options_text = "\n".join(f"{i + 1}. {option}" for i, option in enumerate(self.options))
        return f"{self.text}\n{options_text}"

    def check_answer(self, answer):
        return int(answer) == self.correct_answer


class SingleAnswerQuestion(Question):
    def __init__(self, text: str, correct_answer: str):
        super().__init__(text, correct_answer)

    def get_formatted_question(self):
        return self.text

    def check_answer(self, answer):
        return str(answer).lower() == str(self.correct_answer).lower()


class TrueFalseQuestion(Question):
    def __init__(self, text: str, correct_answer: bool):
        super().__init__(text, correct_answer)

    def get_formatted_question(self):
        return f"{self.text} (True/False)"

    def check_answer(self, answer):
        return str(answer).lower() == str(self.correct_answer).lower()
