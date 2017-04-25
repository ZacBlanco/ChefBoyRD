'''This module contains all of the peewee model classes which correspond to order statistics. They
will be used to make predictions and display data about business revenue and growth.
'''
from peewee import CharField, FloatField, BooleanField, IntegerField, DateTimeField, ForeignKeyField, TextField
from chefboyrd.models import BaseModel
from datetime import datetime, timedelta
# from chefboyrd.models.models.prediction import Meal, Tab, MealIngredients, Ingredients, Quantities

'''
Note on missing "ID" fields on models:
    When using peewee, if no `primary_key` is specified then peewee automatically creates an 'id'
    field which is unique and autoincrements. For this reason ID fields are omitted on models
    which require unique IDs
'''

class Meals(BaseModel):
    '''A model for restaurant meals'''
    price = FloatField()
    name = CharField(unique=True)

class Tabs(BaseModel):
    '''A model for a tab - i.e. a list of meals or items ordered at a given table.'''
    had_reservation = BooleanField()
    party_size = IntegerField()
    timestamp = DateTimeField()
    fb_key = TextField()

class Ingredients(BaseModel):
    '''A table which maps ingredient names to ingredient ID's'''
    name = CharField(unique=True)

class Quantities(BaseModel):
    '''A table mapping quantities names to quantity Id's'''
    name = CharField(unique=True)

class MealIngredients(BaseModel):
    '''A table mapping a meal to the ingredients used'''
    meal_id = ForeignKeyField(Meals)
    ingredient_id = ForeignKeyField(Ingredients)
    quantity_meas_id = ForeignKeyField(Quantities)
    quantity_amt = FloatField()

class Orders(BaseModel):
    '''A model for storing every meal ordered and providing mappings to the tabs to meals'''
    meal = ForeignKeyField(Meals)
    tab = ForeignKeyField(Tabs) # ID is a unique timestamp
