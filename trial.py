import time

from quiz.ui import text

QUESTION = "What is your name?"
ANSWERS = "Tim", "Tom", "Jim", "Jon"

with text.UI() as ui:
   ui.show_question(QUESTION)
   ui.show_multichoice_answers(ANSWERS)
   choice = ui.detect_multichoice_answers(ANSWERS, 1 + len(ANSWERS))
   #~ time.sleep(2)

print("Choice:", choice)