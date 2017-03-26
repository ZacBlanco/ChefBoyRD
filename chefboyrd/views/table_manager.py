'''Statistics dashboard for the manager interface
TO DO: Limit reservation times to after date,limit guests based on table(going to be hard)

Will be able to render dashboards which include statistics from the database
of the Point of sale system and other data systems for the business.
'''
from flask import Blueprint, render_template, abort, url_for, redirect
from jinja2 import TemplateNotFound
from chefboyrd.auth import require_role
from chefboyrd.controllers import booking_controller
from peewee import *
from chefboyrd.models import customers, user, reservation, tables
from flask_wtf import FlaskForm, CsrfProtect
from wtforms import BooleanField, StringField, PasswordField, validators, IntegerField
from wtforms.ext.dateutil.fields import DateTimeField
from wtforms_alchemy import PhoneNumberField
from datetime import datetime
from flask_table import Table, Col, ButtonCol
from flask import request
import json

page = Blueprint('table_manager', __name__, template_folder='./templates')

# Declare your table
class ItemTable(Table):
    html_attrs = {'class': 'table table-striped'}
    name = Col('Name')
    guests = Col('Guests')
    phone = Col('Phone')
    time = Col('Starting Time')
    table = Col('Table')
    confirm = ButtonCol('Confirm','table_manager.confirm',url_kwargs=dict(id='id'),button_attrs={'class': 'btn btn-success'})
    cancel = ButtonCol('Cancel','table_manager.cancel',url_kwargs=dict(id='id'),button_attrs={'class': 'btn btn-danger'})


@page.route("/",methods=['GET', 'POST'])
@require_role('admin') # Example of requireing a role(and authentication)
def table_manager_index():
    '''Renders the index page of the dashboards
    '''
    # Populate the table

    res = []
    for person in tables.Booking.select():
        res.append(dict(name=person.name,guests=person.people,phone=person.phone,time=person.booking_date_time_start.strftime("%Y-%m-%d %H:%M"),table=person.table.id,id=person.id))
    table = ItemTable(res)
        #person.start.strftime("%Y-%m-%d %H:%M")
    # Logged in always true because we require admin role
    return render_template('/table_manager/index.html', res=res,logged_in=True,table=table,tables=tables)

@page.route("/cancel",methods=['GET', 'POST'])
@require_role('admin') # Example of requireing a role(and authentication)
def cancel():
    '''Renders the index page of the dashboards
    '''
    id = int(request.args.get('id'))
    tables.Booking.cancel_reservation(id)
    # reservation.Reservation.create_reservation(form.name.data,form.num.data,form.phone.data,form.start.data)
    return redirect(url_for('table_manager.table_manager_index'))

@page.route("/confirm",methods=['GET', 'POST'])
@require_role('admin') # Example of requireing a role(and authentication)
def confirm():
    '''Renders the index page of the dashboards
    '''
    id = int(request.args.get('id'))
    for ids in tables.Booking.select().where(tables.Booking.id == id):
        id = int(ids.table.id)
        break
    query = tables.Table.update(occupied=1).where(tables.Table.id==id)
    query.execute()
    tables.Booking.cancel_reservation(id)
    # reservation.Reservation.create_reservation(form.name.data,form.num.data,form.phone.data,form.start.data)
    return redirect(url_for('table_manager.table_manager_index'))

@page.route("/change_table",methods=['GET', 'POST'])
@require_role('admin') # Example of requireing a role(and authentication)
def change_table():
    '''Renders the index page of the dashboards
    '''
    id = int(request.form['id'])
    type = int(request.form['type'])
    if type == 0:
        posX = float(request.form['posX'])
        posY = float(request.form['posY'])
        query = tables.Table.update(posX=posX,posY=posY).where(tables.Table.id==id)
        query.execute() 
    else:
        occupied = int(request.form['occupied'])
        query = tables.Table.update(occupied=occupied).where(tables.Table.id==id)
        query.execute()
    return redirect(url_for('table_manager.table_manager_index'))

@page.route("/update_table",methods=['GET', 'POST'])
@require_role('admin') # Example of requireing a role(and authentication)
def update_table():
    '''Renders the index page of the dashboards
    '''
    coords = []
    for table in tables.Table.select():
        coords.append([table.posX,table.posY, table.occupied,table.id])
    return json.dumps(coords)

