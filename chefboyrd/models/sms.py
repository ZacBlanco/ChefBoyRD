from peewee import TextField, DateTimeField, Model, IntegerField
from chefboyrd.models import BaseModel

class Sms(Model):
    '''
    Args:

    sid(str): is an unique id assigned by twilio. it will help us keep track of sms that is in, or not in db
    submission_time(datetime): is the date and time the feedback was submitted
    body(str): the message of the string
    phone_num(str): Phone number of person who sent in text

    TODO: submission_time assumes we are in EST time zone
    '''
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
