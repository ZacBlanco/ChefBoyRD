from peewee import CharField, DateTimeField, IntegrityError
from chefboyrd.models import BaseModel

class Shift(BaseModel):
    name = CharField(max_length=250)
    shift_time_start = DateTimeField()
    shift_time_end = DateTimeField()
    role = CharField(max_length=250)

    @classmethod
    def create_shift(cls, name, shift_time_start, shift_time_end, role, claim):
        '''
        Creates a new Shift

        Args:
            name(char): The name of the employee claiming the shift
            shift_time_start(time): Starting time of shift
            shift_time_end(time): Ending time of shift
            role(str): 
        Returns:
            N/A
        '''
        try:
            cls.create(
                name=name, 
                shift_time_start=shift_time_start,
                shift_time_end=shift_time_end,
                role=role,
                claimed=claim)
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
        res.claimed = None
        res.name = None
        return

    @classmethod
    def remove_shift(cls, id):
        '''
        Attempts to remove a shift given an ID

        Args:
            cls(ClaimedShift): an object representing a claimed shift
            id(int): the id of the shift we want to post
        Returns:
            N/A
        '''
        res = cls.get(cls.id == id)
        res.delete_instance()
        return