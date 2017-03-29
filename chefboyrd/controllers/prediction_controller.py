'''PredictionController

This controller performs our machine learning algorithms using non-linear regression fits on the data.
'''

import numpy as np
from math import floor
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, date, time
from scipy.optimize import curve_fit
from chefboyrd.controllers.model_controller import polynomialModel, sinusoidalModel, get_earliest_datetime, get_last_datetime

def predict_regression(regression_params, modelType, dt_min=None, dt_max=None):
	'''Predicts the usage of ingredients according to our regression model
	Args: 
		regression_params - the parameters for oyur model
		modelType - the type of model you're using
		date range - the two dates that you want to predict the regression for
	Returns: 
		mealUsage - a dictionary of meals with associated usage amounts
	'''
	if dt_min is None and dt_max is None:
		dt_min = get_earliest_datetime()
		dt_max = get_last_datetime()
	elif dt_min is None:
		dt_min = get_earliest_datetime()
	elif dt_max is None:
		dt_max = get_last_datetime()
	elif timedelta.total_seconds(dt_max - dt_min) < 0:
		raise ValueError("Max datetime must be greater than min datetime")
	
	dt_delta = dt_max - dt_min
	total_hours = dt_delta.days*24 + floor(dt_delta.seconds/3600)
	mealUsage = {}
	mealsParams = regression_params
	for i in range(total_hours):
		for meal_key in mealsParams:
			current_dt = dt_min + timedelta(hours=i)
			dt_array = np.array([current_dt.hour, current_dt.day, current_dt.month])
			params = mealsParams[meal_key]
			if meal_key in mealUsage:
				if modelType == 'Polynomial':
					mealUsage[meal_key] += polynomialModel(dt_array, *params)
				elif modelType == 'Sinusoidal':
					mealUsage[meal_key] += sinusoidalModel(dt_array, *params)
			else:
				if modelType == 'Polynomial':
					mealUsage[meal_key] = polynomialModel(dt_array, *params)
				elif modelType == 'Sinusoidal':
					mealUsage[meal_key] = sinusoidalModel(dt_array, *params)

	for meal_key in mealUsage:
		mealUsage[meal_key] = int(round(mealUsage[meal_key]))

	return mealUsage

	
