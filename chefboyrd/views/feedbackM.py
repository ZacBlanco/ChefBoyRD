from flask import Blueprint, render_template, abort, url_for, redirect
from flask_table import Table, Col, ButtonCol
from chefboyrd.auth import require_role
from chefboyrd.models.sms import Sms

page = Blueprint('feedbackM', __name__, template_folder='./templates')

class ItemTable(Table):
    html_attrs = {'class': 'table table-striped'}
    sid = Col('Sid')
    submission_time = Col('Submission Time')
    body = Col('Body')
    phone_num = Col('Phone Number')
    #cancel = ButtonCol('Cancel','reservationH.cancel',url_kwargs=dict(id='id'),button_attrs={'class': 'btn btn-danger'})


@page.route("/",methods=['GET', 'POST'])
@require_role('admin')
def feedback_table():

	#get all of the feedback objects and insert it into table
    res = []
    for sms in Sms.select():
        res.append(dict(sid=sms.sid,submission_time=sms.submission_time,body=sms.body,phone_num=sms.phone_num))
    table = ItemTable(res)
    if not (res == []):
        return render_template('feedbackM/index.html', logged_in=True, table=table)
