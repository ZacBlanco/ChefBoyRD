'''Statistics dashboard for the manager interface


Will be able to render dashboards which include statistics from the database
of the Point of sale system and other data systems for the business.
'''
import sys
import base64
from datetime import datetime, timedelta
import logging
from io import BytesIO
from flask import Blueprint, render_template, abort, request, flash
from jinja2 import TemplateNotFound
from peewee import JOIN_LEFT_OUTER, JOIN
from chefboyrd.auth import require_role
from chefboyrd.models import Orders, Meals, Ingredients, Tabs, MealIngredients
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from chefboyrd.controllers import data_controller
from urllib.parse import quote

logger = logging.getLogger(__name__)


page = Blueprint('dashboard', __name__, template_folder='./templates')

def get_datauri(fig):
    '''Build an image data URI '''
    canvas = FigureCanvas(fig)
    imgdata = BytesIO()
    canvas.print_png(imgdata)
    imgdata.seek(0)
    data = base64.b64encode(imgdata.getvalue())
    data_url = 'data:image/png;base64,{}'.format(quote(data))
    return data_url

def create_jinja_object(fig):
    graph = {
        'width': fig.get_figwidth()*fig.get_dpi()/1.25,
        'height': fig.get_figheight()*fig.get_dpi()/1.25,
        'img': get_datauri(fig)
    }
    return graph    

