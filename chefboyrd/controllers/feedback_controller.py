'''
This houses all the functions to add or delete sms objects into the database
Also includes the feedback analysis functions

'''
from chefboyrd.models.sms import Sms
from twilio.rest import TwilioRestClient
import twilio.twiml
from peewee import IntegrityError
from string import punctuation
from datetime import datetime, date, timedelta
import configparser
import os

config = configparser.RawConfigParser()
config.read(os.path.join(os.path.dirname(__file__),'sms.cfg')) #assuming config file same path as this controller
account_sid = config['keys']['account_sid']
auth_token = config['keys']['auth_token']
cust_phone_number = config['test']['cust_phone_number']
restaurant_phone_number = config['test']['restaurant_phone_number']


def update_db(*date_from):
    '''
    updates the sms in the database starting from the date_from specified (at time midnight)
    no param = updates the sms feedback in database with all message entries
    analyze feedback when sms is sent
    TODO: this may create duplicate entries, should test this 
    TODO: Fix error with twilio, where the most recent message does not have a submission timep
    TODO: Fix possible error with DST. TImezone was hotfix

    Args:
        date_from (date object): a specified date, where we update db with sms sent after this date
    Returns:
        1 on success. 0 on error
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
            res2 = feedback_analysis(sms_tmp.body)
            sms_tmp.pos_flag = res2[0]
            sms_tmp.neg_flag = res2[1]
            sms_tmp.exception_flag = res2[2]
            sms_tmp.food_flag = res2[3]
            sms_tmp.service_flag = res2[4]
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
            #print("Duplicate Sms Entry " + sms_tmp.body)
            #raise IntegrityError
    return 1 #this should be on success


def delete_twilio_feedback():
    '''
    wipe all message history on twilio
    '''
    try:
        client = TwilioRestClient(account_sid,auth_token)
    except:
        raise SystemError("Could not communicate with Twilio Rest client");
    messages = client.messages.list()
    for message in messages:
        try:
            client.messages.delete(message.sid)
        except ValueError:
            print("End of messages list reached.")
            return 0
    return 1

def delete_feedback():
    '''
    Deletes all feedback history in database.
    Should only be done once before demo.
    '''
    query = Sms.delete() # deletes all SMS objects
    res = query.execute()
    return res

def feedback_analysis(inStr):
    """Determines aspects of input string based on word content.

    Extended description:

    Args:
        inStr (string): String containing words separated by spaces or
                        non-apostrophe punctuation.

    Returns:
        list(posFlag,negFlag,exceptionFlag,foodFlag,serviceFlag):
            A list of integers representing whether the input string
            meets the necessary criteria to be flagged as positive,
            negative, food-related, service-related or contains an exception.

    Throws:
        TypeError: When argument is not a string.
        
    """

    if not isinstance(inStr, str):
        raise TypeError("Input must be a string")
    
    posFlag = 0
    negFlag = 0
    exceptionFlag = 0
    foodFlag = 0
    serviceFlag = 0

    Config = configparser.ConfigParser()
    Config.read(os.path.join(os.path.dirname(__file__),"criteriaLists.ini"))
    configDict = {}
    options = Config.options("SectionOne")
    for option in options:
        try:
            configDict[option] = Config.get("SectionOne", option)
        except:
            configDict[option] = None
            
    posWordList = configDict['poslist']
    posWordList = posWordList.split(' ')
    negWordList = configDict['neglist']
    negWordList = negWordList.split(' ')
    exceptionWordList = configDict['exceptionlist']
    exceptionWordList = exceptionWordList.split(' ')
    negationWordList = configDict['negationlist']
    negationWordList = negationWordList.split(' ')
    emphasisWordList = configDict['emphasislist']
    emphasisWordList = emphasisWordList.split(' ')
    foodWordList = configDict['foodlist']
    foodWordList = foodWordList.split(' ')
    serviceWordList = configDict['servicelist']
    serviceWordList = serviceWordList.split(' ')

    inStrProcessed = inStr
    for p in list(punctuation):
        if p != '\'':
            inStrProcessed = inStrProcessed.replace(p,' ')

    inStrProcessed = inStrProcessed.lower()
    wordsProcessed = inStrProcessed.split(' ')
    wordsProcessed = list(filter(bool,wordsProcessed))
    
    for i, word in enumerate(wordsProcessed):
        if word in posWordList:
            if i > 0:
                if wordsProcessed[i-1] in negationWordList:
                    negFlag = 1
                else:
                    if wordsProcessed[i-1] in emphasisWordList and i > 1:
                        if wordsProcessed[i-2] in negationWordList:
                            negFlag = 1
                        else:
                            posFlag = 1
                        
                    else:
                        posFlag = 1
            else:
                posFlag = 1

    for i, word in enumerate(wordsProcessed):
        if word in negWordList:
            if i > 0:
                if wordsProcessed[i-1] in negationWordList:
                    posFlag = 1
                else:
                    if wordsProcessed[i-1] in emphasisWordList and i > 1:
                        if wordsProcessed[i-2] in negationWordList:
                            posFlag = 1
                        else:
                            negFlag = 1
                        
                    else:
                        negFlag = 1
            else:
                negFlag = 1

    for word in wordsProcessed:
        if word in exceptionWordList:
            exceptionFlag = 1
            break

    for word in wordsProcessed:
        if word in foodWordList:
            foodFlag = 1
            break

    for word in wordsProcessed:
        if word in serviceWordList:
            serviceFlag = 1
            break
            
    #print("posFlag = {}:\nnegFlag = {}:\nexceptionFlag = {}:".format(posFlag,negFlag,exceptionFlag),
    #     "\nfoodFlag = {}:\nserviceFlag = {}:".format(foodFlag,serviceFlag))

    return [posFlag,negFlag,exceptionFlag,foodFlag,serviceFlag]


def word_freq_counter(inStr):
    """Determines frequency of each word in input string.

    Extended description:

    Args:
        inStr (string): String containing words separated by spaces or
                        non-apostrophe punctuation.

    Returns:
        resultDict: A list of dictionary elements mapping the each distinct word within inStr
                    to its number of occurrences in the input.

    Throws:
        TypeError: When argument is not a string.
        
    """

    if not isinstance(inStr, str):
        raise TypeError("Input must be a string")
    
    inStrProcessed = inStr
    for p in list(punctuation):
        if p != '\'':
            inStrProcessed = inStrProcessed.replace(p,' ')

    inStrProcessed = inStrProcessed.lower()
  
    wordsProcessed = inStrProcessed.split(' ')
    wordsProcessed = list(filter(bool,wordsProcessed))
    #print("Processed word list: ")
    #print(wordsProcessed)
    #print("\n",set(wordsProcessed))
    wordSet = []
    freqs = [0 for x in range(len(set(wordsProcessed)))]
    #print(freqs,"\n")
    for word in set(wordsProcessed):
        if word not in wordSet:
            wordSet.append(word)
    #print(wordSet)

    for i, word in enumerate(wordSet):
        for  word2 in wordsProcessed:
            if word == word2:
                freqs[i] = freqs[i] + 1
                
    res = []
    n = 0
    for n in range(len(wordSet)):
        res.append(dict(text=wordSet[n],size=freqs[n]))
    resultDict = res
    return resultDict

#muhStr = input("Enter the string: ")
#dictOut = wordFreqCounter(muhStr)
#print(dictOut)
