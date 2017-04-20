'''Reservation dashboard for the manager interface
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

page = Blueprint('reservationH', __name__, template_folder='./templates')

class ReservationForm(FlaskForm):
    '''
    This is the form that displays fields to make a reservation
    '''
    name = StringField('Name', [validators.Length(min=2, max=25)])
    num = IntegerField('Guests')
    # phone = StringField('Phone Number', [validators.Length(min=10, max=10)])
    phone = PhoneNumberField('Phone Number')
    start = DateTimeField('Time and Date')

# Declare your table
class ItemTable(Table):
    '''
    This is a itemTable class that generates text/html automatically to create a table for created reservations
    '''
    html_attrs = {'class': 'table table-striped'}
    name = Col('Name')
    guests = Col('Guests')
    phone = Col('Phone')
    time = Col('Starting Time')
    table = Col('Table')
    cancel = ButtonCol('Cancel','reservationH.cancel',url_kwargs=dict(id='id'),button_attrs={'class': 'btn btn-danger'})

@page.route("/",methods=['GET', 'POST'])
@require_role(['admin','host'],getrole=True) # Example of requireing a role(and authentication)
def resH_index(role):
    '''
    Renders the index page of the reservation page
    '''
    form = ReservationForm()
    if form.validate_on_submit():
        table = booking_controller.book_restaurant_table(1, form.start.data,form.num.data,form.name.data, form.phone.data)
        # reservation.Reservation.create_reservation(form.name.data,form.num.data,form.phone.data,form.start.data)
    # Populate the table

    res = []
    for person in tables.Booking.select():
        res.append(dict(name=person.name,guests=person.people,phone=person.phone,time=person.booking_date_time_start.strftime("%Y-%m-%d %H:%M"),table=person.table.id,id=person.id))
    table = ItemTable(res)
        #person.start.strftime("%Y-%m-%d %H:%M")
    # Logged in always true because we require admin role
    return render_template('/reservationH/index.html', res=res,logged_in=True,table=table,form=form,role=role)

@page.route("/cancel",methods=['GET', 'POST'])
@require_role(['admin','host']) # Example of requireing a role(and authentication)
def cancel():
    '''
    This handles when a user needs to cancel a reservation. 
    '''
    id = request.args.get('id')
    tables.Booking.cancel_reservation(id)
    # reservation.Reservation.create_reservation(form.name.data,form.num.data,form.phone.data,form.start.data)
    return redirect(url_for('reservationH.resH_index'))