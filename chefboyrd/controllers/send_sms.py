from flask import Flask, request, redirect
from twilio.rest import TwilioRestClient
import twilio.twiml
import configparser
import os

config = configparser.RawConfigParser()
config.read(os.path.join(os.path.dirname(__file__),'sms.cfg')) #assuming config file same path as this controller

def rcv_sms():
    '''
    Currently this outputs all the messages received by Seobo's twilio account.
    '''
    account_sid = config['keys']['account_sid']
    auth_token = config['keys']['auth_token']
    cust_phone_number = config['test']['cust_phone_number']
    restaurant_phone_number = config['test']['restaurant_phone_number']
    print(account_sid)
    print(auth_token)

    client = TwilioRestClient(account_sid,auth_token)

    messages = client.messages.list()
    for message in messages:
        try:
            print(message.body)
        except ValueError:
            print("End of messages reached.")


