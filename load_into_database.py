import sys
import csv
from quiz import db

if __name__ == "__main__":    
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <csv file>")
        sys.exit()

    data = {"quizzes": [], "questions": []}

    with open(sys.argv[1], "r") as f:
        cf = csv.reader(f)
        for line in cf:
            if line[0] == "quiz":
                qid = db.new_quiz(line[1])
                data["quizzes"].append(qid)
            
            elif line[0] == "question":
                qid = db.new_question(data["quizzes"][int(line[1])-1], line[2], line[3])
                data["questions"].append(qid)

            elif line[0] == "answer":
                db.new_answer(data["questions"][int(line[1])-1], line[2], line[3])

            else:
                raise ValueError(f"Invalid type={line[0]} for inseting to database.")
    
    print("Finished inserting data.")
