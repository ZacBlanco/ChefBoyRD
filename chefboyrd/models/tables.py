from peewee import Model, CharField, IntegerField, IntegerField, ForeignKeyField, DateTimeField, BooleanField, FloatField
from chefboyrd.models import BaseModel


class Restaurant(BaseModel):
    name = CharField(max_length=250)
    description = CharField(max_length=250)
    opening_time = IntegerField()
    closing_time = IntegerField()

    @classmethod
    def create_restaurant(cls,name,description,opening_time,closing_time):
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
                description=description,
                opening_time=opening_time,
                closing_time=closing_time)
        except IntegrityError:
            raise ValueError("This should not happen(Restaurant)")

class Table(BaseModel):
    restaurant = ForeignKeyField(Restaurant)
    size = IntegerField()
    occupied = BooleanField()
    posX = FloatField()
    posY = FloatField()

    @classmethod
    def create_tables(cls,restaurant,size, occupied, posX, posY):
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
            tb = cls.create(
                restaurant=restaurant,
                size=size, occupied=occupied, posX=posX,posY=posY)
            return [tb.posX,tb.posY,tb.occupied,tb.id]
        except IntegrityError:
            raise ValueError("This should not happen(Table)")



class Booking(BaseModel):
    table = ForeignKeyField(Table)
    people = IntegerField()
    phone = CharField() # Phone number 
    name = CharField() # Name of person who made the reservation
    booking_date_time_start = DateTimeField()
    booking_date_time_end = DateTimeField()

    @classmethod
    def cancel_reservation(cls,id):
        res = cls.get(cls.id == id)
        res.delete_instance()
        return

    @classmethod
    def create_booking(cls,table,people,booking_date_time_start,booking_date_time_end, name, phone):
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
                table=table,
                people=people,
                booking_date_time_start=booking_date_time_start,
                booking_date_time_end=booking_date_time_end,
                name=name,
                phone=phone)
        except IntegrityError:
            raise ValueError("This should not happen(Booking)")

