import sqlite3


def make_db(db_name="quizzes.db", schema="db.sql"):
    conn = sqlite3.connect(db_name, isolation_level=None)
    
    cur = conn.cursor()
    with open(schema, "r") as f:
        cur.executescript(f.read())

    return conn

def query(db, q, ret=None, args=tuple()):
    cur = db.cursor()
    cur.execute(q, args)

    if not ret:
        return

    if ret == 'insert':
        return cur.lastrowid

    if ret == 'fetch_one':
        return cur.fetchone()

    if ret == 'fetch_all':
        return cur.fetchall()

    else:
        raise ValueError('Invalid query return type.')


def get_all_quizes(db):
    return query(db, "SELECT id,name FROM quizzes", "fetch_all")


def get_quiz_questions(db, quiz_id):
    return query(db, "SELECT id FROM questions WHERE quiz_id = ?", "fetch_all", (quiz_id,))


def get_question(db, num):
    return query(db, "SELECT text FROM questions WHERE id = ?", "fetch_one", (num,))


def get_answers(db, num):
    return query(db, "SELECT text, is_right  FROM answers WHERE id = ?", "fetch_all", (num,))


def new_quiz(db, name):
    return query(db, "INSERT INTO quizzes(name) VALUES (?)", "insert", (name,))


def new_question(db, quiz_id, question, _type):
    return query(db, "INSERT INTO questions(quiz_id, text, type) VALUES (?, ?, ?)", "insert", (quiz_id, question, _type))


def new_answer(db, question_id, answer, is_right):
    return query(db, "INSERT INTO answers(question_id, text, is_right) VALUES (?, ?, ?)", "insert", (question_id, answer, is_right))


