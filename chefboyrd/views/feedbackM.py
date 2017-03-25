from flask import Blueprint, render_template, abort, url_for, redirect
from flask_table import Table, Col
from jinja2 import TemplateNotFound
from flask_wtf import FlaskForm
from wtforms import DateTimeField, SubmitField
from chefboyrd.auth import require_role
from chefboyrd.models.sms import Sms
from datetime import datetime

page = Blueprint('feedbackM', __name__, template_folder='./templates')

class ItemTable(Table):
    html_attrs = {'class': 'table table-striped'}
    sid = Col('Sid')
    submission_time = Col('Submission Time')
    body = Col('Body')
    phone_num = Col('Phone Number')
    #cancel = ButtonCol('Cancel','reservationH.cancel',url_kwargs=dict(id='id'),button_attrs={'class': 'btn btn-danger'})

class DateSpecifyForm(FlaskForm):
    date_time_from = DateTimeField(datetime.today(),format='%Y-%m-%d %H:%M:%S')
    date_time_to = DateTimeField(datetime.now(),format='%Y-%m-%d %H:%M:%S')
    submit_field = SubmitField("search")
    #phone = StringField('Phone Number', [validators.Length(min=10, max=10)])
    #phone = PhoneNumberField('Phone Number')
    #start = DateTimeField('Time and Date')

@page.route("/",methods=['GET', 'POST'])
@require_role('admin')
def feedback_table():
    #get all of the feedback objects and insert it into table
    form = DateSpecifyForm()
    if form.validate_on_submit():
        smss = Sms.select().where(
        	(Sms.submission_time > form.date_time_from)
        	and (Sms.submission_time <= form.date_time_to)
        	).orderby(Sms.submission_time)
    else:
    	smss = Sms.select()
    res = []
    for sms in smss:
        res.append(dict(sid=sms.sid,submission_time=sms.submission_time,body=sms.body,phone_num=sms.phone_num))
    table = ItemTable(res)
    if not (res == []):
        return render_template('feedbackM/index.html', logged_in=True, table=table)
