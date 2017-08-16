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
    app.config['ASK_APPLICATION_ID'] = (
        'amzn1.ask.skill.d4ae690d-55d0-494c-9bd3-276fa4e7a9fb')
    app.run(debug=False)
