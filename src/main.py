import logging

from flask import Flask
from flask_ask import Ask, statement
import requests


app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)


# General Helpers

def _eruv_status():
    return requests.get('http://www.universitycityeruv.org/status.php').text


# Intent and Event Handlers

@ask.launch
@ask.intent('AMAZON.HelpIntent')
@ask.intent('EruvStatusIntent')
def instructions():
    return statement(_eruv_status())


@ask.intent('AMAZON.CancelIntent')
@ask.intent('AMAZON.StopIntent')
def stop():
    return statement('Goodbye.')


@ask.session_ended
def session_ended():
    return '{}', 200


if __name__ == '__main__':
    # app.config['ASK_APPLICATION_ID'] = (
    #     'amzn1.ask.skill.89ae4a38-f08c-422c-8cbe-5109ec9b27b4')
    app.run(debug=True)
