'''The basic user model (For logins)

written by: Zachary Blanco
tested by: Zachary Blanco
debugged by: Zachary Blanco

The users will have roles i.e. chef, manager, host, waitress, etc..
'''
from peewee import CharField, IntegrityError
from chefboyrd.models import BaseModel
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

class User(UserMixin, BaseModel):
    '''A User model for who will be using the software. Users have different levels of access with different roles

    Current active roles:

        - host
        - admin
        - chef
        - cust
    '''
    email = CharField(unique=True)
    password = CharField()
    name = CharField()
    role = CharField() #assumption that user will enter valid role

    @classmethod
    def create_user(cls, email, password, name, role):
        '''Creates a new user

        Args:
            email(str): The user email
            password(str): The password string - no need to hash beforehand
            name(str): name, doesn't have to be unique
            role(str): The user role. admin, manager, chef, host, etc..

        Returns:
            N/A

        Raises:
            ValueError: When user email already exists
        '''

        try:
            cls.create(
                email=email,
                password=generate_password_hash(password),
                name=name,
                role=role)
        except IntegrityError:
            raise ValueError("User already exists")
