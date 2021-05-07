from quiz.db import Database, models
from .ui import curses

db = Database(path="quizzes.db", debug=False)
db.register(models.Quiz)
db.register(models.Question)
db.register(models.Answer)


def run():
    with curses.UI() as ui:
        for n in range(1, 4):
            question = db.get("question").by_id(str(n))
            ui.show_question(question.text)
            answers = question.answers
            ui.show_multichoice_answers(answers)

            answer = ui.detect_multichoice_answers(answers, 3)
            print("You answered:", answer)
