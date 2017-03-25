from chefboyrd.models.sms import Sms
from twilio.rest import TwilioRestClient
from datetime import datetime, date
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

'''
need the sms information in the database so we can create tables with multiple objects
'''
def update_db(*date_from):
    '''
    updates the sms in the database starting from the date_from specified (at time midnight)
    no param = updates the sms feedback in database with all message entries
    TODO: this may create duplicate entries, should test this 
    '''
    if date_from == ():
        messages = client.messages.list() # this may have a long random string first
    else:
        date_from = date_from[0]
        messages = client.messages.list(date_sent=date_from)
    for message in messages:
        try:
            sms_tmp = Sms(
                sid=message.sid,
                submission_time=message.date_sent,
                body=message.body, 
                phone_number=message.from_
                )
            print(sms_tmp.body)
            #print(sms_tmp.submission_time) 
            if not (sms_tmp.save()):
                print("sms could not be saved in sb")
        except ValueError:
            print("End of messages reached.")
            return 0
    return 1 #this should be on success

#only need to do this before demo
# def delete_feedback():
#     '''
#     wipe all message history on twilio
#     '''
#     messages = client.messages.list()
#     for message in messages:
#         try:
#             client.messages.delete(message.sid)
#         except ValueError:
#             print("End of messages list reached.")
#             return 0
#     return 1