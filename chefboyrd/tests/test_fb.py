"""Unittesting the functions in feedback_controller. Includes feedback analysis and storage and deletion of 
sms objects in the database

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
        """Tests to make sure that Sms objects that are stored in the database are storing correctly.
        Tests the functionality of the Sms feedback use case: storing and accessing feedback

        **Passes when**: The system can process Sms data that is sent and update the database. 
        Can query with a date range while rejecting invalid dates. Can correctly read sms data

        **Fails when**: System has errors in processing sms. Cannot read information from the Sms object
        The sms database is not empty when deleted and invalid date ranges are specified

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
        """ Tests for correct performance of feedback analysis on known string inputs.
        Tests functionality of sms feedback use case, that the analysis is done accurately

        **Passes when**: The feedback analysis algorithm correctly assigns appropriate flags to
        a set of example strings.

        **Fails when**: The feedback analysis algorithm fails to assign correct flags to messages

        """
        failStr = "Incorrect result for input \'{}\'"
        testStr = "Food was good"
        self.assertEqual(feedback_controller.feedback_analysis(testStr), [1, 0, 0, 1, 0])
        testStr = "Service was bad"
        self.assertEqual(feedback_controller.feedback_analysis(testStr), [0, 1, 0, 0, 1])
        testStr = "Service was bad,  but food was good"
        self.assertEqual(feedback_controller.feedback_analysis(testStr), [1, 1, 1, 1, 1])

    def test_delete_twilio_feedback(self):
        """ Tests for correct performance of method that deletes feedback in the Twilio API and in our database

        **Passes when**: Cannot delete sms data with invalid sid. Method to delete feedback handles
        errors appropriately

        **Fails when**: The controller attempts to delete sms that does not exist. Or if there
        is a problem with interfacing with the Twilio API

        """
        self.assertEqual(feedback_controller.delete_twilio_feedback(9),0)
        self.assertEqual(feedback_controller.delete_twilio_feedback("87fuei8a9s7"),0)

    def test_word_freq_counter(self):
        """ Tests for correct performance of word frequency counter on known string inputs.
        Test for the sms feedback use case, where the result of the feedback analysis can then be displayed in
        a word cloud in the management's feedback panel

        **Passes when**: The word_frequency_counter can appropriately assign frequency values in the correct output format
        Handles invalid input with error

        **Fails when**: The word_frequency_counter is not assigning correct frequency values to words
        Or does not respond appropriately to invalid input.

        """
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
