from quiz.db import Table


class Quiz(Table):
    def __init__(self, _id, name):
        self.id = _id
        self.name = name

    def get_quizzes(self):
        return self.query("SELECT id, name FROM quizzes").fetchall()

    def get_quiz_by_id(self, _id):
        quiz = self.query("SELECT id, name FROM quizzes WHERE id = ?",
                          _id).fetchone()
        if not quiz:
            return None

        _id, name = quiz
        return Quiz(str(_id), name)

    @property
    def questions(self):
        questions = self.query(
            "SELECT id, text, type FROM questions WHERE quiz_id = ?",
            self.id).fetchall()
        if not questions:
            return None

        serialized = []
        for question in questions:
            _id, text, _type = question
            serialized.append(Question(str(_id), text, _type))

        return serialized


class Question(Table):
    def __init__(self, _id, text, _type):
        self.id = _id
        self.text = text
        self.type = _type

    @property
    def answers(self):
        answers = self.query(
            "SELECT id, text, is_right FROM answers WHERE question_id = ?",
            self.id).fetchall()
        if not answers:
            return None

        serialized = []
        for answer in answers:
            _id, text, is_right = answer
            serialized.append(Answer(str(_id), text, is_right))

        return serialized

    def get_right_answer(self):
        answer = self.query(
            "SELECT id, text, is_right FROM answers WHERE question_id = ? AND is_right = 'True'",
            self.id).fetchone()
        if not answer:
            return None

        _id, text, is_right = answer
        return Answer(str(_id), text, is_right)


class Answer(Table):
    def __init__(self, _id, text, is_right):
        self.id = _id
        self.text = text
        self.is_right = is_right
