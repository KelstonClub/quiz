from flask import Flask, request, escape, redirect, url_for, render_template
import os
from . import db

app = Flask(__name__)

HERE = os.path.dirname(__file__)

@app.route("/")
def choose_quiz():
    connenction = db.make_db()
    return render_template("choose_quiz.html", quizes=db.get_all_quizes(connenction))

@app.route("/quiz/<id>/<questionid>")
def show_questions(id, questionid):
    return render_template("quiz_questions.html")

@app.route("/quiz/<id>/score")
def show_score(id):
    return render_template("quiz_score.html")

if __name__ == '__main__':
    app.run(debug=True)