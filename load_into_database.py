import sys
import csv
from quiz import db


ACTIONS = {
    "quizzes": db.new_quiz,
    "questions": db.new_question,
    "answers": db.new_answer,
}

REL_ID = {
    "questions": "quizzes",
    "answers": "questions"
}


def rewrite_args(token, ids, *args):
    if token == "quizzes":
        return args[0]

    args = list(args)
    args[0] = ids[REL_ID[token]][int(args[0]) - 1]

    return args


def parse(conn, csv_file):
    ids = {"quizzes": [], "questions": []}
    
    for line in csv_file:
        token, *args = line
        if not token in ACTIONS:
            raise ValueError(f"Invalid element of type=`{token}`")

        try:
            args = rewrite_args(token, ids, *args)
            rval = ACTIONS[token](conn, args)
        
        except Exception as e:
            print(f"Catched exception while inserting element of type=`{token}` into database with arguments=`{list(args)}`. This was possible caused because of an invalid formatted data file.\nError: {e}\n")

        finally:
            print(f"Inserted element in table `{token}`.")
            if token in ids.keys():
                ids[token].append(rval)


if __name__ == "__main__":    
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <csv file>")
        sys.exit()


    with open(sys.argv[1], "r") as f:
        csv_file = csv.reader(f)
        conn = db.make_db()
        parse(conn, csv_file)

    print("Finished inserting data.")
