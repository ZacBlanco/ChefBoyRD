from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from chefboyrd.controllers import customer_controller, send_sms

page = Blueprint('test_sms', __name__, template_folder='templates')

@page.route('/',methods=['POST'])
def test_sms():
	send_sms.rcv_sms()
	return 'hi'
