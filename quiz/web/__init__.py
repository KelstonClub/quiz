from flask import Flask, request, render_template, session, redirect, url_for, abort
import random
import os
from quiz.db import Database
from .models import Quiz, Question, Answer

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(32)
app.config["DATABASE_PATH"] = "quizzes.db"
db = Database(app)
db.run_migrations("schema.sql")
# Register tables in database.
db.register(Quiz)
db.register(Question)
db.register(Answer)


@app.route("/")
def choose_quiz():
    quizzes = db.get("quiz").all()
    return render_template("choose_quiz.html", quizzes=quizzes)


@app.route("/quiz/<qid>/", methods=["GET", "POST"])
def show_questions(qid):
    quiz = db.get("quiz").by_id(qid)
    if quiz is None:
        abort(404)

    if request.method == "GET":
        questions = quiz.questions
        if questions is None:
            abort(
                500
            )  # We should show a special error if there are no questions.

        session["quiz_len"] = len(questions)
        if not session.get("position"):
            session["position"] = 0

        question = questions[session["position"]]
        answers = question.answers
        if answers is None:
            abort(500)  # Same as with questions

        if question.type == "multiple choice":
            random.shuffle(answers)

        return render_template("question.html",
                               question=question,
                               answers=answers,
                               num_answers=len(answers))

    else:
        right_answer = quiz.questions[session["position"]].get_right_answer()
        if request.form.get("answer") == right_answer.text:
            if not session.get("right"):
                session["right"] = 1
            else:
                session["right"] += 1

        if session["quiz_len"] == session["position"] + 1:
            return redirect(url_for("show_score", qid=qid))

        session["position"] += 1

    return redirect(url_for("show_questions", qid=qid))


@app.route("/quiz/<qid>/score/")
def show_score(qid):
    quiz = db.get("quiz").by_id(qid)
    if quiz is None:
        abort(404)

    right = session.get("right", 0)
    wrong = session["quiz_len"] - right
    score = 5 * right - wrong  # Score is 5 points per right answer minus the wrong ones.
    if score < 0: score = 0
    session.clear()  # Clear session so user can do another quiz.
    return render_template("score.html", score=score)
