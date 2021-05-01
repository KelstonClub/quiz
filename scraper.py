import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

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
    data = soup.find(class_="post-game-stat-table")
    print(data)
    return


if __name__ == "__main__":
    page = requests.get(BASE_SITE + BASE_URL)
    soup = BeautifulSoup(page.content, "html.parser")
    links = soup.find_all("a", href=True)
    quizzes = []
    for link in links:
        if link["href"].startswith("/quizzes/") and link["href"]:
            url = urljoin(link["href"], urlparse(link["href"]).path)
            if url != "/quizzes/random":
                quizzes.append(BASE_SITE + url)

    data = []
    for quiz in quizzes:
        qhtml = requests.get(quiz).content
        qname = get_quiz_name(qhtml)
        questions = get_quiz_questions_and_possible_answers(qhtml)
        ahtml = requests.get(quiz + "/stats").content
        answers = get_quiz_answers(ahtml)
        print(quiz, " => ", [qname, questions, answers])
