'''DataController - This is used to get relevant data for the model controller.'''
from datetime import datetime, timedelta
from chefboyrd.models import Orders, Tabs, Meals
from peewee import JOIN

def get_orders_date_range(dt_min=None, dt_max=None):
    '''Gets a range of orders from one datetime to another datetime joined on Tabs.

    If dt_min is None then all orders less than max will be returned.
    If dt_max is None then all orders greater than dt_min is None
    If both are none then all orders are returned.

    Args:
        dt_min (datetime): A datetime object for the range to begin at. (Inclusive)
        dt_max (datetime): A datetime object for the range end begin at. (Inclusive)

    Returns:
        list: A list of order models (peewee set).
    '''
    ords = None
    if dt_min is None and dt_max is None:
        ords = Orders.select()
    elif dt_min is None:
        ords = Orders.select().join(Tabs).where(Tabs.timestamp <= dt_max)
    elif dt_max is None:
        ords = Orders.select().join(Tabs).where(Tabs.timestamp >= dt_min)
    elif timedelta.total_seconds(dt_max - dt_min) < 0:
        raise ValueError("Max datetime must be greater than min datetime")
    else:
        ords = Orders.select().join(Tabs).where(Tabs.timestamp >= dt_min,
                                                           Tabs.timestamp <= dt_max)
    return ords

def get_tabs_range(dt_min=None, dt_max=None):
    '''Gets a range of tabs from one datetime to another datetime

    If dt_min is None then all tabs less than max will be returned.
    If dt_max is None then all tabs greater than dt_min is None
    If both are none then all tabs are returned.

    Args:
        dt_min (datetime): A datetime object for the range to begin at. (Inclusive)
        dt_max (datetime): A datetime object for the range end begin at. (Inclusive)

    Returns:
        list: A list of order models (peewee set).
    '''
    tabs = None
    if dt_min is None and dt_max is None:
        tabs = Tabs.select()
    elif dt_min is None:
        tabs = Tabs.select().where(Tabs.timestamp <= dt_max)
    elif dt_max is None:
        tabs = Tabs.select().where(Tabs.timestamp >= dt_min)
    elif timedelta.total_seconds(dt_max - dt_min) < 0:
        raise ValueError("Max datetime must be greater than min datetime")
    else:
        tabs = Tabs.select().where(Tabs.timestamp >= dt_min, Tabs.timestamp <= dt_max)
    return tabs

def get_dotw_orders():
    '''Gets all orders on a given day of the week'''
    pass

def get_dollars_in_range():
    '''Returns the total sum of revenue from a range of dates'''
    pass

def people_in_range():
    '''Returns the total number of people served in a range of dates'''
    pass

def get_reservations_on_dotw():
    '''Gets the number of reservations on a given day of the week.'''
    pass