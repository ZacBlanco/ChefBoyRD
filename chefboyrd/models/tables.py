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
            description(str): A description of the restaurant
            opening_time(int): The opening time of the restaurant in hours
            closing_time(int): The closing time of the restaurant in hours

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
            id(int): A unique identifier for the table
            restaurant(int): The foreign key of the restaurant
            size(int): The max number of guests a table can seat
            occupied(bool): Determines if a table is occupied. 0 is not occupied, and 1 is occupied
            posX(float): The relative x position of the table
            posY(float): The relative y position of the table

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
        '''
        Attemps to cancel a reservation given an ID

        Args:
        cls(Booking(: an object representing a booking
        id(int): the id of the booking we want to cancel
        '''
        res = cls.get(cls.id == id)
        res.delete_instance()
        return

    @classmethod
    def create_booking(cls,table,people,booking_date_time_start,booking_date_time_end, name, phone):
        '''Creates a new reservation
        
        Args:
            id(int): Unique Identifier for the booking. This should be auto added by peewee for us.
            people(int): The number of guests requested for the booking
            phone(char): A phone number of the guest making the reservation
            name(char): The name of the guest requesting the reservation
            booking_date_time_start(date): The starting time of the reservation
            booking_date_time_end(date): The ending time of the reservation

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

