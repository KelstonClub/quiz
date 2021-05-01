import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import re

BASE_SITE = "https://www.jetpunk.com"
BASE_URL = "/tags/multiple-choice"


def get_quiz_name(content):
    soup = BeautifulSoup(content, "html.parser")
    name = soup.find("h1").text
    return name


def get_quiz_questions_and_possible_answers(content):
    soup = BeautifulSoup(content, "html.parser")
    questions = soup.find_all("div", class_="question")
    if not questions:
        return None

    possible_answers = soup.find_all("div", class_="choices") 
    if not possible_answers:
        return None

    data = {}
    for question, answers in zip(questions, possible_answers):
        q = question.find_all("span")[1].text
        a = [i.text.strip() for i in answers.find_all(class_="mc-active-choice")]
        data[q] = a

    return data


def get_quiz_answers(content):
    soup = BeautifulSoup(content, "html.parser")
    data = soup.find(class_="post-game-stat-table").find_all('td')
    q_and_a = [i.text for i in data if not "\n" in i.text]
    return q_and_a


def into_csv_format(qid, data):
    fmt = f"quizzes, {data[0]}"
    for i, (question, answers) in enumerate(data[1].items(), 1):
        fmt += f"\nquestions,{qid},{question},multiple choice"
        for answer in answers:
            fmt += f"\nanswers,{i},{answer},False"

    for q, a in zip(data[2], data[2][1::]):
        qid = re.search(f"questions,([0-9]*),{q},multiple choice", fmt)
        # For some reason some questions are not found
        if qid:
            qid = qid.group(1)
        else:
            qid = '1'

        fmt.replace(f"{qid},{a},False", f"{qid},{a},True")

    return fmt


if __name__ == "__main__":
    page = requests.get(BASE_SITE + BASE_URL)
    soup = BeautifulSoup(page.content, "html.parser")
    links = soup.find_all("a", href=True)
    quizzes = set()
    for link in links:
        if link["href"].startswith("/quizzes/") and link["href"]:
            url = urljoin(link["href"], urlparse(link["href"]).path)
            if url != "/quizzes/random":
                quizzes.add(BASE_SITE + url)

    data = []
    for i, quiz in enumerate(quizzes, 1):
        qhtml = requests.get(quiz).content
        qname = get_quiz_name(qhtml)
        questions = get_quiz_questions_and_possible_answers(qhtml)
        if not questions:
            continue
        
        ahtml = requests.get(quiz + "/stats").content
        answers = get_quiz_answers(ahtml)
        if not answers:
            continue
        
        data = (qname, questions, answers)
        formatted = into_csv_format(i, data)

        print(f"Finished loading quiz {i}")
        with open('jetpunk.csv', 'a') as f:
            f.write(formatted)

