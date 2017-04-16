'''Main file to register blueprints and run the flask application

This is where most of the app setup is done. We shouldn't have to modify this file except
for two different cases:

    1. We are adding new views to the application
    2. We are adding new models to the application

Otherwise this file should not be touched.

Every view which is to be part of the app must be registered appropriately using:

    APP.register_blueprint(viewpage, ...)

Other args to register_blueprint might include the url_prefix if you want your pages to reside on
a specific path.

If models are being added we just need to make sure the corresponding tables are created (if they
don't already exist) when starting the application. We do this by making the call

    model.create_table(True)

The ``True`` argument forces any failures to be silent when creating the table - i.e. not crash
the application. Other than that we shouldn't need to add much else to this file.

Please see the following files for examples of each part of the MVC structure of this project

- Model ==> models/customers.py
- View ==> views/root.py
- Controller ==> controllers/customer_controller.py

Other helpful sources of documentaiton and reading:

- http://docs.peewee-orm.com/en/latest/index.html
- https://github.com/coleifer/peewee (See example apps at the bottom of the readme)
- http://flask.pocoo.org/docs/0.12/blueprints/



'''

import configparser
import flask_login
from flask import Flask, render_template
from peewee import SqliteDatabase, fn
from datetime import datetime, timedelta


def init_db(dbname):
    global DB
    DB = SqliteDatabase(dbname)

CONF = configparser.ConfigParser()
CONF.read('config.ini')

init_db(CONF['database']['dbfile'])

APP = Flask(__name__, template_folder="views/templates", static_url_path='/static')
APP.secret_key = 'ENG-</rutgers-chefboyrd?>-<oij!$9ui%^98A*FSD>@2018!'

LM = flask_login.LoginManager()
LM.init_app(APP)
import chefboyrd.auth # register the login and authentication functions

@APP.before_request
def before_request():
    """Connect to the database before each request."""
    try:
        DB.connect()
    except:
        pass


@APP.after_request
def after_request(response):
    """Close the database connection after each request."""
    try:
        DB.close()
    except:
        pass
    return response


# Register all views after here
# =======================
from chefboyrd.auth import auth_pages
from chefboyrd.views import root, stat_dash, reservationH, table_manager, feedbackM, prediction_dash, feedbackC, settings

APP.register_blueprint(root.page, url_prefix='/test')
APP.register_blueprint(stat_dash.page, url_prefix='/dashboard')
APP.register_blueprint(auth_pages, url_prefix='/auth')
APP.register_blueprint(reservationH.page, url_prefix='/reservationH')
APP.register_blueprint(table_manager.page, url_prefix='/table_manager')
APP.register_blueprint(feedbackM.page, url_prefix='/feedbackM')
APP.register_blueprint(prediction_dash.page, url_prefix='/prediction')
APP.register_blueprint(feedbackC.page, url_prefix='/feedbackC')
APP.register_blueprint(settings.page, url_prefix='/settings')

# Put all table creations after here
# ==================================
from chefboyrd.models import Meals, Ingredients, MealIngredients, Quantities, Tabs, Orders
from chefboyrd.models import customers, user, reservation, tables, sms, Customer, User

Customer.create_table(True)
User.create_table(True)

Meals.create_table(True)
Ingredients.create_table(True)
MealIngredients.create_table(True)
Quantities.create_table(True)
Tabs.create_table(True)
Orders.create_table(True)

sms.Sms.create_table(True)
reservation.Reservation.create_table(True)
tables.Restaurant.create_table(True)
tables.Table.create_table(True)
tables.Booking.create_table(True)

# ==================================== Universal Routes ======================================== #
@APP.route('/')
def index():
    ''''Renders the default template'''
    if flask_login.current_user.is_authenticated:
        return render_template('default.html',
                               message='Hello {}'.format(flask_login.current_user.name),
                               logged_in=True)
    else:
        return render_template('default.html',logged_in=False)

# =============================================================================================== #


try:
    # Test User:
    # email: zac
    # Password: zac
    User.create_user('zac', 'zac', 'zac', 'admin')
except:
    pass

# try:
#     # Test User:
#     # email: zac
#     # Password: zac 
#     tables.Restaurant.create_restaurant('Pizzeria Vesuvio','Traditional pizza of Napoli',9,23)
# except:
#     pass

# try:
#     # Test User:
#     # email: zac
#     # Password: zac 
#     if tables.Table.select().count() < 1:
#         tables.Table.create_tables(1,5, 0,0.5, 0.5)
# except:
#     pass

try:
    # Test User:
    # email: zac
    # Password: zac 
    user.User.create_user('bcs', 'bcs', 'bcs', 'admin')
except:
    pass

# try:
#     # Test User:
#     # email: zac
#     # Password: zac 
#     if tables.Booking.select().count() < 1:
#         tables.Booking.create_booking(1,6,datetime(2017, 2, 14, 19, 0),datetime(2015, 2, 14, 19, 1),'Brandon','732-333-5555')
# except:
#     pass

try:
    # email: caz, pw: caz
    User.create_user('caz', 'caz', 'caz', 'notanadmin')
except:
    pass

try:
    User.create_user('admin','admin','admin','admin')
except:
    pass


from chefboyrd.controllers import data_controller, feedback_controller
if Orders.select().count() < 1000:
    start_date = datetime.now() - timedelta(days=15)
    data_controller.generate_data(num_days=15, num_tabs=45, dt_start=start_date)
try:
    feedback_controller.update_db() #updates the database with current text messages stored in twilio rest client
except:
    print("Cannot update")