'''A data model for our customer

A data model is an object which helps us define mappings between our data in our databases
and the objects that we interact with inside of the program and in our code.

For this project I'm proposing we use an ORM (Object-Relational Mapping) library called peewee.
If you look at the code below peewee makes defining these models incredibly simple and the
documentation for the library is quite good. There are lots of examples and it is incredibly
powerful. Plus it peewee is ridiculously easy to use with SQLite. However if we do choose to
use another database the migration is very simple as well. This way our options are left open.

Otherwise there's not much else to talk about with the models. I highly recommend reading the
peewee Quickstart and documentation

See http://docs.peewee-orm.com/en/latest/peewee/quickstart.html

'''
from peewee import Model, CharField
from chefboyrd.models import BaseModel

class Customer(BaseModel):
    '''A sample customer model
    Please modify this to fit our needs
    '''
    name = CharField()
        