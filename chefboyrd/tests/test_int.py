'''Integration Tests which ensure all views are reachable from the homepage'''
import os
import unittest
from unittest.mock import patch
from datetime import datetime, date, timedelta
import tempfile
import chefboyrd
from peewee import SqliteDatabase
from chefboyrd.models import *
from chefboyrd.controllers import data_controller
from chefboyrd.controllers import model_controller
from chefboyrd.controllers import prediction_controller

class PageTest(unittest.TestCase):
    '''Testing for each of the pages and submission forms'''

    def setUp(self):
        '''Setup the test client and application'''
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

    def tearDown(self):
        '''Unlink and remove DB from application'''
        os.close(self.db_fd)
        os.unlink(self.db_name)

    def test_dashboard(self):
        '''Ensure sure we can reach the prediction page properly when logged in and out.'''
        self.login('zac', 'zac')
        self.app.get('/auth/login')
        r = self.app.get('/dashboard/')
        self.assertEqual(r.status_code, 200)
        self.logout()
        r = self.app.get('/dashboard/')
        self.assertEqual(r.status_code, 401)

    def test_dashboard_post(self):
        '''Ensure sure we can POST to each of the dashboard types'''
        self.login('zac', 'zac')
        self.app.get('/auth/login')
        r = self.app.get('/dashboard/')
        self.assertEqual(r.status_code, 200)
        r = self.app.post('/dashboard/?type=Meals', data={})
        self.assertEqual(r.status_code, 200)
        r = self.app.post('/dashboard/?type=Performance', data={})
        self.assertEqual(r.status_code, 200)
        r = self.app.post('/dashboard/?type=Revenue', data={})
        self.assertEqual(r.status_code, 200)
        r = self.app.post('/dashboard/?type=Ingredients', data={})
        self.assertEqual(r.status_code, 200)
        r = self.app.post('/dashboard/?type=Tabs', data={})
        self.assertEqual(r.status_code, 200)
        self.logout()
        r = self.app.get('/dashboard/')
        self.assertEqual(r.status_code, 401)

    def test_homepage(self):
        '''Ensure sure we can reach the homepage while running'''
        r = self.app.get('/')
        self.assertEqual(r.status_code, 200)

    def test_table_manager(self):
        '''Ensure sure we can reach the table_manager page properly when logged in and out.'''
        self.login('zac', 'zac')
        self.app.get('/auth/login')
        r = self.app.get('/table_manager/')
        self.assertEqual(r.status_code, 200)
        self.logout()
        r = self.app.get('/table_manager/')
        self.assertEqual(r.status_code, 401)

    def test_prediction(self):
        '''Ensure sure we can reach the prediction page properly when logged in and out.'''
        self.login('zac', 'zac')
        self.app.get('/auth/login')
        r = self.app.get('/prediction/')
        self.assertEqual(r.status_code, 200)
        self.logout()
        r = self.app.get('/prediction/')
        self.assertEqual(r.status_code, 401)

    def login(self, uname, pw):
        '''Logs a user in'''
        return self.app.post('/auth/login', data=dict(email=uname, pw=pw), follow_redirects=True)

    def logout(self):
        '''Logs the user out'''
        return self.app.get('/auth/logout')