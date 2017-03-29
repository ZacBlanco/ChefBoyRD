from peewee import TextField, DateTimeField, Model, IntegerField
from chefboyrd.models import BaseModel

class Sms(Model):
    """
    Args:

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
    pos_flag = IntegerField()
    neg_flag = IntegerField()
    exception_flag = IntegerField()
    food_flag = IntegerField()
    service_flag = IntegerField()
    #additional categories to associate	
