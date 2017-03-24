'''DataController - This is used to get relevant data for the model controller.'''
from datetime import datetime, timedelta, date
from chefboyrd.models import Orders, Tabs, Meals
from peewee import JOIN

def get_meals(dt_min=None, dt_max=None):
    ''' Gets a range of meals from one datetime to another datetime joined on Tabs
    
    If dt_min is None then all orders less than max will be returned.
    If dt_max is None then all orders greater than dt_min is None
    If both are none then all orders are returned.

    Args:
        dt_min (datetime): A datetime object for the range to begin at. (Inclusive)
        dt_max (datetime): A datetime object for the range end begin at. (Inclusive)

    Returns:
        iterable: An iterable of order models (peewee set).
    '''
    meals = None
    if dt_min is None and dt_max is None:
        meals = Meals.select()
    elif dt_min is None:
        meals = Meals.select().join(Tabs).where(Meals.timestamp <= dt_max)
    elif dt_max is None:
        meals = Meals.select().join(Tabs).where(Meals.timestamp >= dt_min)
    elif timedelta.total_seconds(dt_max - dt_min) < 0:
        raise ValueError("Max datetime must be greater than min datetime")
    else:
        meals = Meals.select().join(Tabs).where(Meals.timestamp >= dt_min, Meals.timestamp <= dt_max)
    return meals

def get_orders_date_range(dt_min=None, dt_max=None):
    '''Gets a range of orders from one datetime to another datetime joined on Tabs.

    If dt_min is None then all orders less than max will be returned.
    If dt_max is None then all orders greater than dt_min is None
    If both are none then all orders are returned.

    Args:
        dt_min (datetime): A datetime object for the range to begin at. (Inclusive)
        dt_max (datetime): A datetime object for the range end begin at. (Inclusive)

    Returns:
        iterable: An iterable of order models (peewee set).
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
        iterable: An iterable of order models (peewee set).
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

def get_dotw_orders(dotw):
    '''Gets all orders on a given day of the week
    
    Interesting challenge because we only have a datetime value.
    Args:
        dotw (int): An integer representing the day of the week. 0 for Monday, 6 for Sunday.
    
    Returns:
        list: A list of all order models on a given day of the week.
    '''
    if dotw < 0 or dotw > 6:
        raise ValueError("DoTW {} is not in the valid range of [0, 6]".format(dotw))
    
    ords = []
    orders = Orders.select()
    for order_t in orders:
        order = order_t.tab
        if date(order.timestamp.year, order.timestamp.month, order.timestamp.day).weekday() == dotw:
            ords.append(order)
    return ords


def get_dollars_in_range(dt_min=None, dt_max=None):
    '''Returns the total sum of revenue from a range of dates'''
    meals = get_meals(dt_min, dt_max)
    sum = 0
    for meal in meals:
        sum += meal.price
    return sum

def people_in_range(dt_min=None, dt_max=None):
    '''Returns the total number of people served in a range of dates'''
    tabs = get_tabs_range(dt_min, dt_max)
    total_people = 0
    for tab in tabs:
        total_people += tab.party_size
    return total_people

def get_reservations_on_dotw(dotw):
    '''Gets the number of reservations on a given day of the week.'''
    if dotw < 0 or dotw > 6:
        raise ValueError("DoTW {} is not in the valid range of [0, 6]".format(dotw))

    num_reservations = 0
    orders = Orders.select()
    for order_t in orders:
        order = order_t.tab
        if date(order.timestamp.year, order.timestamp.month, order.timestamp.day).weekday() == dotw and order.had_reservation:
            num_reservations += 1
    return num_reservations