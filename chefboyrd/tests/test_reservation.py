'''Test some model creation and methods'''
import os
import unittest
from unittest.mock import patch
from datetime import datetime, date, timedelta
import tempfile
import chefboyrd
from chefboyrd.models import *
from peewee import SqliteDatabase
from chefboyrd.controllers import booking_controller as booking


class ModelTest(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.db_fd, self.db_name = tempfile.mkstemp()
        chefboyrd.init_db(self.db_name)
        self.app = chefboyrd.APP.test_client()
        # This bit of code sets the db to a tempfile for each model
        # Ensures testing on fresh DB every run.
        chefboyrd.DB = SqliteDatabase(self.db_name)
        tables.Restaurant._meta.database = chefboyrd.DB
        tables.Restaurant.create_table(True)
        tables.Tables._meta.database = chefboyrd.DB
        tables.Tables.create_table(True)
        tables.Booking._meta.database = chefboyrd.DB
        tables.Booking.create_table(True)



        self.restaurant_1 = tables.Restaurant.create(opening_time=18, closing_time=23,name='Pizza Hut',description='Pizza place.')
        self.restaurant_1_table_1 = tables.Tables.create(restaurant=self.restaurant_1, size=2,occupied=0,posX=0,posY=0,shape =0)
        self.restaurant_1_table_2 = tables.Tables.create(restaurant=self.restaurant_1, size=4,occupied=0,posX=0,posY=0,shape =0)

        booking_date_time_start = datetime(2017, 2, 14, 19, 0)
        minutes_slot = 90
        delta = timedelta(seconds=60*minutes_slot)
        booking_date_time_end = booking_date_time_start + delta

        self.booking_1 = tables.Booking.create(
            table=self.restaurant_1_table_2,
            people=4,
            booking_date_time_start=booking_date_time_start,
            booking_date_time_end=booking_date_time_end,name='Bob',phone='5555555555')

    @classmethod
    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_name)

    def test_get_first_table_available(self):
        '''
        This tests that we successfully created the table, and are able to book this table.
        '''
        table = booking.get_first_table_available(
            restaurant=self.restaurant_1,
            booking_date_time=datetime(2017, 2, 14, 20, 0),
            people=2)
        self.assertEqual(table.id, self.restaurant_1_table_1.id)

    def test_get_first_table_available_unavailable_1(self):
        '''
        The setup already books the 4 people table from 19:00 to 20:30
        '''
        table = booking.get_first_table_available(
            restaurant=self.restaurant_1,
            booking_date_time=datetime(2017, 2, 14, 20, 0),
            people=4)
        self.assertEqual(table, None)

    def test_get_first_table_available_unavailable_2(self):
        '''
        The setup already books the 4 people table from 19:00 to 20:30
        '''
        table = booking.get_first_table_available(
            restaurant=self.restaurant_1,
            booking_date_time=datetime(2017, 2, 14, 18, 0),
            people=4)
        self.assertEqual(table, None)

    def test_get_first_table_available_unavailable_3(self):
        '''
        The setup already books the 4 people table from 19:00 to 20:30
        '''
        table = booking.get_first_table_available(
            restaurant=self.restaurant_1,
            booking_date_time=datetime(2017, 2, 14, 18, 0),
            people=4,
            minutes_slot=300)
        self.assertEqual(table, None)

    def test_get_first_table_available_unavailable_4(self):
        '''
        The setup already books the 4 people table from 19:00 to 20:30
        '''
        table = booking.get_first_table_available(
            restaurant=self.restaurant_1,
            booking_date_time=datetime(2017, 2, 14, 19, 30),
            people=4,
            minutes_slot=30)
        self.assertEqual(table, None)

    def test_unavailable_tables_1_hour_before_closing(self):
        '''
        Attempts to get a table 1 hour before closing, but there is not enough time
        '''
        table = booking.get_first_table_available(
            restaurant=self.restaurant_1,
            booking_date_time=datetime(2017, 2, 14, 22, 0),
            people=2)
        self.assertEqual(table, None)

    def test_unavailable_tables_1_hour_before_opening(self):
        '''
        Attempts to make a booking before the restaurant opens
        '''
        table = booking.get_first_table_available(
            restaurant=self.restaurant_1,
            booking_date_time=datetime(2017, 2, 14, 17, 0),
            people=2)
        self.assertEqual(table, None)

    def test_book_first_available_table(self):
        '''
        Another test to get first table at a different date
        '''
        booking_response = booking.book_restaurant_table(
            restaurant=self.restaurant_1,
            booking_date_time=datetime(2017, 2, 14, 20, 0),
            people=2,name='Bob',phone='5555555555')
        self.assertEqual(booking_response['table'], self.restaurant_1_table_1.id)

    def test_book_table_for_2_hours(self):
        '''
        Attempts to book a reservation for 2 hours
        '''
        booking_response = booking.book_restaurant_table(
            restaurant=self.restaurant_1,
            booking_date_time=datetime(2017, 2, 14, 21, 0),
            people=2,
            minutes_slot=120,name='Bob',phone='5555555555')
>>>>>>> master
        self.assertEqual(booking_response['table'], self.restaurant_1_table_1.id)