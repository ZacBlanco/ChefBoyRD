import logging
import sys
from datetime import datetime
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
from chefboyrd.controllers import data_controller
from chefboyrd.controllers import model_controller
from chefboyrd.controllers import prediction_controller



APP = Flask(__name__)
ask = Ask(APP, "/")
logging.getLogger("flask_ask").setLevel(logging.INFO)

def reprompt():
    resp = statement('')
    resp._response = {}
    resp._response['directives'] = [{'type':'Dialog.Delegate'}]
    return resp

def todatetime(datestr):
    return datetime.strptime(datestr, '%Y-%m-%d')

def speak_date(dd):
    return dd.strftime("%B %d, %Y")


@ask.launch
def welcome():
    welcome_msg = render_template('welcome')
    return question(welcome_msg)

@ask.intent("AMAZON.HelpIntent")
def cancel():
    return statement(render_template('help'))

@ask.intent("AMAZON.StopIntent")
def cancel():
    return statement(render_template('stop'))

@ask.intent("AMAZON.CancelIntent")
def stop():
    return statement(render_template('stop'))

@ask.intent("CommandIntent", convert={'stat_type': str, 'start_date': datetime, 'end_date': datetime})
def statistics(stat_type, start_date, end_date):
    print("Stat Function Args: type: {}, start: {}, end: {}".format(stat_type, start_date, end_date))
    if start_date is None or stat_type is None:
        return reprompt()

    try:
        start_date = todatetime(start_date)
    except:
        return statement("You must provide a specific day")
    if end_date is None:
        end_date = datetime.now()
    else:
        end_date = todatetime(end_date)

    if end_date < start_date:
        return statement(render_template('bad_dates', start=speak_date(start_date.date()), end=speak_date(end_date.date())))

    msg = "Uh oh, I've encountered an error. Please try again"
    num = data_controller.people_in_range(start_date, end_date)
    if stat_type == 'revenue':
        dollars = int(data_controller.get_dollars_in_range(start_date, end_date))
        # print(type(render_template('dollars', amount=dollars)))
        msg = render_template('num_people', num=num, start=speak_date(start_date.date()), end=speak_date(end_date.date())) + render_template('dollars', amount=dollars)
    elif stat_type == 'meals':
        num_meals = data_controller.get_meals_in_range(start_date, end_date)
        msg = render_template('meals', meal=num_meals)
    elif stat_type == 'tabs':
        parties = len(data_controller.get_tabs_range(start_date, end_date))
        msg = render_template('tabs', parties=parties)
    elif stat_type == 'performance':
        dollars = int(data_controller.get_dollars_in_range(start_date, end_date))
        parties = len(data_controller.get_tabs_range(start_date, end_date))
        num_meals = data_controller.get_meals_in_range(start_date, end_date)
        msg = render_template('tabs', parties=parties)
        msg += render_template('meals', meal=num_meals)
        msg += render_template('num_people', num=num, start=speak_date(start_date.date()), end=speak_date(end_date.date())) + render_template('dollars', amount=dollars)

    print(msg)
    return statement(msg)

@ask.intent("PredictionIntent", convert={'meal_type': str, 'start_date': datetime, 'end_date': datetime})
def prediction(meal_type, start_date, end_date):
    print("Prediction Function Args: type: {}, start: {}, end: {}".format(meal_type, start_date, end_date))

    if meal_type is None or start_date is None or end_date is None:
        return reprompt()
    modelType = 'Polynomial'
    start_date = todatetime(start_date)
    end_date = todatetime(end_date)
    print(type(start_date))
    print(type(end_date))
    orders = data_controller.get_orders_date_range()
    processedOrders = model_controller.orders_to_list(orders)
    params = model_controller.train_regression(processedOrders, modelType)
    mealUsage = prediction_controller.predict_regression(params, modelType, start_date, end_date)
    if mealUsage is None:
        return statement(render_template('unsuited_prediction'))
    for meal_key in mealUsage:
        if meal_key == meal_type:
            return statement(render_template('prediction', meal_type=meal_type, meal_count=mealUsage[meal_key]))
    return statement(render_template('failed_prediction'))

if __name__ == '__main__':
    APP.run(debug=True)