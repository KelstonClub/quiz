from quiz.db import Table


class Quiz(Table):
    def __init__(self, _id, name, db):
        super().__init__(db)

        self.id = _id
        self.name = name

    def all(self):
        return self.query("SELECT id, name FROM quizzes").fetchall()

    def by_id(self, _id):
        quiz = self.query("SELECT id, name FROM quizzes WHERE id = ?",
                          _id).fetchone()
        if not quiz:
            return None

        _id, name = quiz
        return Quiz(str(_id), name, self.db)

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
            serialized.append(Question(str(_id), text, _type, self.db))

        return serialized


class Question(Table):
    def __init__(self, _id, text, _type, db):
        super().__init__(db)

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
            serialized.append(Answer(str(_id), text, is_right, self.db))

        return serialized

    def get_right_answer(self):
        answer = self.query(
            "SELECT id, text, is_right FROM answers WHERE question_id = ? AND is_right = 'True'",
            self.id).fetchone()
        if not answer:
            return None

        _id, text, is_right = answer
        return Answer(str(_id), text, is_right, self.db)


class Answer(Table):
    def __init__(self, _id, text, is_right, db):
        super().__init__(db)

        self.id = _id
        self.text = text
        self.is_right = is_right
