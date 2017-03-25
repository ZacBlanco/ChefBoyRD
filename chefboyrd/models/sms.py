from peewee import TextField, DateTimeField, Model
from chefboyrd.models import BaseModel

class Sms(Model):
	'''
	sid is an unique id assigned by twilio. it will help us keep track of sms that is in, or not in db
	'''
	sid = TextField()
	submission_time = DateTimeField()
	body = TextField()
	phone_num = TextField()
	#additional categories to associate	
