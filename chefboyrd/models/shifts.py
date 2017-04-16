from peewee import CharField, DateTimeField
from chefboyrd.models import BaseModel

class ClaimedShift(BaseModel):
    name = CharField(max_length=250)
    shift_time_start = DateTimeField()
    shift_time_end = DateTimeField()
    role = CharField(max_length=250)

    @classmethod
    def claim_shift(cls, name, shift_time_start, shift_time_end, role):
        '''
        Attempts to claim a shift given an ID

        Args:
            name(char): The name of the employee claiming the shift
        Returns:
            N/A
        '''
        try:
            cls.create(
                name=name, 
                shift_time_start=shift_time_start,
                shift_time_end=shift_time_end,
                role=role)
        except IntegrityError:
            raise ValueError("This should not happen(Shift)")

    @classmethod
    def post_shift(cls, id):
        '''
        Attempts to post a shift given an ID

        Args:
            cls(ClaimedShift): an object representing a claimed shift
            id(int): the id of the shift we want to post
        Returns:
            N/A
        '''
        res = cls.get(cls.id == id)
        res.delete_instance()
        return
    
class FreeShift(BaseModel):
    name = CharField(max_length=250)
    shift_time_start = DateTimeField()
    shift_time_end = DateTimeField()
    role = CharField(max_length=250)

    @classmethod
    def claim_shift(cls, id):
        '''
        Attempts to post a shift given an ID

        Args:
            cls(ClaimedShift): an object representing a claimed shift
            id(int): the id of the shift we want to post
        Returns:
            N/A
        '''
        res = cls.get(cls.id == id)
        res.delete_instance()
        return

    @classmethod
    def post_shift(cls, name, shift_time_start, shift_time_end, role):
        '''
        Attempts to claim a shift given an ID

        Args:
            name(char): The name of the employee claiming the shift
        Returns:
            N/A
        '''
        try:
            cls.create(
                name=name, 
                shift_time_start=shift_time_start,
                shift_time_end=shift_time_end,
                role=role)
        except IntegrityError:
            raise ValueError("This should not happen(Shift)")
        
