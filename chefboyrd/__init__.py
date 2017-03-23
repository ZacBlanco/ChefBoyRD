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
from flask import Flask
from peewee import SqliteDatabase

def init_db(dbname):
    global DB
    DB = SqliteDatabase(dbname)

CONF = configparser.ConfigParser()
CONF.read('config.ini')

init_db(CONF['database']['dbfile'])
APP = Flask(__name__)

# Register all views after here
# =======================
from chefboyrd.views import root, sms_test
APP.register_blueprint(root.page, url_prefix='/test')
APP.register_blueprint(sms_test.page, url_prefix='/')

# Put all table creations after here
# ==================================
from chefboyrd.models import customers
from chefboyrd.models import sms
sms.Sms.create_table(True)
customers.Customer.create_table(True)
    
