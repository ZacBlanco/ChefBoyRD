"""
test_fb for unittesting the functions in feedback_controller
"""
"""
written by: Seo Bo Shim, Jarod Morin
tested by: Seo Bo Shim, Jarod Morin
debugged by: Seo Bo Shim, Jarod Morin
"""

import unittest
from unittest.mock import patch
from chefboyrd.controllers import feedback_controller
from chefboyrd.models.sms import Sms
from datetime import datetime

class MyModuleTest(unittest.TestCase):

    def test_update_db(self):
        """test the send_sms function
        """
        #TODO: if twilio connection not maintained
        self.assertEqual(feedback_controller.update_db(datetime(2016, 3, 21), update_from="test"), 1)
        self.assertEqual(feedback_controller.update_db(datetime(2027, 3, 21), update_from="test"), 0)
        query = Sms.delete()
        res = query.execute()
        self.assertEqual(len(Sms.select()), 0)
        feedback_controller.update_db(update_from="test")
        self.assertTrue(len(Sms.select()) > 0)
        smss = Sms.select().where(Sms.sid == 1)
        for sms in smss:
            self.assertEqual(sms.phone_num, "+12345678905")
        query = Sms.delete()
        res = query.execute()
        self.assertEqual(len(Sms.select()), 0)


    #delete_twilio_feedback not tested because it could skew results

    def test_feedback_analysis(self):
        """ Tests for correct performance of feedback analysis on known string inputs."""
        failStr = "Incorrect result for input \'{}\'"
        testStr = "Food was good"
        self.assertEqual(feedback_controller.feedback_analysis(testStr), [1, 0, 0, 1, 0])
        testStr = "Service was bad"
        self.assertEqual(feedback_controller.feedback_analysis(testStr), [0, 1, 0, 0, 1])
        testStr = "Service was bad,  but food was good"
        self.assertEqual(feedback_controller.feedback_analysis(testStr), [1, 1, 1, 1, 1])

    def test_delete_twilio_feedback(self):
        self.assertEqual(feedback_controller.delete_twilio_feedback(9),0)
        self.assertEqual(feedback_controller.delete_twilio_feedback("87fuei8a9s7"),0)
        #with self.assertRaises(ValueError):
        #    feedback_controller.delete_twilio_feedback("87fuei8a9s7")

    def test_word_freq_counter(self):
        """ Tests for correct performance of word frequency counter on known string inputs."""
        with self.assertRaises(TypeError):
            feedback_controller.word_freq_counter(5)
        self.assertEqual(feedback_controller.word_freq_counter("hello hello hello hello hello"),(['hello'],[5], 5) )
        self.assertEqual(feedback_controller.word_freq_counter("hello. hello, hello. hello, hello"),(['hello'],[5], 5) )
        self.assertEqual(feedback_controller.word_freq_counter("bad bad bad"),(['bad'],[3], 3))
        [a,b,maxfreq] = feedback_controller.word_freq_counter("bad bad bad good good")
        res = dict(zip(a,b))
        self.assertEqual(res,{'good':2,'bad':3})
        self.assertEqual(maxfreq,3)
        [a,b,maxfreq] = feedback_controller.word_freq_counter("bad bad ..bad ;spaghetti.. good good get out of my kitchen")
        res = dict(zip(a,b))
        self.assertEqual(res,{'good':2,'bad':3,'spaghetti':1,'get':1,'kitchen':1})
        self.assertEqual(maxfreq,3)

    #test stopwords
