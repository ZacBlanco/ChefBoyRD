import logging
import sys
from datetime import datetime
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

sys.path.append('..')

from chefboyrd.controllers import data_controller


APP = Flask(__name__)
ask = Ask(APP, "/")
logging.getLogger("flask_ask").setLevel(logging.INFO)

def reprompt():
    resp = statement('')
    resp._response = {}
    resp._response['directives'] = [{'type':'Dialog.Delegate'}]
    return resp



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
    print("Stat Function Args: type: {}, start: {}, end: {}".format(stat_type, start_date, end_date))
    if start_date is None:
        return reprompt()

    msg = 'You wrote bad code'
    if stat_type is None:
        pass
    else:
        pass

    return statement(msg)

@ask.intent("PredictionIntent", convert={'meal_type': str, 'start_date': datetime, 'end_date': datetime})
def prediction(meal_type, start_date, end_date):
 
    if meal_type is None or start_date is None or end_date is None:
        return reprompt()
 
    modelType = 'Polynomial'
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