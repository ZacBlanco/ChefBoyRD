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
        '''Setup for the database and test client'''
        self.db_fd, self.db_name = tempfile.mkstemp()
        chefboyrd.init_db(self.db_name)
        self.app = chefboyrd.APP.test_client()

    def tearDown(self):
        '''Deletion and unlinking of the database file'''
        os.close(self.db_fd)
        os.unlink(self.db_name)

    def test_login(self):
        '''Test login/logout functionality with different users'''
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
        '''Test the role requirement wrapper to make sure role-based
        authorization works as expected.
        
        '''
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


    def test_multi_role(self):
        '''Ensure that the role-required wrapper can handle multiple roles'''
        try:
            User.create_user('man2', 'man2', 'man2', 'role1')
            User.create_user('nam3', 'nam3', 'nam3', 'role2')
        except:
            pass
        rv = self.app.get('/multiroletest')
        self.assertNotEqual(rv.get_data(True), 'Stop')
        self.assertEqual(rv.status_code, 401, 'Should get a 401')
        self.login('man2', 'man2')
        rv = self.app.get('/multiroletest')
        self.assertEqual(rv.get_data(True), 'roletest')
        self.assertEqual(rv.status_code, 200, 'Should get a 200')
        self.logout()

        rv = self.app.get('/multiroletest')
        self.assertNotEqual(rv.get_data(True), 'Stop')
        self.assertEqual(rv.status_code, 401, 'Should get a 401')
        self.login('nam3', 'nam3')
        rv = self.app.get('/multiroletest')
        self.assertEqual(rv.get_data(True), 'roletest')
        self.assertEqual(rv.status_code, 200, 'Should get a 200')
        self.logout()


    def login(self, uname, pw):
        '''Logs a user in'''
        return self.app.post('/auth/login', data=dict(email=uname, pw=pw), follow_redirects=True)

    def logout(self):
        '''Logs the user out'''
        return self.app.get('/auth/logout')

@chefboyrd.APP.route('/protected')
@auth.require_login
def req_login():
    '''Route which requires a  user to be loggd in to access'''
    return 'Stop'

@chefboyrd.APP.route('/admintest')
@auth.require_role('manager')
def req_roles():
    '''Rout which requires a single role to be accessed'''
    return 'admintest'

@chefboyrd.APP.route('/multiroletest')
@auth.require_role(['role1', 'role2'])
def req_multi_role():
    '''Route which requires one of a list of roles to access'''
    return 'roletest'
