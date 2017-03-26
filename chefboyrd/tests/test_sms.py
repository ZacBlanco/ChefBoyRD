'''An example tet module to demonstrate the python unittest structure'''

import unittest
from unittest.mock import patch
from chefboyrd.controllers import send_sms
from datetime import datetime

class MyModuleTestt(unittest.TestCase):
    '''Example Test Module'''

    def test_sms(self):
        '''test the send_sms function
        '''
        self.assertEqual(send_sms.update_db(datetime(2017,3,21)),1)