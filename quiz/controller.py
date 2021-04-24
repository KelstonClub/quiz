from . import db
from .ui import curses

def run():
    with curses.UI() as ui:
        for n in range(1, 4):
            question = db.get_question(n)
            ui.show_question(question)
            answers = db.get_answers(n)
            ui.show_multichoice_answers(answers)

            answer = ui.detect_multichoice_answers(answers, 3)
            print("You answered:", answer)

