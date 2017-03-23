'''Test some model creation and methods'''
import os
import datetime
import unittest
from unittest.mock import patch
import tempfile
import chefboyrd
from chefboyrd.models import *
from peewee import SqliteDatabase

class ModelTest(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_name = tempfile.mkstemp()
        chefboyrd.init_db(self.db_name)
        self.app = chefboyrd.APP.test_client()
        chefboyrd.DB = SqliteDatabase(self.db_name)

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_name)

    def test_create_meal(self):
        try:
            Meals.create(price=12.99, name="Cheeseburger")
        except:
            pass
        meals = Meals.select().where(Meals.name == "Cheeseburger")
        self.assertEqual(len(meals), 1)
        self.assertEqual(meals[0].price, 12.99)

    def test_create_tab(self):
        Tabs._meta.database = chefboyrd.DB
        Tabs.create_table(True)
        try:
            Tabs.create(had_reservation=False, party_size=12, timestamp=datetime.datetime.now())
        except:
            pass
        tabs = Tabs.select().where(Tabs.party_size == 10)
        self.assertEqual(len(tabs), 0)
        tabs = Tabs.select().where(Tabs.party_size == 12)
        self.assertEqual(len(tabs), 1)
        self.assertEqual(tabs[0].had_reservation, False)

    def test_create_foreign_key_obj(self):
        MealIngredients._meta.database = chefboyrd.DB
        MealIngredients.create_table(True)
        try:
            MealIngredients.create(quantity_amt=1, meal_id=12, ingredient_id=9,
                                   quantity_meas_id=12)
        except BaseException as err:
            pass
        mis = MealIngredients.select().where(MealIngredients.quantity_amt == 1)
        self.assertEqual(len(mis), 1)
