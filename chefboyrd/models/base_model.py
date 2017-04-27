'''Base model that all new models should inherit from

written by: Zachary Blanco
tested by: Zachary Blanco
debugged by: Zachary Blanco

This alows us to create new models which inherit the DB value and also the __str__
method for printing data for debugging purposes

'''
import json
from chefboyrd import DB as db
from peewee import Model

class BaseModel(Model):
    '''A base model which sets up the database connection for all inherited classes
    '''
    class Meta:
        database = db # Database for customers

    def __str__(self):
        r = {}
        for k in self._data.keys():
            try:
                r[k] = str(getattr(self, k))
            except BaseException:
                r[k] = json.dumps(getattr(self, k))
        return str(r)
