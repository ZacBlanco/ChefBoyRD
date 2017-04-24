'''
Shift management dashboard for the manager interface
'''
import json
import flask_login
from flask import Flask, Blueprint, render_template, request, url_for, jsonify, redirect
from flask_table import Table, Col, ButtonCol
from flask_wtf import FlaskForm, CsrfProtect
from wtforms import StringField, IntegerField, validators
from wtforms.ext.dateutil.fields import DateTimeField
from datetime import datetime   
from jinja2 import TemplateNotFound
import os 
from chefboyrd.auth import require_role
from chefboyrd.models.shifts import Shift
from chefboyrd.controllers import shift_controller


page = Blueprint('shift_manager', __name__, template_folder='./templates')

class ShiftForm(FlaskForm):
    '''
    This is the form that displays fields to make a shift
    '''
    start = DateTimeField('Shift Starting Time')
    end = DateTimeField('Shift Ending Time')
    role = StringField('Role', [validators.Length(min=2, max=25)])

class FreeTable(Table):
    '''
    This FreeTable class generates a table of the avaliable/open shifts.
    It also has a button to remove a shift
    '''
    shift_time_start = Col('Starting Time')
    shift_time_end = Col('Ending Time')
    role = Col('Role')
    claim = ButtonCol('Claim Shift', 'shift_manager.claim', url_kwargs=dict(id='id'), button_attrs={'class': 'btn btn-success'})
    remove = ButtonCol('Remove Shift', 'shift_manager.remove', url_kwargs=dict(id='id'), button_attrs={'class': 'btn btn-danger'})

class ClaimTable(Table):
    '''
    This ClaimTable class generates a table of the claimed shifts.
    It also has a button to post a shift
    '''
    name = Col('Employee Name')
    shift_time_start = Col('Starting Time')
    shift_time_end = Col('Ending Time')
    role = Col('Role')
    post = ButtonCol('Post Shift', 'shift_manager.post',url_kwargs=dict(id='id'), button_attrs={'class': 'btn btn-warning'})

@page.route("/", methods=['GET', 'POST'])
@require_role('admin')
def calendar():
    '''
    Renders the index page of the shift management page
    '''
    form = ShiftForm()
    if form.validate_on_submit():
        Shift.create_shift("", form.start.data, form.end.data, form.role.data)
    free_shifts = []
    current_time = datetime.now()
    for freeShift in Shift.select().where((Shift.name=="") & (Shift.shift_time_end > current_time)):
        free_shifts.append(dict(shift_time_start=freeShift.shift_time_start, shift_time_end=freeShift.shift_time_end, role=freeShift.role, id=freeShift.id))
    freeTable = FreeTable(free_shifts)
    claim_shifts = []
    for claimShift in Shift.select().where((Shift.name!="") & (Shift.shift_time_end > current_time)):
        claim_shifts.append(dict(name=claimShift.name, shift_time_start=claimShift.shift_time_start, shift_time_end=claimShift.shift_time_end, role=claimShift.role, id=claimShift.id))
    claimTable = ClaimTable(claim_shifts)
    return render_template('/shift_manager/index.html', logged_in=True, freeTable=freeTable, claimTable = claimTable, form=form)

@page.route('/data')
def return_data():
    start_date = request.args.get('start', '')
    end_date = request.args.get('end', '')
    current_time = datetime.now()
    shift_json = []
    for s in Shift.select().where((Shift.shift_time_end < current_time) & (Shift.name!= "")):
        shift_json.append(dict(title=s.name+'-'+s.role,start=str(s.shift_time_start),end=str(s.shift_time_end), backgroundColor='#85929E'))
    for s in Shift.select().where((Shift.name=="") & (Shift.shift_time_end > current_time)):
        shift_json.append(dict(title=s.role,start=str(s.shift_time_start),end=str(s.shift_time_end), backgroundColor='#66ff66'))
    for s in Shift.select().where((Shift.name!="") & (Shift.shift_time_end > current_time)):
        shift_json.append(dict(title=s.name+'-'+s.role,start=str(s.shift_time_start),end=str(s.shift_time_end), backgroundColor='#3399ff'))
    print(shift_json)
    return json.dumps(shift_json)

@page.route("/claim", methods=['GET', 'POST'])
@require_role('admin')
def claim():
    '''
    This handles when the user needs to claim a shift
    '''
    id = request.args.get('id')
    name = flask_login.current_user.name
    role = flask_login.current_user.role
    if shift_controller.checkAvailability(id, name, role):
        Shift.claim_shift(id, name)
    return redirect(url_for('shift_manager.calendar'))

@page.route("/post", methods=['GET', 'POST'])
@require_role('admin')
def post():
    '''
    This handles when the user needs to post a shift
    '''
    id = request.args.get('id')
    Shift.post_shift(id)
    return redirect(url_for('shift_manager.calendar'))

@page.route("/remove", methods=['GET', 'POST'])
@require_role('admin')
def remove():
    '''
    This handles when the user needs to remove a shift
    '''
    id = request.args.get('id')
    Shift.remove_shift(id)
    return redirect(url_for('shift_manager.calendar'))