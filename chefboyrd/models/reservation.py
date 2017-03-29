'''The basic reservation model

'''
from peewee import *
from chefboyrd.models import BaseModel
from flask_login import UserMixin
from werkzeug.security import generate_password_hash


class Reservation(UserMixin, BaseModel):

    name = CharField() # Name of person who made the reservation
    num = IntegerField() # Number of people
    phone = CharField() # Phone number 
    start = DateTimeField() # Starting time of reservation

    @classmethod
    def cancel_reservation(cls,id):
        res = cls.get(cls.id == id)
        res.delete_instance()
        return


    @classmethod
    def create_reservation(cls,name, num, phone, start):
        '''Creates a new reservation
        
        Args:
            id(int): Unique Identifier for reservation. This should be auto added by peewee for us.
            name(str): Name of person who made the reservation
            num(int): Number of people in the reservation
            phone(str): Phone number of person who made the reservation
            start(time): Starting time of reservation

        Returns:
            N/A

        Raises:
            ValueError: 
        '''
        try:
            cls.create(
                name=name,
                num=num,
                phone=phone,
                start=start)
        except IntegrityError:
            raise ValueError("This should not happen(Reservation)")
