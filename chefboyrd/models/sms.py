"""Contains the SMS model. Feedback submitted

written by: Seo Bo Shim, Jarod Morin
tested by: Seo Bo Shim
debugged by: Seo Bo Shim
"""

from peewee import TextField, DateTimeField, Model, IntegerField, BooleanField
from chefboyrd.models import BaseModel

class Sms(BaseModel):
    """ A model for SMS objects to be stored and analyzed. The many flags hold a range of values between -1 and 1
    """
    sid = TextField(unique=True)
    submission_time = DateTimeField() 
    body = TextField()
    phone_num = TextField()
    pos_flag = IntegerField(default=-1)
    neg_flag = IntegerField(default=-1)
    exception_flag = IntegerField(default=-1)
    food_flag = IntegerField(default=-1)
    service_flag = IntegerField(default=-1)
    invalid_field = BooleanField(default=False)
    #additional categories to associate	
