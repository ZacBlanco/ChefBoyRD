from flask import Blueprint, render_template, abort, url_for, redirect, request
from flask_table import Table, Col, create_table
from jinja2 import TemplateNotFound
from flask_wtf import FlaskForm
from wtforms import DateTimeField, SubmitField
from chefboyrd.auth import require_role
from chefboyrd.controllers import feedback_controller, send_sms
from chefboyrd.models.sms import Sms
from datetime import datetime
import copy

page = Blueprint('feedbackM', __name__, template_folder='./templates')

class DateSpecifyForm(FlaskForm):
    '''
    The form that should be submitted to get feedback tables within the specified date range
     '''

    date_time_from = DateTimeField('Time From',format='%Y-%m-%d %H:%M:%S')
    date_time_to = DateTimeField('Time To',format='%Y-%m-%d %H:%M:%S')
    submit_field = SubmitField("search")

@page.route("/",methods=['GET', 'POST'])
@require_role('admin')
def feedback_table():
    '''
    Display a table of feedback sent in during a specified date-time range.
    By default all feedback in database will be displayed
    '''
    TableCls = create_table('TableCls')
    #get all of the feedback objects and insert it into table
    form = DateSpecifyForm()
    if (request.method== 'POST'):
        time_col, body_col, pos_col, neg_col, except_col, food_col, service_col, feedback_analyze = (0,0,0,0,0,0,0,0)
        dtf = datetime.strptime(request.form['datetimefrom'], "%m/%d/%Y %H:%M %p")
        dtt = datetime.strptime(request.form['datetimeto'], "%m/%d/%Y %H:%M %p")
        
        if (request.form.get('Time')):
            TableCls.add_column('Time', Col('Time'))
            time_col = 1
        if (request.form.get('Body')):
            TableCls.add_column('Body', Col('Body'))
            body_col = 1
        if (request.form.get('Positive')):
            TableCls.add_column('Positive', Col('Positive'))
            pos_col = 1
        if (request.form.get('Negative')):
            TableCls.add_column('Negative', Col('Negative'))
            neg_col = 1
        if (request.form.get('Exception')):
            TableCls.add_column('Exception', Col('Exception'))
            except_col = 1
        if (request.form.get('Food')):
            TableCls.add_column('Food', Col('Food'))
            food_col = 1
        if (request.form.get('Service')):
            TableCls.add_column('Service', Col('Service'))
            service_col = 1
        
        smss = Sms.select().where(
        	(Sms.submission_time  > dtf)
        	& (Sms.submission_time <= dtt)
        	).order_by(-Sms.submission_time)
        
        if (pos_col ==1 or neg_col==1 or except_col==1 or food_col==1 or service_col==1):
            feedback_analyze=1
        if (request.form.get('WordCloud') == 1):
            pass
            #feedback_controller.word_freq_counter()
        res = []
        all_string_bodies = ""
        for sms in smss:
            tmp_dict = dict()
            #print(sms.submission_time)
            #res.append(dict(submission_time=sms.submission_time,body=sms.body))
            if time_col==1:
                tmp_dict['Time']=sms.submission_time
            if body_col==1:
                tmp_dict['Body']=sms.body
            if feedback_analyze==1:
                if (sms.pos_flag > -1): #if feedback analysis exists
                    pass
                else:
                    res2 = feedback_controller.feedback_analysis(sms.body)
                    sms.pos_flag = res2[0]
                    sms.neg_flag = res2[1]
                    sms.exception_flag = res2[2]
                    sms.food_flag = res2[3]
                    sms.service_flag = res2[4]
                    sms.update()
            if pos_col==1:
                tmp_dict['Positive']=sms.pos_flag
            if neg_col==1:
                tmp_dict['Negative']=sms.neg_flag
            if except_col==1:
                tmp_dict['Exception']=sms.exception_flag
            if food_col==1:
                tmp_dict['Food']=sms.food_flag
            if service_col==1:
                tmp_dict['Service']=sms.service_flag
            if res == []:
                res = [copy.deepcopy(tmp_dict)]
                #print(sms.body)
            else:
                res.append(copy.deepcopy(tmp_dict))

        #     all_string_bodies = all_string_bodies + sms.body + ","
        # if (request.form.get('WordCloud')):
        #     word_freq = feedback_controller.word_freq_counter(all_string_bodies)
        # else:
        # 	word_freq = []
        # #print(word_freq)
        table = TableCls(res)
    else:
        res = []
        table = TableCls(res)
    if not (res == []):
        return render_template('feedbackM/index.html', logged_in=True, table=table, form=form, word_freq=word_freq)
    else:
        return render_template('feedbackM/index.html', logged_in=True, form=form)

@page.route("/deleteallfeedbackhistory",methods=['GET', 'POST'])
@require_role('admin')
def delete_feedback():
    '''
    Deletes all feedback history on twilio and in database.
    Should only be done once before demo.
    '''
    send_sms.delete_feedback()
    query = Sms.delete() # deletes all SMS objects
    res = query.execute()
    return String.format("%03d amount of sms entries deleted", res)
