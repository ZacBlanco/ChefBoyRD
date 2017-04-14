'''Table dashboard for the manager interface
TO DO: Limit reservation times to after date,limit guests based on table(going to be hard)
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
    '''
    This itemTable class generates a table of the created reservations. It also has buttons to cancel or confirm a reservation
    '''
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
    '''Renders the index page of the table management page
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
    '''
    This handles when a user needs to cancel a reservation. 
    '''
    id = int(request.args.get('id'))
    tables.Booking.cancel_reservation(id)
    # reservation.Reservation.create_reservation(form.name.data,form.num.data,form.phone.data,form.start.data)
    return redirect(url_for('table_manager.table_manager_index'))

@page.route("/confirm",methods=['GET', 'POST'])
@require_role('admin') # Example of requireing a role(and authentication)
def confirm():
    '''
    This handles when a user needs to confirm a reservation. 
    '''
    id = int(request.args.get('id'))
    id2 = 0
    for ids in tables.Booking.select().where(tables.Booking.id == id):
        id2 = int(ids.table.id)
        break
    query = tables.Table.update(occupied=1).where(tables.Table.id==id2)
    query.execute()
    tables.Booking.cancel_reservation(id)
    # reservation.Reservation.create_reservation(form.name.data,form.num.data,form.phone.data,form.start.data)
    return redirect(url_for('table_manager.table_manager_index'))

@page.route("/change_table",methods=['GET', 'POST'])
@require_role('admin') # Example of requireing a role(and authentication)
def change_table():
    '''
    This handles when a user needs to change the status of a table. 
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
    '''
    This handles when we need to change the position of a table.
    '''
    coords = []
    for table in tables.Table.select():
        coords.append([table.posX,table.posY, table.occupied,table.id, table.size])
    return json.dumps(coords)

@page.route("/add_table",methods=['GET', 'POST'])
@require_role('admin') # Example of requireing a role(and authentication)
def add_table():
    '''
    This handles when a user adds a table to the layout.
    '''
    table_size = int(request.form['table_size'])
    id = tables.Table.create_tables(1,table_size, 0,0.5, 0.5)
    return json.dumps(id)

@page.route("/del_table",methods=['GET', 'POST'])
@require_role('admin') # Example of requireing a role(and authentication)
def del_table():
    '''
    This handles when a user adds a table to the layout.
    '''
    id = int(request.form['id'])
    id = tables.Table.delTable(id)
    return json.dumps(id)
