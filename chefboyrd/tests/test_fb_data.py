"""test_fb_data
includes the functions required to generate random sms messages in case Twilio is not available

"""
"""
written by: Seo Bo Shim
tested by: Seo Bo Shim
debugged by: Seo Bo Shim
"""

from datetime import datetime, timedelta
from random import randrange
import configparser
import os
from chefboyrd.models.sms import Sms
from peewee import IntegrityError

class TestMessages(object):
    """
    test class that emulates how twilio stores messages, so that this can be run to test the funtions without a connection to twilio
    """
    def __init__ (self, sid, date_sent, body, from_):
        self.sid = sid
        self.date_sent = date_sent
        self.body = body
        self.from_ = from_

def test_sms_data(n,date_from):
    """
    Creates n samples of SMS of a pre-determined body, listed in sample_messages
    If n is >5, then more sample feedback messages must be added to the list below
    """
    #d = random_date(date_from,datetime.now(), n)
    sample_messages = ["First timer. Ordered at counter. Wide selection of healthy choices. Had \"Fish & Chips\" pain plus cup of red pepper soup. Very tasty but pain bun to thick. Tuesday after Labor Day not very busy.",
                        "I was very impressed with Mixed! Not only was the food delicious (I had the club panini & lasagna soup) the staff was extremely friendly. Will definitely be back and highly recommend!! Great find for a fresh and healthy option.",
                        "Visiting family from California and we dropped by this place. My mom loved the Caribbean crunch salad. I had the opah and is was okay. It had black olive instead of kalamata olives which was disappointing. Serving sizes are huge but overall I was underwhelmed by my salad. My brother had a wrap that looked tastey",
                        "It's just ok. Nothing to write home about or admit to anyone that I came here on a Friday night.",
                        "The food was amazing and the service was excellent! 5/5!"
                        ] # sample messages for running tests. TODO: generate/scrape random feedback
    messages = []
    for y in range(0,n):
        msg = TestMessages(y, datetime.now(),sample_messages[y], "+12345678905")
        messages.append(msg)
    return messages

def auto_generate_sms_data(n=25, date_from=(datetime.now() - timedelta(days=60))):
    '''Generates random feedback data
    Arguments:
        n(int): number of items to generate
        date_from(datetime): starting date time. Ending date time used is datetime.now()

    Returns:
        messages(TestMessage): message with same format as Twilio message to store in database
    '''
    Config = configparser.ConfigParser()
    file = os.path.join(os.path.dirname(__file__),"criteriaLists.ini")
    Config.read(file)
    configDict = {}
    options = Config.options("SectionOne")
    for option in options:
        try:
            configDict[option] = Config.get("SectionOne", option)
        except:
            configDict[option] = None

    allLists = ["hello"]
    posWordList = configDict['poslist'].split(' ')
    negWordList = configDict['neglist'].split(' ')
    exceptionWordList = configDict['exceptionlist'].split(' ')
    negationWordList = configDict['negationlist'].split(' ')
    emphasisWordList = configDict['emphasislist'].split(' ')
    foodWordList = configDict['foodlist'].split(' ')
    serviceWordList = configDict['servicelist'].split(' ')
    stopWordList = configDict['stoplist'].split(' ')
    allLists.extend(posWordList)
    allLists.extend(negWordList)
    allLists.extend(stopWordList)
    allLists.extend(exceptionWordList)
    allLists.extend(negationWordList)
    allLists.extend(emphasisWordList)
    allLists.extend(foodWordList)
    allLists.extend(serviceWordList)

    delta = datetime.now() - date_from
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    messages = []
    for m in range(0,n):
        random_second = randrange(int_delta)
        rand_time = date_from + timedelta(seconds=random_second)
        msg = TestMessages(m, rand_time, random_word(allLists), "+1231234123")
        messages.append(msg)
    return messages

def random_word(allLists,max=13):
    '''Helper function to generate random sentence 
    Arguments:
        allLists(List(str)): List of strings of available words to use
        max: max length of the sentence
    '''
    random_num_words = randrange(max)
    random_index = randrange(1,len(allLists)-1)
    sentence = ""
    for n in range(0,random_num_words):
        random_index = randrange(1,len(allLists)-1)
        sentence = sentence + allLists[random_index] +' '
    return sentence