import curses

from . import base

class UI(base.BaseUI):

    def __init__(self):
        """Initialise the screen ready to start
        """
        self.screen = curses.initscr()

    def __enter__(self):
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)
        return self

    def __exit__(self, *args, **kwargs):
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()

    def reset(self):
        self.screen.clear()

    def main(self):
        pass

    def execute_loop(self):
        """Execute whatever main loop the UI needs
        """
        curses.wrapper(self.main)

    def show_question(self, question, start_from_row=0):
        """Show the text or image for a single question
        """
        self.screen.addstr(start_from_row, 0, question)
        self.screen.refresh()

    def show_multichoice_answers(self, answers, start_from_row=1):
        """Show the possibilities for multiple choice answers"""
        for row, (letter, answer) in enumerate(zip("ABCDEFG", answers)):
            self.screen.addstr(start_from_row + row, 0, "%s - %s" % (letter, answer))
        self.screen.refresh()

    def detect_multichoice_answers(self, answers, start_from_row):
        """Return which answer(s) a user selected"""
        possibles = "ABCDEFG"[:len(answers)]
        self.screen.addstr(start_from_row, 0, "Choose one of %s-%s: " % (possibles[0], possibles[-1]))
        key = self.screen.getkey().upper()
        self.screen.addstr(1 + start_from_row, 0, "You chose: " + key)
        return key



    def detect_text_answer(self):
        """Return what text the user entered"""
        curses.echo()
        try:
            return self.screen.getstr()
        finally:
            curses.noecho()

