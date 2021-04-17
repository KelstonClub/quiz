import sqlite3


def make_database(db_name="quizzes.db", schema="db.sql"):
    conn = sqlite3.connect(db_name, isolation_level=None)
    cur = conn.cursor()
    with open(schema, "r") as f:
        cur.executescript(f.read())

    cur.close()
    return conn

db = make_database()

def get_question(num):
    cur = db.cursor()
    cur.execute("SELECT * FROM questions WHERE id = ?", (num,))
    data = cur.fetchone()
    cur.close()
    
    return data


def get_answers(num):
    cur = db.cursor()
    cur.execute("SELECT * FROM answers WHERE id = ?", (num,))
    data = cur.fetchall()
    cur.close()
    
    return data


def new_quiz(name):
    cur = db.cursor()
    cur.execute("INSERT INTO quizzes(name) VALUES (?)", (name,));
    quiz_id = cur.lastrowid
    cur.close()
    
    return quiz_id


def new_question(quiz_id, question):
    cur = db.cursor()
    cur.execute("INSERT INTO questions(quiz_id, text) VALUES (?, ?)", (quiz_id, question,))
    question_id = cur.lastrowid
    cur.close()
    
    return question_id


def new_answer(question_id, answer):
    cur = db.cursor()
    cur.execute("INSERT INTO answers(question_id, text) VALUES (?, ?)", (question_id, answer,))
    answer_id = cur.lastrowid
    cur.close()
    
    return answer_id

if __name__ == "__main__":
    quiz_id = new_quiz("Maths quiz")
    print(f"{quiz_id=}")
    question_id = new_question(quiz_id, "What is 2+2?")
    print(f"{question_id=}")
    ids = []
    for i in range(1, 5):
        ids.append(new_answer(question_id, str(i)))

    print(f"{ids=}")
    db.close()

