'''ModelController
This is a preprocessor for the prediction_controller. Given data in the form of
our local models, it converts it into numbers usable by the prediction controller.

'''
from peewee import Model


def objects_to_list():
    '''Converts peewee query result set to a list of dictionary of lists'''
    pass

def scale_data():
    '''Scale data over a min/max range'''
    pass

def train_regression():
    '''Train and store a regression model with parameters'''
    pass

def get_earliest_datetime():
    '''Finds the minimum datetime'''
    pass

def get_last_datetime():
    '''Finds the maximum datetime in a list'''
    pass

def get_last_regression_params():
    '''Retrieves the last set of regression parameters trained.'''
    pass