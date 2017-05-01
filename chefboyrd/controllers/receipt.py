"""Interfaces with an external system that generates receipts

written by: Seo Bo Shim
tested by: Seo Bo Shim
debugged by: Seo Bo Shim
"""

from chefboyrd.models.statistics import Tabs
from peewee import IntegrityError
from string import punctuation
from datetime import datetime, date, timedelta
import configparser
import os
from chefboyrd.tests.test_fb_data import test_sms_data, TestMessages
import json
import os


def get_receipts():
	"""Generates a .json file at the root directory with information for each tab, including unique ID
	Returns:
		N/A
	"""
	tabs = Tabs.select()
	f = open('receipts.json','w+')

	for tab in tabs:
		hr = str(tab.had_reservation)
		tab_dict = {'had_reservation': hr,
						'party_size': str(tab.party_size),
						'timestamp': tab.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
						'fb_key': tab.fb_key
						}
		tab_json = json.dumps(tab_dict)
		f.write(tab_json)
		f.write('\n\n\n')
	f.close()
	return