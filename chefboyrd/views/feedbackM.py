from flask import Blueprint, render_template, abort, url_for, redirect, request
from flask_table import Table, Col
from jinja2 import TemplateNotFound
from flask_wtf import FlaskForm
from wtforms import DateTimeField, SubmitField
from chefboyrd.auth import require_role
from chefboyrd.models.sms import Sms
from datetime import datetime

page = Blueprint('feedbackM', __name__, template_folder='./templates')

class ItemTable(Table):
    '''
    Table to be displayed as the list of all feedback received in a time range.
    The following fields are the columns to be displayed
    '''
    html_attrs = {'class': 'table table-striped'}
    #sid = Col('Sid')
    submission_time = Col('Submission Time')
    body = Col('Body')
    #phone_num = Col('Phone Number')
    

class DateSpecifyForm(FlaskForm):
    '''
    The form that should be submitted to get feedback tables within the specified date range
     '''
    #,datetime.today() ,datetime.now()
    date_time_from = DateTimeField('Date&Time From',format='%Y-%m-%d %H:%M:%S')
    date_time_to = DateTimeField('Date&Time To',format='%Y-%m-%d %H:%M:%S')
    submit_field = SubmitField("search")
    #phone = StringField('Phone Number', [validators.Length(min=10, max=10)])
    #phone = PhoneNumberField('Phone Number')
    #start = DateTimeField('Time and Date')

@page.route("/",methods=['GET', 'POST'])
@require_role('admin')
def feedback_table():
    '''
    Display a table of feedback sent in during a specified date-time range.
    By default all feedback in database will be displayed
    '''
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
        res.append(dict(submission_time=sms.submission_time,body=sms.body))
    table = ItemTable(res)
    if not (res == []):
        return render_template('feedbackM/index.html', logged_in=True, table=table, form=form)
    else:
    	return render_template('feedbackM/index.html', logged_in=True, form=form)
