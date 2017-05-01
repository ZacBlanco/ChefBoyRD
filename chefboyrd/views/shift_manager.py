'''
Shift management dashboard for the manager interface
'''
import json
import flask_login
from flask import Flask, Blueprint, render_template, request, url_for, redirect, flash
from flask_table import Table, Col, ButtonCol
from flask_wtf import FlaskForm, CsrfProtect
from wtforms import SelectField, SubmitField, validators
from wtforms.ext.dateutil.fields import DateTimeField
from datetime import datetime   
from jinja2 import TemplateNotFound
import os 
from chefboyrd.auth import require_role
from chefboyrd.models.shifts import Shift
from chefboyrd.models.user import User
from chefboyrd.controllers import shift_controller

page = Blueprint('shift_manager', __name__, template_folder='./templates')

class ShiftForm(FlaskForm):
    '''
    This is the form that displays fields to make a shift
    '''
    role = SelectField('Role', validators=[validators.required()])
    start = DateTimeField('Shift Starting Time', validators=[validators.required()])
    end = DateTimeField('Shift Ending Time', validators=[validators.required()])
    submit = SubmitField("Add Shift")

class CheckForm(FlaskForm):
    '''
    This is the form that allows users to pick between different people that work at the same place.
    '''
    user = SelectField('')
    submit = SubmitField("Check Shift")

class FreeTable(Table):
    '''
    This FreeTable class generates a table of the avaliable/open shifts.
    It also has a button to remove a shift
    '''
    role = Col('Role', column_html_attrs={'class': 'spaced-table-col'})
    shift_time_start = Col('Starting Time', column_html_attrs={'class': 'spaced-table-col'})
    shift_time_end = Col('Ending Time', column_html_attrs={'class': 'spaced-table-col'})
    claim = ButtonCol('Claim Shift', 'shift_manager.claim', url_kwargs=dict(id='id'), button_attrs={'class': 'btn btn-success'}, column_html_attrs={'class': 'spaced-table-col'})
    remove = ButtonCol('Remove Shift', 'shift_manager.remove', url_kwargs=dict(id='id'), button_attrs={'class': 'btn btn-danger'}, column_html_attrs={'class': 'spaced-table-col'})

class UniqueTable(Table):
    '''
    This UniqueTable class generates a table of the claimed shifts
    for a specific user. It also has a button to post a shift
    '''
    role = Col('Role', column_html_attrs={'class': 'spaced-table-col'})
    shift_time_start = Col('Starting Time', column_html_attrs={'class': 'spaced-table-col'})
    shift_time_end = Col('Ending Time', column_html_attrs={'class': 'spaced-table-col'})
    post = ButtonCol('Post Shift','shift_manager.post',url_kwargs=dict(id='id'),button_attrs={'class': 'btn btn-warning'},column_html_attrs={'class': 'spaced-table-col'})

class ClaimTable(Table):
    '''
    This ClaimTable class generates a table of the claimed shifts.
    It also has a button to post a shift
    '''
    name = Col('Name', column_html_attrs={'class': 'spaced-table-col'})
    role = Col('Role', column_html_attrs={'class': 'spaced-table-col'})
    shift_time_start = Col('Starting Time', column_html_attrs={'class': 'spaced-table-col'})
    shift_time_end = Col('Ending Time', column_html_attrs={'class': 'spaced-table-col'})
    post = ButtonCol('Post Shift','shift_manager.post',url_kwargs=dict(id='id'),button_attrs={'class': 'btn btn-warning'},column_html_attrs={'class': 'spaced-table-col'})

