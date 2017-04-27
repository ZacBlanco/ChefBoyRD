"""Rating.py
Contains the Rating model, submitted by customers through the online interface
"""
"""
written by: Seo Bo Shim, Jarod Morin
tested by: Seo Bo Shim
debugged by: Seo Bo Shim
"""

from peewee import TextField, DateTimeField, Model, IntegerField
from chefboyrd.models import BaseModel

class Rating(Model):
    """ A model for restaurant ratings that have a numerical value between 0 and 5.
    """
    submission_time = DateTimeField()
    
    food = IntegerField()
    service = IntegerField()
    clean = IntegerField()
    ambience = IntegerField()
    overall = IntegerField()
