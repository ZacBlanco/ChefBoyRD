"""Contains the SMS model. Feedback submitted

written by: Seo Bo Shim, Jarod Morin
tested by: Seo Bo Shim
debugged by: Seo Bo Shim
"""

from peewee import TextField, DateTimeField, Model, IntegerField, BooleanField
from chefboyrd.models import BaseModel

class Sms(BaseModel):
    """ A model for SMS objects to be stored and analyzed. The many flags hold a range of values between -1 and 1

    Attributes:
        sid: is an unique id assigned by twilio. it will help us keep track of sms that is in, or not in db
        submission_time: is the date and time the feedback was submitted
        body: the message of the Sms
        phone_num: Phone number of person who sent in text
        pos_flag: 1 if body includes positive feedback. 0 if not. -1 default value
        neg_flag: 1 if body includes negative feedback. 0 if not. -1 default value
        exception_flag: 1 if body includes an exception to a present clause. 0 if not. -1 default value
        food_flag: 1 if body includes feedback about food. 0 if not. -1 default value
        service_flag: 1 if indicating body includes feedback about service. 0 if not. -1 default value

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
