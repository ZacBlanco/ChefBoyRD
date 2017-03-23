from chefboyrd import DB as db
from peewee import *

class Sms(Model):
	id = PrimaryKeyField()
	submission_time = DateTimeField()
	body = TextField()
	phone_number = TextField()
	#additional categories to associate
	
	class Meta:
		database = db
