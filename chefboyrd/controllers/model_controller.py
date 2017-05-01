'''ModelController

This is a preprocessor for the prediction_controller. Given data in the form of our local models,
it converts it into numbers usable by the prediction controller.

'''
from peewee import Model
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from datetime import datetime, timedelta, date, time
from chefboyrd.models import Orders, Tabs, Meals, Ingredients, MealIngredients, Quantities
from peewee import fn

def polynomialModel(x, *params):
    '''
    This is the polynomial model that will be fit by our algorithm. 

    Args:
        x : input matrix where the features are rows and each predictor(data point) is a column
        params : the parameters for the model

    Returns:
        sum : the output vector where each indice is a predictor
    '''
    complexity = 1
    sum = params[0]
    for i in range(len(x)):
        for j in range(1,complexity+1):
            sum += params[complexity*i+j]*(x[i]**j)
    return sum

def sinusoidalModel(x, *params):
    '''
    This is the sinusoidal model that will be fit by our algorithm. 

    Args:
        x : input matrix where the features are rows and each predictor(data point) is a column
        params : the parameters for the model

    Returns:
        list - the output vector where each indice is a predictor
    '''
    sum = params[9]
    for i in range(len(x)):
        sum += params[3*i]*np.sin(params[3*i+1]*x[i]+params[3*i+2])
    return sum

def orders_to_list(orders):
    '''
    Converts peewee query result set to a list of dictionary of lists

    Args:
        orders (list): Accepts a list of orders made from a query for peewee
    '''
    orders = orders.switch(Orders).join(Meals).order_by(Meals.name)
    currentMeal = ""
    previousMeal = ""
    currentHour = -1
    previousHour = -1
    mealCounter = 0
    mealDict = {}
    for order in orders:
        currentMeal = order.meal.name
        # Check if you're on a new meal
        if currentMeal != previousMeal:
            # Add the rest of the mealCounter to the previous meal
            if previousMeal != "" and mealCounter != 0:
                ts = order.tab.timestamp
                row = np.array([[ts.hour, ts.day, ts.month, mealCounter]])
                if previousMeal in mealDict:
                    mealDict[previousMeal] = np.append(mealDict[previousMeal], row, axis=0)
                else:
                    mealDict[previousMeal] = row
                mealCounter = 0

        mealCounter += 1
        # Check if the hour bucket is the same
        currentHour = order.tab.timestamp.hour 
        if currentHour != previousHour:
            if previousHour != -1:
                ts = order.tab.timestamp
                row = np.array([[ts.hour, ts.day, ts.month, mealCounter]])
                if currentMeal in mealDict:
                    mealDict[currentMeal] = np.append(mealDict[currentMeal], row, axis=0)
                else:
                    mealDict[currentMeal] = row
                mealCounter = 0
        previousHour = currentHour
        previousMeal = currentMeal
    return mealDict

def train_regression(mealDict, modelType):
    '''
    This trains all of the meals and fits their data to their own set of parameters

    Args:
        mealDict : The meal dictionary containing order data created by orders_to_list
        modelType : the type of model to use(sinusoidal, polynomial)

    Returns:
        mealsParams : a dictionary that contains the parameters for each corresponding meal
    '''
    mealsParams = {}
    for meal_key in mealDict:
        x = np.transpose(mealDict[meal_key][:, 0:3])
        y = mealDict[meal_key][:, 3]
        mealParams = train_regression_single(x, y, modelType)
        mealsParams[meal_key] = mealParams;
    return mealsParams

def train_regression_single(x, y, modelType):
    '''
    Trains a single meal and fits it to a model to find its parameters

    Args:
        x : The input vector(which is composed of rows 0 to 3 in the vector)
        y : The expected output vector(the last row)
        modelType : the type of model to use

    Returns:
        params : A list of parameters
    '''
    # Train the model
    initial_params = []

    if modelType == 'Polynomial':
        initial_params = [1.,1.,1.,1.]
        params, pcov = curve_fit(polynomialModel, x, y, initial_params)
        return params
    elif modelType == 'Sinusoidal':
        initial_params = [1.,1.,1.,1.,1.,1.,1.,1.,1.,1.]
        params, pcov = curve_fit(sinusoidalModel, x, y, initial_params)
        return params

def get_earliest_datetime():
    '''Finds the minimum datetime in the orders database'''
    earliestDatetime = Tabs.select(fn.MIN(Tabs.timestamp)).scalar(convert=True)
    return earliestDatetime

def get_last_datetime():
    '''Finds the maximum datetime in the orders database'''
    lastDatetime = Tabs.select(fn.MAX(Tabs.timestamp)).scalar(convert=True)
    return lastDatetime


    
