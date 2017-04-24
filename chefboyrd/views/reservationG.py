'''Reservation dashboard for the manager interface
'''
from flask import Blueprint, render_template, abort, url_for, redirect, flash
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

page = Blueprint('reservationG', __name__, template_folder='./templates')

class ReservationForm(FlaskForm):
    '''
    This is the form that displays fields to make a reservation
    '''
    name = StringField('Name', [validators.Length(min=2, max=25)])
    num = IntegerField('Guests',[validators.NumberRange(min=1, max=None)])
    # phone = StringField('Phone Number', [validators.Length(min=10, max=10)])
    phone = PhoneNumberField('Phone Number',[validators.DataRequired()])
    length = IntegerField('Reservation Length(Minutes)',[validators.NumberRange(min=30, max=None)])
    start = DateTimeField('Time and Date')

@page.route("/",methods=['GET', 'POST'])
def resG_index():
    '''
    Renders the index page of the reservation page
    '''
    form = ReservationForm()
    if form.validate_on_submit():
        error = booking_controller.book_restaurant_table(1, form.start.data,form.num.data,form.name.data, form.phone.data, form.length.data)
        if(type(error) == str):
            flash(error)
        else:
            flash("Table successfully reserved!")

    # Logged in always true because we require admin role
    return render_template('/reservationG/index.html',logged_in=False,form=form)