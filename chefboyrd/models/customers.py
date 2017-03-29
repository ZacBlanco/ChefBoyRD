'''A data model for our customer

A data model is an object which helps us define mappings between our data in our databases
and the objects that we interact with inside of the program and in our code.
'''
from peewee import Model, CharField
from chefboyrd.models import BaseModel

class Customer(BaseModel):
    '''A sample customer model
    Please modify this to fit our needs
    '''
    name = CharField()
        