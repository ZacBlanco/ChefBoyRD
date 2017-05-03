'''Customer Controller

A controller houses all functions that has to do with taking arguments
and modifying the underlying data store. The controllers also perform all
of the data analysis that might be taking place.abs

Essentially controllers are for the 'business logic' of the application.
Everything that goes here will somehow manipulate, calculate, store, modify
or learn everything that we need.

All of the data and objects that we are working with will come from the ``models``
folder. Typically each Model will have a corresponding controller which will do
all of the CRUD (create, read, update, deletion) from the database. It's really
a middle man from the flask functions to the database which contains all of the
logic.

Other controllers which aren't directly mapped to updating, reading, or writing
models might perform actions like model training (machine learning) or scheduling
jobs which may be run at specified times that aren't necessarily completely dictated
by user interaction.

Basically if you've got some code and it doesn't interact with the models or the views,
then it should be a controller.

'''
from chefboyrd.models import Customer


def new_customer(name):
    '''Create a new customer
    Args:
        name (str): the customer name

    '''
    cust = Customer(name=name)
    return True if cust.save() == 1 else False

def get_customers():
    '''Return a list with all customer names'''
    custs = []
    try:
        for cust in Customer.select():
            custs.append(cust.name)
        return custs
    except:
        return []

