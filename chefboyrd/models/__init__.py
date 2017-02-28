'''The base model sets up the database connections for all classes which inherit from it.
'''

from chefboyrd import DB as db
from peewee import Model

class BaseModel(Model):
    '''A base model which sets up the database connection for all inherited classes
    '''
    class Meta:
        database = db # Database for customers
