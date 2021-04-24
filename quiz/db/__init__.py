import sqlite3


def make_db(db_name="quizzes.db", schema="db.sql"):
    conn = sqlite3.connect(db_name, isolation_level=None)
    
    cur = conn.cursor()
    with open(schema, "r") as f:
        cur.executescript(f.read())
    cur.close()

    return conn

def query(db, q, ret=None, *args):
    cur = db.cursor()
    if args and isinstance(args[0], list):
        args = args[0]
    
    cur.execute(q, args)
    rval = None
    
    if ret == "insert":
        rval = cur.lastrowid

    elif ret == "fetch_one":
        rval = cur.fetchone()

    elif ret == "fetch_all":
        rval = cur.fetchall()
        
    cur.close()
    return rval


def get_all_quizzes(db):
    return query(db, "SELECT id,name FROM quizzes", "fetch_all")


def get_quiz_questions(db, args):
    return query(db, "SELECT id FROM questions WHERE quiz_id = ?", "fetch_all", args)


def get_question(db, args):
    return query(db, "SELECT text FROM questions WHERE id = ?", "fetch_one", args)


def get_answers(db, args):
    return query(db, "SELECT text, is_right  FROM answers WHERE id = ?", "fetch_all", args)


def new_quiz(db, args):
    return query(db, "INSERT INTO quizzes(name) VALUES (?)", "insert", args)


def new_question(db, args):
    return query(db, "INSERT INTO questions(quiz_id, text, type) VALUES (?, ?, ?)", "insert", args)


def new_answer(db, args):
    return query(db, "INSERT INTO answers(question_id, text, is_right) VALUES (?, ?, ?)", "insert", args)


