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
