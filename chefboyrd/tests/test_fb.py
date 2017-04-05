"""test_fb for unittesting the feedback-related functions"""
import unittest
from unittest.mock import patch
from chefboyrd.controllers import feedback_controller
from chefboyrd.models.sms import Sms
from datetime import datetime

class MyModuleTest(unittest.TestCase):

    def test_update_db_delete(self):
        """test the send_sms function
        """
        #TODO: if twilio connection not maintained
        self.assertEqual(feedback_controller.update_db(datetime(2016, 3, 21), "test"), 1)
        self.assertEqual(feedback_controller.update_db(datetime(2027, 3, 21), "test"), 0)
        feedback_controller.delete_feedback()
        self.assertEqual(len(Sms.select()), 0)
        feedback_controller.update_db(update_from="test")
        self.assertTrue(len(Sms.select()) > 0)
        feedback_controller.delete_feedback()
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


    def test_word_freq_counter(self):
        """ Tests for correct performance of word frequency counter on known string inputs."""
        with self.assertRaises(TypeError):
            feedback_controller.word_freq_counter(5)
        self.assertEqual(feedback_controller.word_freq_counter("hello hello hello hello hello"), [dict(text='hello', size=5)] )
        self.assertEqual(feedback_controller.word_freq_counter("hello. hello,  hello. hello,  hello"), [dict(text='hello', size=5)] )
        testStr2 = "bad bad bad"
        self.assertEqual(feedback_controller.word_freq_counter(testStr2), [dict(text='bad', size=3)])

