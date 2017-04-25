''' Prediction dashboard for the manager interface


Will allow you to predict ingredient usage between two chosen dates
'''
import urllib, base64
from datetime import datetime, timedelta
import logging
from io import BytesIO
from flask import Blueprint, render_template, abort, request, flash
from jinja2 import TemplateNotFound
from peewee import JOIN_LEFT_OUTER, JOIN
from chefboyrd.auth import require_role
from chefboyrd.models import Orders, Meals, Ingredients, Tabs, MealIngredients
from chefboyrd.controllers import data_controller
from chefboyrd.controllers import model_controller
from chefboyrd.controllers import prediction_controller
import dateutil.parser

logger = logging.getLogger(__name__)


page = Blueprint('prediction', __name__, template_folder='./templates')

@page.route("/", methods=['GET', 'POST'])
@require_role('admin')
def prediction_index():
	'''Renders the index page of the prediction page
	'''
	beginningDate = None
	endingDate = None
	mealUsage = None
	if request.method == "POST":
		try:
			print(request.form.get('beginningDate'))
			beginningDate = dateutil.parser.parse(request.form.get('beginningDate'))
		except BaseException as er:
			logger.warning(er)
		try:
			print(request.form.get('endingDate'))
			endingDate = dateutil.parser.parse(request.form.get('endingDate'))
		except BaseException as er:
			logger.warning(er)
		if beginningDate is not None and endingDate is not None:
			if beginningDate > endingDate:
				flash('Start Date must be strictly before End Date')
				return render_template('/prediction/index.html', logged_in=True, meals=mealUsage)

		modelType = 'Polynomial'

		orders = data_controller.get_orders_date_range()
		#print(list(orders))
		processedOrders = model_controller.orders_to_list(orders)
		#print(processedOrders)
		mainParams = None
		try:
			mainParams = model_controller.train_regression(processedOrders, modelType)
		except RuntimeError:
			try:
				mainParams = model_controller.train_regression(processedOrders, 'Sinusoidal')
			except RuntimeError:
				flash('Unable to predict meal usage with given data')
				return render_template('/prediction/index.html', logged_in=True, meals=mealUsage)
		except TypeError:
			return render_template('/prediction/index.html', logged_in=True, meals=mealUsage)

		#print(mainParams)
		mealUsage = prediction_controller.predict_regression(mainParams, modelType, beginningDate, endingDate)
		# Check if values were good
		if mealUsage is None:
			flash('The predicted values are unsuited for the specified date range. Pick a better date range.')
		#print(mealUsage)

	return render_template('/prediction/index.html', logged_in=True, meals=mealUsage)


