from twilio.rest import TwilioRestClient
from datetime import datetime, date, timedelta
import twilio.twiml
import configparser
import os
from chefboyrd.models.sms import Sms
from peewee import IntegrityError

config = configparser.RawConfigParser()
config.read(os.path.join(os.path.dirname(__file__),'sms.cfg')) #assuming config file same path as this controller
account_sid = config['keys']['account_sid']
auth_token = config['keys']['auth_token']
cust_phone_number = config['test']['cust_phone_number']
restaurant_phone_number = config['test']['restaurant_phone_number']


'''
need the sms information in the database so we can create tables with multiple objects
'''
def update_db(*date_from):
    '''
    updates the sms in the database starting from the date_from specified (at time midnight)
    no param = updates the sms feedback in database with all message entries
    TODO: this may create duplicate entries, should test this 
    TODO: Fix error with twilio, where the most recent message does not have a submission timep
    TODO: Fix possible error with DST. TImezone was hotfix

    Args:
        date_from (date object): a specified date, where we update db with sms sent after this date

    Throws:
        SystemError: When the Twilio Client cannot be started. Possibly invalid account_sid or auth_token
    '''
    try:
        client = TwilioRestClient(account_sid,auth_token)
    except:
        raise SystemError("Could not communicate with Twilio Rest client");
    if date_from == ():
        messages = client.messages.list() # this may have a long random string first
    else:
        date_from = date_from[0]
        messages = client.messages.list(DateSent=date_from)
    for message in messages:
        try:
            if (message.date_sent != None):
                date_tmp = message.date_sent - timedelta(hours=4)
            else:
                date_tmp = None
            sms_tmp = Sms(
                sid=message.sid,
                submission_time= date_tmp,
                body=message.body, 
                phone_num=message.from_,
                pos_flag=-1,
                neg_flag=-1,
                exception_flag=-1,
                food_flag=-1,
                service_flag=-1
                )
            #print(sms_tmp.body)
            #print(sms_tmp.submission_time) 
            #print(sms_tmp.body)
            err = sms_tmp.save()
            if not (err):
                print("Sms could not be saved in db" + sms_tmp.body)
        except ValueError:
            print("End of messages reached.")
            return 0
        except IntegrityError:
            err = 0
            print("Duplicate Sms Entry " + sms_tmp.body)
            #raise IntegrityError
    return 1 #this should be on success

#only need to do this once before demo
def delete_feedback():
    '''
    wipe all message history on twilio
    '''
    messages = client.messages.list()
    for message in messages:
        try:
            client.messages.delete(message.sid)
        except ValueError:
            print("End of messages list reached.")
            return 0
    return 1