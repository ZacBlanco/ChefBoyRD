import unittest
import chefboyrd
import os
import tempfile
from chefboyrd import auth
import flask_login
from chefboyrd.models import User


class AuthTest(unittest.TestCase):
    '''Authentication and Authorization Tests'''

    def setUp(self):
        self.db_fd, self.db_name = tempfile.mkstemp()
        chefboyrd.init_db(self.db_name)
        self.app = chefboyrd.APP.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_name)

    def test_login(self):
        '''Test login/logout functionality'''
        try:
            User.create_user('zac', 'zac', 'zac', 'manager')
        except:
            pass
        rv = self.app.get('/protected')
        self.assertNotEqual(rv.get_data(True), 'Stop')
        self.assertEqual(rv.status_code, 401, 'Should get a 401')
        rv = self.login('zac', 'zac')
        self.assertEqual(rv.status_code, 200, 'After login should receive a 200')
        rv = self.app.get('/protected')
        self.assertEqual(rv.status_code, 200, 'Protected should be 200 after login')
        self.assertEqual(rv.get_data(True), 'Stop')
        self.logout()
        self.assertEqual(rv.status_code, 200, 'After logout should receive a 200')
        rv = self.app.get('/protected')
        self.assertNotEqual(rv.get_data(True), 'Stop')
        self.assertEqual(rv.status_code, 401, 'Should get a 401')

    def test_roles(self):
        '''Test the role requirement wrapper'''
        try:
            User.create_user('man', 'man', 'man', 'manager')
            User.create_user('nam', 'nam', 'nam', 'nomanager')
        except:
            pass
        rv = self.app.get('/admintest')
        self.assertNotEqual(rv.get_data(True), 'Stop')
        self.assertEqual(rv.status_code, 401, 'Should get a 401')
        self.login('nam', 'nam')
        rv = self.app.get('/admintest')
        self.assertNotEqual(rv.get_data(True), 'admintest')
        self.assertEqual(rv.status_code, 401, 'Should get a 401')
        self.logout()
        rv = self.app.get('/admintest')
        self.assertNotEqual(rv.get_data(True), 'admintest')
        self.assertEqual(rv.status_code, 401, 'Should get a 401')
        self.login('man', 'man')
        rv = self.app.get('/admintest')
        self.assertEqual(rv.status_code, 200, 'Protected should be 200 after login')
        self.assertEqual(rv.get_data(True), 'admintest')
        self.logout()
        rv = self.app.get('/admintest')
        self.assertNotEqual(rv.get_data(True), 'admintest')
        self.assertEqual(rv.status_code, 401, 'Should get a 401')


    def login(self, uname, pw):
        '''Logs a user in'''
        return self.app.post('/auth/login', data=dict(email=uname, pw=pw), follow_redirects=True)

    def logout(self):
        '''Logs the user out'''
        return self.app.get('/auth/logout')

@chefboyrd.APP.route('/protected')
@auth.require_login
def req_login():
    return 'Stop'

@chefboyrd.APP.route('/admintest')
@auth.require_role('manager')
def req_roles():
    return 'admintest'
