'''Test some model creation and methods'''
import os
import unittest
from unittest.mock import patch
from datetime import datetime, date, timedelta
import tempfile
import chefboyrd
from chefboyrd.models import *
from peewee import SqliteDatabase
from chefboyrd.controllers import data_controller
from chefboyrd.controllers import model_controller
from chefboyrd.controllers import prediction_controller

class ModelTest(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.db_fd, self.db_name = tempfile.mkstemp()
        chefboyrd.init_db(self.db_name)
        self.app = chefboyrd.APP.test_client()
        # This bit of code sets the db to a tempfile for each model
        # Ensures testing on fresh DB every run.
        chefboyrd.DB = SqliteDatabase(self.db_name)
        Tabs._meta.database = chefboyrd.DB
        Tabs.create_table(True)
        Meals._meta.database = chefboyrd.DB
        Meals.create_table(True)
        MealIngredients._meta.database = chefboyrd.DB
        MealIngredients.create_table(True)
        Orders._meta.database = chefboyrd.DB
        Orders.create_table(True)
        Quantities._meta.database = chefboyrd.DB
        Quantities.create_table(True)
        Ingredients._meta.database = chefboyrd.DB
        Ingredients.create_table(True)

    @classmethod
    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_name)

    def test_polynomialModel(self):
        iv = [1, 2, 3] # Input vector
        ip = [1, 1, 1, 1] # Input parameters
        ans = model_controller.polynomialModel(iv, *ip)
        self.assertEqual(ans, 7) # Expected output is 7

    def test_sinusoidalModel(self):
        iv = [1, 2, 3]
        ip = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ans = model_controller.sinusoidalModel(iv, *ip)
        self.assertEqual(ans, 1.2936149395776206) # Expected output

    def test_get_earliest_datetime(self):
        data_controller.generate_data(1, 1, 1)
        expected_earliest_datetime = datetime.now()
        earliest_datetime = model_controller.get_earliest_datetime() 
        self.assertEqual(earliest_datetime.year, expected_earliest_datetime.year)
        self.assertEqual(earliest_datetime.month, expected_earliest_datetime.month)
        self.assertEqual(earliest_datetime.day, expected_earliest_datetime.day)

    def test_create_meal(self):
        try:
            Meals.create(price=12.99, name="Cheeseburger")
        except:
            pass
        meals = Meals.select().where(Meals.name == "Cheeseburger")
        self.assertEqual(len(meals), 1)
        self.assertEqual(meals[0].price, 12.99)

    def test_create_tab(self):
        try:
            Tabs.create(had_reservation=False, party_size=12, timestamp=datetime.now())
        except:
            pass
        tabs = Tabs.select().where(Tabs.party_size == 10)
        self.assertEqual(len(tabs), 0)
        tabs = Tabs.select().where(Tabs.party_size == 12)
        self.assertEqual(len(tabs), 1)
        self.assertEqual(tabs[0].had_reservation, False)

    def test_create_foreign_key_obj(self):
        try:
            MealIngredients.create(quantity_amt=1, meal_id=12, ingredient_id=9,
                                   quantity_meas_id=12)
        except BaseException as err:
            pass
        mis = MealIngredients.select().where(MealIngredients.quantity_amt == 1)
        self.assertEqual(len(mis), 1)

    def test_get_order_range(self):
        m1 = Meals.create(name="Burger", price=8.99)
        num = 20
        times = []
        ords = []
        for x in range(20):
            tm = datetime.now()
            times.append(tm)
            t = Tabs.create(timestamp=tm, had_reservation=False, party_size=x)
            ords.append(Orders.create(tab=t.get_id(), meal=m1.get_id()))
        dcords = data_controller.get_orders_date_range()
        self.assertEqual(len(dcords), 20)
        dcords = data_controller.get_orders_date_range(times[1])
        for c in dcords:
            self.assertEqual(c.tab.timestamp >= times[1], True)
        self.assertEqual(len(dcords), 19)
        dcords = data_controller.get_orders_date_range(times[2])
        self.assertEqual(len(dcords), 18)
        dcords = data_controller.get_orders_date_range(times[18])
        self.assertEqual(len(dcords), 2)
        dcords = data_controller.get_orders_date_range(dt_max=times[15])
        self.assertEqual(len(dcords), 16)
        for c in dcords:
            self.assertEqual(c.tab.timestamp <= times[15], True)
        dcords = data_controller.get_orders_date_range(dt_max=times[18])
        self.assertEqual(len(dcords), 19)
        dcords = data_controller.get_orders_date_range(times[2], times[18])
        for c in dcords:
            self.assertEqual(c.tab.timestamp >= times[2] and c.tab.timestamp <= times[18], True)
        self.assertEqual(len(dcords), 17)

        with self.assertRaises(ValueError):
            data_controller.get_orders_date_range(times[5], times[4])

    def test_get_tab_range(self):
        num = 20
        times = []
        ords = []
        for x in range(20):
            tm = datetime.now()
            times.append(tm)
            t = Tabs.create(timestamp=tm, had_reservation=False, party_size=x)
        dcords = data_controller.get_tabs_range()
        self.assertEqual(len(dcords), 20)
        dcords = data_controller.get_tabs_range(times[1])
        for c in dcords:
            self.assertEqual(c.timestamp >= times[1], True)
        self.assertEqual(len(dcords), 19)
        dcords = data_controller.get_tabs_range(times[2])
        self.assertEqual(len(dcords), 18)
        dcords = data_controller.get_tabs_range(times[18])
        self.assertEqual(len(dcords), 2)
        dcords = data_controller.get_tabs_range(dt_max=times[15])
        self.assertEqual(len(dcords), 16)
        for c in dcords:
            self.assertEqual(c.timestamp <= times[15], True)
        dcords = data_controller.get_tabs_range(dt_max=times[18])
        self.assertEqual(len(dcords), 19)
        dcords = data_controller.get_tabs_range(times[2], times[18])
        for c in dcords:
            self.assertEqual(c.timestamp >= times[2] and c.timestamp <= times[18], True)
        self.assertEqual(len(dcords), 17)

        with self.assertRaises(ValueError):
            data_controller.get_tabs_range(times[5], times[4])
        
    def test_get_dotw(self):
        m1 = Meals.create(name="Burger", price=8.99)
        for x in range(5):
            tm = datetime.now()
            for y in range(7):
                td = tm - timedelta(days = y)
                t = Tabs.create(timestamp=td, had_reservation=False, party_size=x)
                Orders.create(tab=t.get_id(), meal=m1.get_id())
        for x in range(7):
            self.assertEqual(len(data_controller.get_dotw_orders(x)), 5)

        with self.assertRaises(ValueError):
            data_controller.get_dotw_orders(-1)
        with self.assertRaises(ValueError):
            data_controller.get_dotw_orders(8)

    @patch('chefboyrd.models.Orders.create', return_value=None)
    def test_generate_data(self, orders):
        # print(Ingredients._meta.database.database)
        data_controller.generate_data(num_days=1, num_tabs=5)
        orders.asser_called_once()
            


