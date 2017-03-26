from datetime import datetime
from chefboyrd.models import Sms

def

def update_db(*sid_list):
	'''
	Helper function that can be used to update the database
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

def feedbackAnalysis(inStr):

    posFlag = 0
    negFlag = 0
    exceptionFlag = 0
    foodFlag = 0
    serviceFlag = 0

    inStrProcessed = inStr
    from string import punctuation
    for p in list(punctuation):
        if p != '\'':
            inStrProcessed = inStrProcessed.replace(p,' ')

    inStrProcessed = inStrProcessed.lower()
    print("Processed word list: ")
    wordsProcessed = inStrProcessed.split(' ')
    wordsProcessed = list(filter(bool,wordsProcessed))
    print(wordsProcessed)

    posWordList = ('good','excellent','happy','awesome','delightful','wonderful',
                   'exceptional','cool','great','fun','amazing','delicious',
                   'satisfied','satisfy','satisfies','satisfying','enjoy','enjoys',
                   'enjoying','enjoyed','liked','likes','adore','adored','adores',
                   'adoring','savor','savory','savored','savoring','savors','love',
                   'like','loves','loved','compliment','compliments','fine','superior',
                   'outstanding','magnificent','satisfactory','terrific','fantastic',
                   'fabulous','classy','tasty','mouthwatering','appetizing',
                   'flavorful','delectable','palatable','succulent','luscious',
                   'special','pleasant','lovely','exquisite','pleasurable','positive'
                   'remarkable','pleasing','clean','spotless','pristine')

    negWordList = ('bad','horrible','negative','disgusting','foul','awful','sad',
                   'angry', 'unsatisfactory','inadequate','unacceptable','deficient',
                   'shoddy','atrocious','deplorable','terrible','absymal',
                   'inappropriate','unpleasant','unwelcome','rancid','revolting',
                   'repulsive','sickening','nauseating','unpalatable','distasteful',
                   'nasty','abhorrent','gross','disliked','dislike','dislikes',
                   'unappetizing','unremarkable','displeasing','unsanitary','unclean',
                   'greasy','filthy')


    exceptionWordList = ('but','yet','nevertheless','nonetheless','however','despite',
                      'whereas','conversely','except','actually')

    negationWordList = ('not','no','wasnt','wasn\'t','isnt','isn\'t','arent','aren\'t',
                        'werent','weren\'t','dont','don\'t','didnt','didn\'t','doesnt',
                        'doesn\'t')

    emphasisWordList = ('very','extremely','that','exceptionally','particularly','really',
                        'quite','exceedingly','decidedly','highly','remarkably','awfully',
                        'too')

    foodWordList = ('food','dish','dishes','meal','meals','drink','drinks','appetizer',
                    'appetizers')

    serviceWordList = ('service','services','waiter','waiters','waitress','waitresses',
                       'waitperson','waitpersons','attendant','attendants','cashier',
                       'cashiers','host','hosts','hostess','hostesses','staff','manager',
                       'wait','delay')

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

    return list(posFlag,negFlag,exceptionFlag,foodFlag,serviceFlag)
