'''An example tet module to demonstrate the python unittest structure'''

import unittest
import datetime
from unittest.mock import patch

from chefboyrd import example_module
from chefboyrd.controllers import send_sms

class MyModuleTest(unittest.TestCase):
    '''Example Test Module'''

    def test_something(self):
        '''Sample Test Case'''

        self.assertEqual("I am Equal", "I am Equal", 'Assert equal on testcase should always pass')
        self.assertNotEqual("Not equal", 'nOt EqUaL', "These two should always not be equal")

    def test_sms(self):
        '''test send sms function'''
        dt = datetime.datetime(2017,2,22)
        self.assertEqual(send_sms.update_db(dt),1,"got all msgs")

    def test_fib(self):
        '''Second sample testcase'''
        self.assertEqual(example_module.fib(0), 0, "fib(0) is 0")
        self.assertEqual(example_module.fib(1), 1, "fib(1) is 1")
        self.assertEqual(example_module.fib(2), 1, "fib(2) is 1")
        self.assertEqual(example_module.fib(3), 2, "fib(3) is 2")

    def test_non_int_fib(self):
        '''Third sample testcase'''
        with self.assertRaises(TypeError):
            example_module.fib(1.2)

    @patch('chefboyrd.example_module.fib', return_value=10)
    def test_example_patch(self, mock1):
        ''''Demonstrate what patching does
        Highly recommended to check out the documentation for unittest.mock. Please see
        https://docs.python.org/3/library/unittest.mock.html

        There are lots of great features
        '''
        self.assertEqual(example_module.fib(999999), 10,
                         "Patch makes the return value always 10")


if __name__ == '__main__':
    unittest.main()
