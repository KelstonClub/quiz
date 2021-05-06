import sys
import csv
from quiz.db import Database


def parse(db, csv_file):
    ids = {"quizzes": [], "questions": []}

    for line in csv_file:
        token, *args = line
        print(token, args)
        if token == "quizzes":
            rval = db.conn.execute("INSERT INTO quizzes(name) VALUES (?)",
                                   args).lastrowid

        elif token == "questions":
            qid = ids["quizzes"][int(args[0]) - 1]
            rval = db.conn.execute(
                "insert into questions(quiz_id, text, type) VALUES (?, ?, ?)",
                (qid, args[1], args[2])).lastrowid

        elif token == "answers":
            qid = ids["questions"][int(args[0]) - 1]
            rval = db.conn.execute(
                "insert into answers(question_id, text, is_right) VALUES (?, ?, ?)",
                (qid, args[1], args[2]))

        else:
            raise ValueError(f"Invalid token: `{token=}`")

        if token in ["quizzes", "questions"]:
            ids[token].append(rval)


class App:
    config = {"DATABASE_PATH": "quizzes.db"}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <csv file>")
        sys.exit()

    with open(sys.argv[1], "r") as f:
        csv_file = csv.reader(f)
        db = Database(App)
        db.run_migrations("schema.sql")
        parse(db, csv_file)

    print("Finished inserting data.")
