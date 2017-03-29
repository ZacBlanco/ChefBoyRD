'''Base model that all new models should inherit from

A data model is an object which helps us define mappings between our data in our databases
and the objects that we interact with inside of the program and in our code.

For this project we use an ORM (Object-Relational Mapping) library called peewee.
If you look at the code below peewee makes defining these models incredibly simple and the
documentation for the library is quite good. There are lots of examples and it is incredibly
powerful. Plus it peewee is ridiculously easy to use with SQLite. However if we do choose to
use another database the migration is very simple as well. This way our options are left open.

Otherwise there's not much else to talk about with the models. I highly recommend reading the
peewee Quickstart and documentation

See http://docs.peewee-orm.com/en/latest/peewee/quickstart.html
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
