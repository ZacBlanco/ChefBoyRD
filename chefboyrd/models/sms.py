from peewee import TextField, DateTimeField, Model, IntegerField, BooleanField
from chefboyrd.models import BaseModel

class Sms(Model):
    """
    Args:

        Submission_time: is the date and time the feedback was submitted
        Body: the message of the Sms
        Phone_num: Phone number of person who sent in text
        Pos_flag: 1 if body includes positive feedback. 0 if not. -1 default value
        Neg_flag: 1 if body includes negative feedback. 0 if not. -1 default value
        Exception_flag: 1 if body includes an exception to a present clause. 0 if not. -1 default value
        Food_flag: 1 if body includes feedback about food. 0 if not. -1 default value
        Service_flag: 1 if indicating body includes feedback about service. 0 if not. -1 default value
        Invalid_field: True if needs to be deleted.

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
    invalid_field = BooleanField(default=False)
    #additional categories to associate	
