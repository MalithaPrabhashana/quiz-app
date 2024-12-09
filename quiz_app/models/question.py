class Question:
    def __init__(self, text: str, options: list = None, correct_answer=None):
        self.text = text
        self.options = options or []
        self.correct_answer = correct_answer