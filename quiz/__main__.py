from flask import Flask, request, escape, redirect, url_for, render_template
import os
from . import db

app = Flask(__name__)

HERE = os.path.dirname(__file__)

@app.route("/")
def choose_quiz():
    connenction = db.make_db()
    return render_template("choose_quiz.html", quizes=db.get_all_quizes(connenction))

def display_question(questionid, id):
    connenction = db.make_db()
    question = db.get_question(connenction, id)
    answers = db.get_answers(connenction, questionid)
    return render_template("quiz_questions.html", question=question, answers=answers)

@app.route("/quiz/<id>")
def show_questions(id):
    connenction = db.make_db()
    questions = db.get_quiz_questions(connenction, id)
    for questionid in questions:
        display_question(questionid, id)
    return render_template("quiz_questions.html")

@app.route("/quiz/<id>/score")
def show_score(id):
    return render_template("quiz_score.html")

if __name__ == '__main__':
    app.run(debug=True)