@page.route("/", methods=['GET', 'POST'])
@require_role(['admin','manager','chef','host','waiter'])
def calendar():
    '''
    Renders the index page of the shift management page
    '''
    current_time = datetime.now()
    employee_name = flask_login.current_user.name
    employee_role = flask_login.current_user.role
    form = ShiftForm()
    form.role.choices={(r.role, r.role) for r in User.select()}
    form.role.default=''
    if form.validate_on_submit() and form.submit.data:
        Shift.create_shift("", form.start.data, form.end.data, form.role.data)
    free_shifts = []
    for freeShift in Shift.select().where((Shift.name=="") & (Shift.shift_time_end > current_time)):
        free_shifts.append(dict(shift_time_start=freeShift.shift_time_start, shift_time_end=freeShift.shift_time_end, role=freeShift.role, id=freeShift.id))
    freeTable = FreeTable(free_shifts)
    claim_shifts = []
    form2 = CheckForm()
    form2.user.choices={(u.name,u.name+' - '+u.role) for u in User.select()}.union({('', 'All Users')})
    form2.user.default=''
    if form2.validate_on_submit() and form2.submit.data:
        if form2.user.data=='':
            for claimShift in Shift.select().where((Shift.name!="")&(Shift.shift_time_end>current_time)):
                claim_shifts.append(dict(name=claimShift.name, shift_time_start=claimShift.shift_time_start, shift_time_end=claimShift.shift_time_end, role=claimShift.role, id=claimShift.id))
            selection='All Users'
            claimTable = ClaimTable(claim_shifts)
            flash("Notification: Shifts for selected user is displayed")
            return render_template('/shift_manager/index.html', logged_in=True, name=employee_name, role=employee_role, freeTable=freeTable, claimTable = claimTable, form=form, userShift=form2, selection=selection)
        else:
            for userShift in Shift.select().where((Shift.name==form2.user.data)&(Shift.shift_time_end>current_time)):
                claim_shifts.append(dict(shift_time_start=userShift.shift_time_start, shift_time_end=userShift.shift_time_end, role=userShift.role, id=userShift.id))
            selection=form2.user.data
            claimTable = UniqueTable(claim_shifts)
            flash("Notification: Shifts for selected user is displayed")
        return render_template('/shift_manager/index.html', logged_in=True, name=employee_name, role=employee_role, freeTable=freeTable, claimTable = claimTable, form=form, userShift=form2, selection=selection)
    else:
        for claimShift in Shift.select().where((Shift.name!="")&(Shift.shift_time_end>current_time)):
            claim_shifts.append(dict(name=claimShift.name, shift_time_start=claimShift.shift_time_start, shift_time_end=claimShift.shift_time_end, role=claimShift.role, id=claimShift.id))
        selection='All Users'
        claimTable = ClaimTable(claim_shifts)
    return render_template('/shift_manager/index.html', logged_in=True, name=employee_name, role=employee_role, freeTable=freeTable, claimTable = claimTable, form=form, userShift=form2, selection=selection)

@page.route('/data')
@require_role(['admin', 'chef', 'waiter', 'host', 'manager'])
def return_data():
    start_date = request.args.get('start', '')
    end_date = request.args.get('end', '')
    current_time = datetime.now()
    shift_json = [] 
    for s in Shift.select().where((Shift.shift_time_end<current_time)):
        if  s.name!="":
            shift_json.append(dict(title=s.name+'-'+s.role,start=str(s.shift_time_start),end=str(s.shift_time_end), backgroundColor='#85929E'))
    for s in Shift.select().where((Shift.name=="") & (Shift.shift_time_end > current_time)):
        shift_json.append(dict(title=s.role,start=str(s.shift_time_start),end=str(s.shift_time_end), backgroundColor='#66ff66'))
    for s in Shift.select().where((Shift.name!="") & (Shift.shift_time_end > current_time)):
        shift_json.append(dict(title=s.name+' - '+s.role,start=str(s.shift_time_start),end=str(s.shift_time_end), backgroundColor='#3399ff'))
    # print(shsift_json)
    return json.dumps(shift_json)

@page.route("/claim", methods=['GET', 'POST'])
@require_role(['admin', 'chef', 'waiter', 'host', 'manager'])
def claim():
    '''
    This handles when the user needs to claim a shift
    '''
    id = request.args.get('id')
    name = flask_login.current_user.name
    role = flask_login.current_user.role
    if shift_controller.checkAvailability(id, name, role):
        Shift.claim_shift(id, name)
        flash("Notification: Successfully claimed the shift")
        return redirect(url_for('shift_manager.calendar'))
    else:
        flash("Insufficient Privileges: Unable to claim the shift")
        return redirect(url_for('shift_manager.calendar'))

@page.route("/post", methods=['GET', 'POST'])
@require_role(['admin', 'chef', 'waiter', 'host', 'manager'])
def post():
    '''
    This handles when the user needs to post a shift
    '''
    id = request.args.get('id')
    name = flask_login.current_user.name
    role = flask_login.current_user.role
    if shift_controller.checkPostConditions(id, name, role):
        Shift.post_shift(id)
        flash("Notification: Successfully posted the shift")
        return redirect(url_for('shift_manager.calendar'))
    else:
        flash("Insufficient Privileges: Unable to post the shift")
        return redirect(url_for('shift_manager.calendar'))

@page.route("/remove", methods=['GET', 'POST'])
def remove():
    '''
    This handles when the user needs to remove a shift
    '''
    id = request.args.get('id')
    role = flask_login.current_user.role
    if shift_controller.checkRemoveConditions(id, role):
        Shift.remove_shift(id)
        flash("Successfully removed the shift")
    else:
        flash("Unable to remove shift")
    return redirect(url_for('shift_manager.calendar'))
