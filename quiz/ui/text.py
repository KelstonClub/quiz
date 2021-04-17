from . import base

class UI(base.BaseUI):

    def __init__(self):
        """Initialise the screen ready to start
        """
        pass

    def reset(self):
        """Initialise the screen ready to start
        """

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def execute_loop(self):
        """Execute whatever main loop the UI needs
        """
        pass

    def show_question(self, question):
        """Show the text or image for a single question
        """
        print(question)

    def show_multichoice_answers(self, answers, *args):
        """Show the possibilities for multiple choice answers"""
        for letter, answer in zip("ABCDEFG", answers):
            print("%s - %s" % (letter, answer))

    def detect_multichoice_answers(self, answers, *args):
        """Return which answer(s) a user selected"""
        possibles = "ABCDEFG"[:len(answers)]
        return input("Choose one of %s-%s: " % (possibles[0], possibles[-1])).upper()

    def detect_text_answer(self):
        """Return what text the user entered"""
        return input("Answer: ")
