'''This is a sample blueprint for a homepage

Because we're going to have multiple views for the project we need a way to break them up easily
within our application. Flask provides us with this neat tool called blueprints where we're able
to define, essentially, chunks of our APIs or programs as blueprints with functions, then map
the predefined functions to specific routes in our application. (See the __init__.py file)
for blueprint registering.

To create a new routable location as part of the view you need to first create the blueprint for
the module. This is done with the following code

    page = Blueprint('main', __name__, template_folder='templates')

Then you can use the function decorator @page.route(...) to decorate methods in order to create
the views. See the example below. I think the code is relatively straightforward.

Read the flask documentation if you have issues. Particularly the following pages:

- http://flask.pocoo.org/docs/0.12/blueprints/
- http://flask.pocoo.org/docs/0.12/quickstart/

Dive deeper into the documentation for a better understanding of how this all works.

'''
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from chefboyrd.controllers import customer_controller, send_sms
from datetime import date

page = Blueprint('main', __name__, template_folder='templates')

@page.route('/')
def show():
    '''Render Homepage'''
    try:
        return render_template('default.html', users=customer_controller.get_customers())
    except TemplateNotFound:
        abort(404)

@page.route('/hello')
def showhello():
    '''Super basic function. Always shows "Hi"'''
    return "Hi"

@page.route('/customer/<name>')
def new_cust(name):
    '''Creates a new customer

    Args:
        name (str): String representing the name
    '''

    if customer_controller.new_customer(name):
        return render_template('default.html', users=[name])
    else:
        return render_template('default.html', users=['Failed'])

@page.route('/sms')
def sms():
    '''
    get a list of all messages sent to Twilio ever
    '''
    d  = date.today()
    send_sms.update_db()
    return 'sms'
    #send_sms.rcv_sms()

@page.route('/sendsms',methods=['POST'])
def send_sms_route():
    '''
    This is the directory we need to configure twilio for.
    When Twilio makes a POST request, db will be updated with new sms messages from today
    '''
    #print(request.url)
    send_sms.update_db(date.today())
    return 'db updated'
