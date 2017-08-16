from HTMLParser import HTMLParser
import logging

from flask import Flask
from flask_ask import Ask, statement
import requests


app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)


@ask.launch
@ask.intent('AMAZON.HelpIntent')
@ask.intent('EruvStatusIntent')
def instructions():
    status = requests.get('http://www.universitycityeruv.org/status.php').text
    status = _strip_tags(status)  # to strip away the <u></u> tag
    status = status.replace('eruv', 'eiruv')  # for better pronunciation
    return statement(status)


@ask.intent('AMAZON.CancelIntent')
@ask.intent('AMAZON.StopIntent')
def stop():
    return statement('Goodbye.')


@ask.session_ended
def session_ended():
    return '{}', 200


# Strips HTML tags from a string
# Created by Stack Overflow user Eloff in answer to the question
# https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python

class MLStripper(HTMLParser):

    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def _strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


if __name__ == '__main__':
    # app.config['ASK_APPLICATION_ID'] = (
    #     'amzn1.ask.skill.89ae4a38-f08c-422c-8cbe-5109ec9b27b4')
    app.run(debug=True)
