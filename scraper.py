import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

BASE_SITE = "https://www.jetpunk.com"
BASE_URL = "/tags/multiple-choice"


def get_quiz_name(content):
    soup = BeautifulSoup(content, 'html.parser')
    name = soup.find('h1').text
    return name


def get_quiz_questions_and_possible_answers(content):
    soup = BeautifulSoup(content, 'html.parser')
    questions = soup.find_all('div', class_='question')
    return questions


def get_quiz_answers(content):
    return


if __name__ == '__main__':
    page = requests.get(BASE_SITE + BASE_URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    links = soup.find_all('a', href=True)
    quizzes = []
    for link in links:
        if link["href"].startswith("/quizzes/"):
            url = urljoin(link["href"], urlparse(link["href"]).path)
            quizzes.append(BASE_SITE + url)

    data = []
    for quiz in quizzes:
        qhtml = requests.get(quiz).content
        qname = get_quiz_name(qhtml)
        questions = get_quiz_questions_and_possible_answers(qhtml)
        print(quiz, " => ", [qname, questions])
