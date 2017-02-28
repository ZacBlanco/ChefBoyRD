'''The basic user model

The users will have roles i.e. chef, manager, host, waitress, etc..
'''
from peewee import CharField, IntegrityError
from chefboyrd.models import BaseModel
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

class User(UserMixin, BaseModel):
    '''A sample customer model
    Please modify this to fit our needs
    '''
    email = CharField(unique=True, primary_key=True)
    password = CharField()
    name = CharField()
    role = CharField()

    @classmethod
    def create_user(cls, email, password, name, role):
        try:
            cls.create(
                email=email,
                password=generate_password_hash(password),
                name=name,
                role=role)
        except IntegrityError:
            raise ValueError("User already exists")
