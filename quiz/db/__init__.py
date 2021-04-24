import sqlite3


def make_database(db_name="quizzes.db", schema="db.sql"):
    conn = sqlite3.connect(db_name, isolation_level=None)
    
    cur = conn.cursor()
    with open(schema, "r") as f:
        cur.executescript(f.read())

    cur.close()

    return conn

db = make_database()

def query(q, ret=None, args=tuple()):
    cur = db.cursor()
    cur.execute(q, args)
    cur.close()

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


def get_all_quizes():
    return query("SELECT id,name FROM quizzes", "fetch_all")


def get_quiz_questions(quiz_id):
    return query("SELECT id FROM questions WHERE quiz_id = ?", "fetch_all", (quiz_id,))


def get_question(num):
    return query("SELECT text FROM questions WHERE id = ?", "fetchone", (num,))


def get_answers(num):
    return query("SELECT text, is_right  FROM answers WHERE id = ?", "fetchall", (num,))


def new_quiz(name):
    return query("INSERT INTO quizzes(name) VALUES (?)", "insert", (name,))


def new_question(quiz_id, question, _type):
    return query("INSERT INTO questions(quiz_id, text, type) VALUES (?, ?, ?)", "insert", (quiz_id, question, _type))


def new_answer(question_id, answer, is_right):
    return query("INSERT INTO answers(question_id, text, is_right) VALUES (?, ?, ?)", "insert", (question_id, answer, is_right))


if __name__ == "__main__":
    quiz_id = new_quiz("Maths quiz")
    print(f"{quiz_id=}")
    question_id = new_question(quiz_id, "What is 2+2?", "multiple choice")
    print(f"{question_id=}")
    ids = []
    for i in range(1, 5):
        ids.append(new_answer(question_id, str(i), True if i == 4 else False))

    print(f"{ids=}")
    db.close()