@page.route("/", methods=['GET', 'POST'])
@require_role('admin') # Example of requireing a role(and authentication)
def dash_index():
    '''Renders the index page of the dashboards
    '''
    # Logged in always true because we require admin role
    graphs = []
    options = []
    date_min = None
    date_max = None
    if request.method == "POST":
        try:
            start = [int(x) for x in request.form.get('startdate').split('-')]
            date_min = datetime(year=start[0], month=start[1], day=start[2])
        except BaseException as er:
            logger.warning(er)
        try:
            end = [int(x) for x in request.form.get('enddate').split('-')]
            date_max = datetime(year=end[0], month=end[1], day=end[2])
        except BaseException as er:
            logger.warning(er)
        if date_min is not None and date_max is not None:
            if date_min > date_max:
                flash('Start Date must be strictly before End Date')
                return render_template('/dashboard/index.html', logged_in=True)
    if date_max is None:
        date_max = datetime.today()
    if date_min is None:
        date_min = date_max - timedelta(days=5)
    if request.args.get('type', default='') == 'Meals':
        options = list(data_controller.menu.keys())
        fig = Figure()
        ax1 = fig.add_subplot(1, 1, 1)
        if request.method == 'POST':
            orders = data_controller.get_orders_date_range(date_min, date_max)
            orders = orders.switch(Orders).join(Meals).where(Meals.name == request.form.get('selector'))
            
            ords = []
            orddays = []
            for order in orders:
                ords.append(order.tab.timestamp.hour)
                orddays.append(order.tab.timestamp.day)
            if date_min is not None and date_max is not None:
                fig.suptitle('Plot of {} for {} to {} on Hours of the Day'.format(request.form.get('selector'), date_min.date(), date_max.date()))
            else:
                fig.suptitle('Plot for {} over Hours of the Day'.format(request.form.get('selector')))
            ax1.hist(ords, bins=list(range(24)))
            ax1.set_xlabel('Hours')
            ax1.set_ylabel('Count')
            graphs.append(create_jinja_object(fig))
            fig2 = Figure()
            ax2 = fig2.add_subplot(1, 1, 1)
            ax2.hist(orddays)
            fig.suptitle('Plot of {} Over All Days'.format(request.form.get('selector')))
            ax2.set_xlabel('Days')
            ax2.set_ylabel('Count')
            graphs.append(create_jinja_object(fig2))
    elif request.args.get('type', default='') == 'Ingredients':
        options = [x.name for x in Ingredients.select()]
        # Get a specific ingredient used over a timespan
        # Show 2 graph - hourly usage (overall)
        # and daily usage.
        ingred = request.form.get('selector')
        if request.method == 'POST':
            if not request.form.get('selector') in options and request.method == 'POST':
                flash('That ingredient does not exist.')
            else:
                # We have all orders - we need to filter by specific ingredient.
                # Must join on Meals, then Ingredients. Then filter on where
                # Ingredient.name == parameter
                ingredient = Ingredients.select().where(Ingredients.name == ingred)[0]

                orders = (Orders.select(Orders, MealIngredients, Tabs)
                        .join(Tabs).switch(Orders)
                        .join(MealIngredients, on=(MealIngredients.meal_id == Orders.meal).alias('ingredient'))
                        .where((MealIngredients.ingredient_id == ingredient.get_id()) &
                                (Tabs.timestamp >= date_min) &
                                (Tabs.timestamp <= date_max)))
                quantities = [0]*24
                days = [0]*(date_max-date_min).days
                for order in orders:
                    hr = order.tab.timestamp.hour
                    day = (order.tab.timestamp - date_min).days
                    quantities[hr] += order.ingredient.quantity_amt
                    days[day] += order.ingredient.quantity_amt
                print(quantities)
                print(days)

                qfig = Figure()
                ax1 = qfig.add_subplot(1, 1, 1)
                ax1.bar(range(len(quantities)), quantities)
                qfig.suptitle("{} Used Per Hour from {} to {}".format(ingred, date_min.date(), date_max.date()))
                ax1.set_xlabel('Hours')
                ax1.set_ylabel('Amount')
                
                dfig = Figure()
                ax1 = dfig.add_subplot(1, 1, 1)
                ax1.bar([(x*1.0) for x in range(len(days))], days, align='center')
                ax1.set_xticks([(x*1.0) for x in range(len(days))])
                ax1.set_xticklabels((date_min + timedelta(days=x)).date() for x in range((date_max-date_min).days))
                dfig.suptitle("{} Used Per Day from {} to {}".format(ingred, date_min.date(), date_max.date()))
                ax1.set_xlabel('Days')
                ax1.set_ylabel('Amount')

                graphs.append(create_jinja_object(qfig))
                graphs.append(create_jinja_object(dfig))
    elif request.args.get('type', default='') == 'Performance':
        if request.method == "POST":
            if date_max is None:
                date_max = datetime.today()
            if date_min is None:
                date_min = date_max - timedelta(days=5)
            
            day_diff = date_max - date_min
            for date in range(day_diff.days):
                curr_date = date_min + timedelta(days=date)
                # create graphs for the last 10 days, otherwise create a graph for every day in the timedelta
                figure = Figure()
                ax1 = figure.add_subplot(1, 1, 1)
                ords = []
                orders = data_controller.get_orders_date_range(date_min-timedelta(days=1), date_max).where(Tabs.timestamp.day == curr_date.date().day)
                for order in orders:
                    ords.append(order.tab.timestamp.hour)
                ax1.hist(ords)
                figure.suptitle("Business activity for {}".format(curr_date.date()))
                ax1.set_xlabel('Hours')
                ax1.set_ylabel('Parties Served')
                graphs.append(create_jinja_object(figure))
    elif request.args.get('type', default='') == 'Tabs':
        options = ['Tables Served', 'Reservations']
        if request.method == "POST":
            if date_max is None:
                date_max = datetime.today()
            if date_min is None:
                date_min = date_max - timedelta(days=5)
            
            day_diff = date_max - date_min
            if request.form.get('selector') == options[0]:
                for date in range(day_diff.days):
                    curr_date = date_min + timedelta(days=date)
                    figure = Figure()
                    ax1 = figure.add_subplot(1, 1, 1)
                    ords = []
                    tabs = data_controller.get_tabs_range(date_min-timedelta(days=1), date_max).where(Tabs.timestamp.day == curr_date.date().day)
                    for tab in tabs:
                        ords.append(tab.timestamp.hour)
                    ax1.hist(ords)
                    figure.suptitle("Tables Served on for {}".format(curr_date.date()))
                    ax1.set_xlabel('Hours')
                    ax1.set_ylabel('Count')
                    graphs.append(create_jinja_object(figure))
            elif request.form.get('selector') == options[1]:
                for date in range(day_diff.days):
                    curr_date = date_min + timedelta(days=date)
                    figure = Figure()
                    ax1 = figure.add_subplot(1, 1, 1)
                    ords = [0, 0]
                    tabs = data_controller.get_tabs_range(date_min-timedelta(days=1), date_max).where(Tabs.timestamp.day == curr_date.date().day)
                    for tab in tabs:
                        if tab.had_reservation:
                            ords[0] += 1
                        else:
                            ords[1] += 1
                    
                    ax1.set_xticks([0.425, 0.425+0.85])
                    ax1.set_xticklabels(('Yes', 'No'))
                    ax1.bar(range(len(ords)), ords)
                    figure.suptitle("Total Reservations on {}".format(curr_date.date()))
                    ax1.set_xlabel('Hours')
                    ax1.set_ylabel('Count')
                    graphs.append(create_jinja_object(figure))
    elif request.args.get('type', default='') == 'Revenue':
        options = [x.name for x in Ingredients.select()]
        # Show revenue over x days
        orders = data_controller.get_orders_date_range(date_min, date_max)
        hrly_rev = [0]*24
        daily_rev = [0]*(date_max-date_min).days
        for order in orders:
            hr = order.tab.timestamp.hour
            day = (order.tab.timestamp - date_min).days
            hrly_rev[hr] += order.meal.price
            daily_rev[day] += order.meal.price
        
        qfig = Figure()
        ax1 = qfig.add_subplot(1, 1, 1)
        ax1.bar(range(len(hrly_rev)), hrly_rev, align='center')
        qfig.suptitle("Dollars per Hour from {} to {}".format(date_min.date(), date_max.date()))
        ax1.set_xlabel('Hours')
        ax1.set_ylabel('Dollars')
        
        dfig = Figure()
        ax1 = dfig.add_subplot(1, 1, 1)
        ax1.bar([(x*1.0) for x in range(len(daily_rev))], daily_rev, align='center')
        ax1.set_xticks([(x*1.0) for x in range(len(daily_rev))])
        ax1.set_xticklabels((date_min + timedelta(days=x)).date() for x in range((date_max-date_min).days))
        dfig.suptitle("Dollars per Day from {} to {}".format(date_min.date(), date_max.date()))
        ax1.set_xlabel('Days')
        ax1.set_ylabel('Dollars')

        graphs.append(create_jinja_object(qfig))
        graphs.append(create_jinja_object(dfig))
    else:
        pass
    return render_template('/dashboard/index.html', options=options, logged_in=True, graphs=graphs)
