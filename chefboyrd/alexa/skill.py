import logging
from datetime import datetime
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session


APP = Flask(__name__)
ask = Ask(APP, "/")
logging.getLogger("flask_ask").setLevel(logging.INFO)


@ask.launch
def welcome():
    welcome_msg = render_template('welcome')
    return question(welcome_msg)

@ask.intent("AMAZON.StopIntent")
def cancel():
    return statement(render_template('stop'))

@ask.intent("AMAZON.CancelIntent")
def stop():
    return statement(render_template('stop'))

@ask.intent("CommandIntent", convert={'stat_type': str, 'start_date': datetime, 'end_date': datetime})
def statistics(stat_type, start_date, end_date):

    if stat_type is None or start_date is None:
        resp = statement('')
        resp._response = {}
        resp._response['directives'] = {'type':'Dialog.Delegate'}

    return statement('I got all of your information')

@ask.intent("PredictionIntent", convert={'meal_type': str, 'start_date': datetime, 'end_date': datetime})
def prediction(meal_type, start_date, end_date):

    if meal_type is None or start_date is None:
        resp = statement('')
        resp._response = {}
        resp._response['directives'] = {'type':'Dialog.Delegate'}

    return statement('I got all of your information for prediction.')

if __name__ == '__main__':
    APP.run(debug=True)