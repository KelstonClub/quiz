class BaseUI:

    def __init__(self):
        raise NotImplementedError

    def reset(self):
        """Initialise the screen ready to start
        """
        raise NotImplementedError

    def execute_loop(self):
        """Execute whatever main loop the UI needs
        """
        raise NotImplementedError

    def show_question(self, question):
        """Show the text or image for a single question
        """
        raise NotImplementedError

    def show_multichoice_answers(self, answers):
        """Show the possibilities for multiple choice answers"""
        raise NotImplementedError

    def detect_multichoice_answers(self):
        """Return which answer(s) a user selected"""
        raise NotImplementedError

    def detect_text_answer(self):
        """Return what text the user entered"""
        raise NotImplementedError

