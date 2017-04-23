from peewee import TextField, DateTimeField, Model, IntegerField
from chefboyrd.models import BaseModel

class Rating(Model):
    """
    Args:

        Submission_time(datetime): is the date and time the rating was submitted
        food(int): 0-5 rating for food
        service(int): 0-5 rating for service
        clean(int): 0-5 rating for cleanliness
        ambience(int): 0-5 rating for ambience
        overall(int): 0-5 rating for overall experience
        comment(str): submitted comment

    """
    submission_time = DateTimeField()
    
    food = IntegerField()
    service = IntegerField()
    clean = IntegerField()
    ambience = IntegerField()
    overall = IntegerField()

    comment = TextField()
