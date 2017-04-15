"""
feedbackM
This view is specifically for the administrative staff's management of the feedback
"""

from flask import Blueprint, render_template, abort, url_for, redirect, request
from flask_table import Table, Col, create_table
from jinja2 import TemplateNotFound
from flask_wtf import FlaskForm
from wtforms import DateTimeField, SubmitField
from chefboyrd.auth import require_role
from chefboyrd.controllers import feedback_controller
from chefboyrd.models.sms import Sms
from datetime import datetime, date
import copy

page = Blueprint('feedbackM', __name__, template_folder='./templates')

class ItemTable(Table):
    """
    FlaskTable object for organizing feedback info into a table

    """
    time = Col('Time', column_html_attrs={'class': 'spaced-table-col'})
    body = Col('Body')

class DateSpecifyForm(FlaskForm):
    """WTforms object for the date-time form submission for the DB query"""

    date_time_from = DateTimeField('Time From')
    date_time_to = DateTimeField('Time To')
    submit_field = SubmitField("search")

@page.route("/",methods=['GET', 'POST'])
@require_role('admin')
def feedback_table():
    """
    By default displays a webpage for user to make feedback DB query.
    Display a table of feedback sent in during a specified date-time range.
    Also, depending on whether category flags are specified, this page will only display

    Returns:
        The template to display with the appropriate parameters
	table: table of feedback to display
	form: form that specifies the query instructions.
    """
    #get all of the feedback objects and insert it into table
    form = DateSpecifyForm()
    if (request.method== 'POST'):
        pos_col, neg_col, except_col, food_col, service_col= (-1,-1,-1,-1,-1) # -1 is a don't care term
        dtf = datetime.strptime(request.form['datetimefrom'], "%m/%d/%Y %I:%M %p")
        dtt = datetime.strptime(request.form['datetimeto'], "%m/%d/%Y %I:%M %p")
        if (request.form.get('dropdown') =='Good'):
            #print('Form Good')
            pos_col, neg_col = (1,0)
            smss = Sms.select().where(
                (Sms.submission_time  > dtf)& 
                (Sms.submission_time <= dtt)&
                (Sms.pos_flag==pos_col)&
                (Sms.neg_flag==neg_col)
                ).order_by(-Sms.submission_time)
        elif (request.form.get('dropdown') =='Bad'):
            pos_col, neg_col = (0,1)
            smss = Sms.select().where(
                (Sms.submission_time  > dtf)& 
                (Sms.submission_time <= dtt)&
                (Sms.pos_flag==pos_col)&
                (Sms.neg_flag==neg_col)
                ).order_by(-Sms.submission_time)
        elif (request.form.get('dropdown') =='Mixed'):
            pos_col, neg_col = (1,1)
            smss = Sms.select().where(
                (Sms.submission_time  > dtf)& 
                (Sms.submission_time <= dtt)&
                (Sms.pos_flag==pos_col)&
                (Sms.neg_flag==neg_col)
                ).order_by(-Sms.submission_time)
        elif (request.form.get('dropdown') == 'Food'):
            food_col = 1
            smss = Sms.select().where(
                (Sms.submission_time  > dtf)& 
                (Sms.submission_time <= dtt)&
                (Sms.food_flag == food_col)
                ).order_by(-Sms.submission_time)
        elif (request.form.get('dropdown') == 'Service'):
            service_col = 1
            smss = Sms.select().where(
                (Sms.submission_time  > dtf)& 
                (Sms.submission_time <= dtt)&
                (Sms.service_flag == service_col)
                ).order_by(-Sms.submission_time)
        elif (request.form.get('dropdown') =='Exception'):
            except_col = 1
            smss = Sms.select().where(
                (Sms.submission_time  > dtf)& 
                (Sms.submission_time <= dtt)&
                (Sms.exception_flag==except_col)
                ).order_by(-Sms.submission_time)
        else:
            pos_col, neg_col, except_col,food_col, service_col = (-1,-1,-1,-1,-1)
            smss = Sms.select().where(
                (Sms.submission_time  > dtf)& 
                (Sms.submission_time <= dtt)
                ).order_by(-Sms.submission_time)

        #if (request.form.get('WordCloud') == 1):
        #    pass
            #feedback_controller.word_freq_counter()
        res = []
        all_string_bodies = ""
        #print(len(smss))
        for sms in smss:
            #print('pos:{} neg:{} except:{} food:{} service:{}'.format(sms.pos_flag,sms.neg_flag, sms.exception_flag, sms.food_flag, sms.service_flag))
            res.append(dict(time=sms.submission_time.strftime("%Y-%m-%d %H:%M"),body=sms.body))

        #     all_string_bodies = all_string_bodies + sms.body + ","
        # if (request.form.get('WordCloud')):
        #     word_freq = feedback_controller.word_freq_counter(all_string_bodies)
        # else:
        # 	word_freq = []
        # #print(word_freq)
        table = ItemTable(res)
    else:
        res = []
        table = ItemTable(res)
    if not (res == []):
        return render_template('feedbackM/index.html', logged_in=True, table=table, form=form)
    else:
        return render_template('feedbackM/index.html', logged_in=True, form=form)

@page.route("/deleteallfeedbackhistory",methods=['GET', 'POST'])
@require_role('admin')
def delete_feedback():
    """
    Calls the delete_feedback function, returns a message confirming # of feedback entries deleted

    Returns:
        Confirmation string
    """
    res = feedback_controller.delete_feedback()
    return String.format("%03d amount of sms entries deleted", res) 

@page.route("/deletealltwiliofeedbackhistory",methods=['GET', 'POST'])
@require_role('admin')
def delete_twilio_feedback():
    """
    wipe all message history on twilio. Only needs to be called once to clear data.

    Returns:
        Confirmation string
    """
    feedback_controller.delete_twilio_feedback()
    return "Twilio Feedback deleted"

@page.route("/updateallsms",methods=['GET','POST'])
@require_role('admin')
def update_all_sms():
    """
    Update sms data from external Twilio database

    Returns:
        Confirmation string
    """
    feedback_controller.update_db()
    return "db updates with all sms: Success"

@page.route('/twiliosms',methods=['POST'])
def send_sms_route():
    """
    This is the directory we need to configure twilio for.
    When Twilio makes a POST request, db will be updated with new sms messages from today
    Returns:
        Confirmation string
    """
    feedback_controller.update_db(date.today())
    return 'db updated'
