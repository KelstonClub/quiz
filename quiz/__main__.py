from flask import Flask, request, render_template, g, session, redirect, url_for
import os
from . import db


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)


def get_db():
    _db = getattr(g, '_database', None)
    if _db is None:
        _db = g._database = db.make_db()
    
    return _db


@app.teardown_appcontext
def close_connection(exception):
    _db = getattr(g, '_database', None)
    if _db is not None:
        _db.close()


@app.route("/")
def choose_quiz():
    with app.app_context():
        conn = get_db()
        return render_template("choose_quiz.html", quizzes=db.get_all_quizzes(conn))


@app.route("/quiz/<qid>/", methods=["GET", "POST"])
def show_questions(qid):
    if session.get("qid") and session["qid"] != qid:
        return redirect(url_for("show_questions", qid=session["qid"]))
    
    if request.method == "GET":
        with app.app_context():
            conn = get_db()
        
            if not session.get("questions"):
                questions = db.get_quiz_questions(conn, qid)
                session["qid"] = qid
                session["questions"] = questions
                session["quiz_len"] = len(questions)
                session["position"] = 0
                session["correct"] = 0
        
            quiestion_id = session["questions"][session["position"]]
            question = db.get_question(conn, quiestion_id)
            answers = db.get_answers(conn, quiestion_id)
            session["answer"] = [ans for ans in answers if ans[1] == "True"][0]
        
            return render_template("question.html", question=question, answers=answers)
    else:
        correct = request.form.get("answer") == session["answer"][0]
        if correct:
            session["correct"] += 1

        if session["quiz_len"] > session["position"] + 1:
            session["position"] += 1
        else:
            return redirect(url_for("show_score", qid=qid))

        return redirect(url_for("show_questions", qid=qid))


@app.route("/quiz/<qid>/score/")
def show_score(qid):
    if not session.get("qid") or session["qid"] != qid or session["position"]+1 != session["quiz_len"]:
        return redirect(url_for("choose_quiz"))
    
    right = session["correct"]
    wrong = session["quiz_len"] - right
    score = 5*right - wrong # Score is 5 points per right answer minus the wrong ones.
    session.clear() # Clear session so user can do another quiz.
    return render_template("score.html", score=score)


if __name__ == '__main__':
    app.run(debug=True)
