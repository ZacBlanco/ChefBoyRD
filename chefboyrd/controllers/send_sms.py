from flask import Flask, request, redirect
from twilio.rest import TwilioRestClient
from datetime import datetime, date
from chefboyrd.models.sms import Sms
import twilio.twiml
import configparser
import os

config = configparser.RawConfigParser()
config.read(os.path.join(os.path.dirname(__file__),'sms.cfg')) #assuming config file same path as this controller
account_sid = config['keys']['account_sid']
auth_token = config['keys']['auth_token']
cust_phone_number = config['test']['cust_phone_number']
restaurant_phone_number = config['test']['restaurant_phone_number']

try:
    client = TwilioRestClient(account_sid,auth_token)
except:
    print("Could not communicate with rest client");

#print(account_sid)
#print(auth_token)
def rcv_sms():
    '''
    Currently this outputs all the messages received by Seobo's twilio account.
    '''
    
    messages = client.messages.list()
    for message in messages:
        try:
            print(message.body)
        except ValueError:
            print("End of messages reached.")

'''
need the sms information in the database so we can create tables with multiple objects
'''
def update_db(date_from):
    '''
	updates the sms in the database starting from the date_from specified (at time midnight)
	'''
    #date_from_twil = ("%s-%s-%s"%(date_from.year,"{0:0>2}".format(date_from.month),"{0:0>2}".format(date_from.day)))
    d = date(date_from.year, date_from.month, date_from.day)
    #messages = client.messages.list(date_sent=d) #doesnt work
    messages = client.messages.list() 
    print(messages)
    for message in messages:
        try:
            sms_tmp = Sms(body=message.body, phone_number=message.from_, submission_time=message.date_sent)
            print(sms_tmp.body)
            print(sms_tmp.submission_time) 
            if not (sms_tmp.save()):
                print("sms could not be saved in sb")
        except ValueError:
            print("End of messages reached.")
            return 0
    return 1 #this should be on success