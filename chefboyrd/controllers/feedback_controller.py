from datetime import datetime
from chefboyrd.models.sms import Sms
import configparser
import os
from string import punctuation

def update_db(*sid_list):
    '''
    Helper function that can be used to update the database based on the sid list given

    Args:
        sid_list: list of message sids to update into the db. sid is unique text identifier
    '''
    for sid in sid_list:
        try:
            sms_tmp = Sms.select().where(Sms.sid==sid)
            #feedbackAnalyse(sms_tmp.body)
            sms_tmp = Sms(
                sid=message.sid,
                submission_time=message.date_sent,
                body=message.body, 
                phone_num=message.from_
                )
            #print(sms_tmp.body)
            #print(sms_tmp.submission_time) 
            if not (sms_tmp.save()):
                print("sms could not be saved in sb")
        except ValueError:
            print("End of messages reached.")
            return 0
    return 1

def feedback_analysis(inStr):
    '''Determines aspects of input string based on word content.

    Extended description:

    Args:
        inStr (string): String containing words separated by spaces or
                        non-apostrophe punctuation.

    Returns:
        list(posFlag,negFlag,exceptionFlag,foodFlag,serviceFlag):
            A list of integers representing whether the input string
            meets the necessary criteria to be flagged as positive,
            negative, food-related, service-related or contains an exception

    Throws:
        TypeError: When argument is not a string
        
    '''

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
    '''Determines frequency of each word in input string.

    Extended description:

    Args:
        inStr (string): String containing words separated by spaces or
                        non-apostrophe punctuation.

    Returns:
        resultDict: A dictionary mapping the distinct words within inStr
                    to its number of occurrences within the input

    Throws:
        TypeError: When argument is not a string
        
    '''

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