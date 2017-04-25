'''DataController - This is used to get relevant data for the model controller.'''
import random
from calendar import monthrange
from math import ceil, floor
from datetime import datetime, timedelta, date, time
from chefboyrd.models import Orders, Tabs, Meals, Ingredients, MealIngredients, Quantities
from hashids import Hashids
from peewee import fn

hashids = Hashids() # does this result in different encode and decodes?s

def get_orders_date_range(dt_min=None, dt_max=None):
    '''Gets a range of orders from one datetime to another datetime joined on Tabs.

    If dt_min is None then all orders less than max will be returned.
    If dt_max is None then all orders greater than dt_min is returned
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

def get_dollars_in_range(dt_min, dt_max):
    '''Returns the total sum of revenue from a range of dates'''
    meals = Orders.select().join(Meals).switch(Orders).join(Tabs).where(Tabs.timestamp >= dt_min,
                                                                        Tabs.timestamp <= dt_max)
    tot = 0
    for order in meals:
        tot += order.meal.price
    return tot

def get_meals_in_range(dt_min, dt_max):
    '''Returns the total sum of meals from a range of datetimes

    Args:
        dt_min (datetime): Starting datetime
        dt_max (datetime): Ending datetime
    Returns:
        int: The total number of meals served in the range.

    '''
    meals = get_orders_date_range(dt_min, dt_max)
    return len(meals)


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


def generate_data(num_days=10, num_tabs=50, order_per_tab=3, dt_start=None):
    '''Generates and stores data for the models in chefboyrd.models.statistics

    Notes:
      - Opening time is 7AM
      - Closing time is 10PM
      - Tabs are generated throughout the day UNEVENLY. Orders increase during the evening

    Args:
        num_days (int): default=10, The number of days to generate data for
        num_tabs (int): default=50, The average number of tabs per day
        order_per_tab (int): default=3, Number of orders which exist on each tab
        dt_start (datetime): default=(datetime.now()), The datetime to start creating orders

    Returns:
        int: The number of new orders created in the DB.
    '''
    # Populate necessary tables
    for item in menu:
        # 1. Add meal to meals table w/ price
        # 2. Add the ingredient to ingredients table
        # 3. Add the quantity to quantities table
        # 4. Add the MealIngredients after getting the ingredient ID and quanitity ID
        meal = Meals.get_or_create(name=item, price=menu[item]['price'])[0]
        for ingredient in menu[item]['ingredients']:
            qna = menu[item]['ingredients'][ingredient].strip().split('=')
            ingredient = Ingredients.get_or_create(name=ingredient)[0]
            quant = Quantities.get_or_create(name=qna[1])[0]
            m_ingr = MealIngredients.get_or_create(meal_id=meal.get_id(),
                                                   ingredient_id=ingredient.get_id(),
                                                   quantity_meas_id=quant.get_id(),
                                                   quantity_amt=qna[0])
    
    # Database tables are now properly populated with menu items, ingredients, prices, etc..
    # Now we need to create a number of tabs with each tab having 1 to n different orders.
    # This will simulate a real restaurant.
    if dt_start is None:
        dt_start = datetime.now()
    
    for day in range(num_days):
        tab_date = dt_start + timedelta(days=day)
        
        for tab in range(int(clamp_rng(random.gauss(num_tabs, 2), 1, 20000000))):
            # Create tab here
            tab_time = time(hour=int(clamp_rng(random.gammavariate(60.25, .1991701244813278), 6, 21)),
                            minute=random.randint(0, 59))
            tab_dt = datetime(year=tab_date.year,
                              day=tab_date.day,
                              month=tab_date.month,
                              hour=tab_time.hour,
                              minute=tab_time.minute)
            num_orders = int(clamp_rng(abs(random.gauss(order_per_tab, 1)), 1, 200)) #rng w/ mean of order_per_tab
            tab = Tabs.create(timestamp=tab_dt, had_reservation=randbool(), party_size=num_orders, 
                fb_key= hashids.encode(int ( (tab_dt - datetime(1970, 8, 15, 6, 0, 0 )).total_seconds())))
            for order in range(num_orders):
                # Pick a random meal
                mealname = list(menu.keys())[random.randint(0, len(menu)-1)]
                meal = Meals.select().where(Meals.name == mealname)[0]
                # Add the order with the meal
                new_meal = Orders.create(meal=meal.get_id(), tab=tab.get_id())

def randbool():
    return random.gauss(0, 1) >= 0

def clamp_rng(num, lo, hi):
    '''Forces a number to fall within min/max range by doing lo + (num % (hi-lo))

    Hi and lo should always be positive.
    If num is < 0 then we take its absolute value and clamp that.
    '''
    return lo + (abs(num) % (hi-lo))

menu = {
        'hamburger': {
            'price': 8.99,
            'ingredients': {
                'beef': '2=patty',
                'bun': '1=bun',
                'lettuce': '2=leaves',
                'ketchup': '2=teaspoon',
                'mustard': '2=teaspoon'
            }
        },
        "cheeseburger": {
            'price': 9.99,
            'ingredients': {
                'beef': '2=patty',
                'bun': '1=bun',
                'lettuce': '2=leaves',
                'ketchup': '2=teaspoon',
                'mustard': '2=teaspoon',
                'cheddar cheese': '2=slices'
            }

        },
        'bacon burger': {
            'price': 11.99,
            'ingredients': {
                'beef': '2=patty',
                'bun': '1=bun',
                'lettuce': '2=leaves',
                'ketchup': '2=teaspoon',
                'mustard': '2=teaspoon',
                'cheddar cheese': '2=slices',
                'bacon': '4=strips'
            }
        },
        'cheesesteak': {
            'price': 10.99,
            'ingredients': {
                'beef': '8=oz',
                'bun': '1=hoagie roll',
                'cheddar cheese': '2=slices',
                'onions': '0.25=onion'
            }
        },
        'blt': {
            'price': 6.75,
            'ingredients': {
                'bread': '2=slices',
                'bacon': '4=strips',
                'lettuce':'2=leaves'
            }
        },
        'hoagie': {
            'price': 6.50,
            'ingredients': {
                'bun': '1=hoagie roll',
                'salami': '4=slices',
                'capicola': '4=slices',
                'provolone cheese': '4=slices',
                'onion': '0.5=onion',
                'lettuce': '2=cup',
                'tomato': '1=tomato'
            }
        },
        'french fries': {
            'price': 3.85,
            'ingredients': {
                'potato': '0.5=lb',
                'salt': '1=teaspoon'
            }
        },
        'onion rings': {
            'price': 4.15,
            'ingredients': {
                'onion': '1=onion',
                'salt': '0.25=teaspoon'
            }
        },
        'grilled cheese': {
            'price': 4.50,
            'ingredients': {
                'bread':'2=slices',
                'cheese':'2=slices'
            }
        },
        'tuna sandwich': {
            'price': 5.50,
            'ingredients': {
                'tuna fish': '1=can',
                'bun':'1=hoagie roll',
                'mayo': '2=teaspoon',
                'salt': '0.25=teaspoon'
            }
        },
        'chicken quesadilla': {
            'price': 6.99,
            'ingredients': {
                'butter': '1=tablespoon',
                'tortilla': '1=tortilla',
                'chicken': '1=lb',
                'salsa': '1=cup',
                'sour cream': '4=tablespoon'
            }
        },
        'turkey sandwich': {
            'price': 6.99,
            'ingredients': {
                'turkey': '0.5=lb',
                'mayo': '2=teaspoon',
                'bread': '2=slices',
                'pepper': '0.5=teaspoon'
            }
        },
        'ceasar wrap': {
            'price': 5.99,
            'ingredients': {
                'ceasar dressing': '2=tablespoon',
                'tortilla': '1=tortilla',
                'chicken': '0.35=lb',
                'lettuce': '0.5=cup'
            }
        },
        'pizza steak': {
            'price': 7.99,
            'ingredients': {
                'cheddar cheese': '0.5=cup',
                'mozzarella cheese': '0.5=cup',
                'bun': '1=hoagie roll',
                'tomato sauce': '0.25=cup',
                'steak': '1=steak'
            }
        },
        'pulled pork': {
            'price': 14.99,
            'ingredients': {
                'pork': '1=lb',
                'spices': '0.5=tablespoon',
                'potatoes': '1=lb',
                'barbecue sauce': '0.3=cup'
            }
        },
        'steak': {
            'price': 17.99,
            'ingredients': {
                'steak':'2=lb',
                'potatoes': '2=cups',
                'A1': '0.25=cup',
                'salt':'0.25=teaspoon',
                'pepper': '0.3=teeaspoon'
            }
        },
        'buffalo chicken cheesesteak': {
            'price': 9.99,
            'ingredients': {
                'chicken': '8=oz',
                'bun': '1=hoagie roll',
                'mozzarella cheese': '2=slices',
                'onions': '0.25=onion',
                'buffalo sauce': '0.25=cup'
            }
        },
        'roast beef sandwich': {
            'price': 8.99,
            'ingredients': {
                'roast beef': '1=lb',
                'mayo': '0.25=cup',
                'mustard': '0.2=cup',
                'onion': '0.3=onion'
            }
        },
        'chicken parmesan sandwich': {
            'price': 11.99,
            'ingredients': {
                'chicken': '8=oz',
                'bun': '1=hoagie roll',
                'mozzarella cheese': '2=slices',
                'tomato sauce': '0.5=cup'
            }
        },
        'spaghetti and meatballs': {
            'price': 0.99,
            'ingredients': {
                'spaghetti': '2.0=cup',
                'tomato sauce': '0.5=cup',
                'meatballs': '3=meatball'
            }
        },
        'rock sandwich': {
            'price': 1.0,
            'ingredients': {
                'chicken': '6=oz',
                'buffalo sauce': '0.25=cup',
                'bun': '1=hoagie roll'
            }
        }
    }