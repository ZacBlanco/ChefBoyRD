'''A data model for our customer'''
import chefboyrd
from peewee import Model

class Customer(Model):
    '''A sample customer model
    Please modify this to fit our needs
    '''
    name = CharField()

    class Meta:
        database = chefboyrd.db # This model uses the "people.db" database.
        