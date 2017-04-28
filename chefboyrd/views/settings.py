"""This view is for displaying the settings page. Users with admin role can add and remove users

written by: Seo Bo Shim
tested by: Seo Bo Shim
debugged by: Seo Bo Shim
"""
from wtforms import TextAreaField, SubmitField
from flask import Blueprint, render_template, abort, url_for, redirect, request
from jinja2 import TemplateNotFound
from chefboyrd.auth import require_role
from flask_wtf import FlaskForm
from flask_table import Table, Col, create_table, ButtonCol
from chefboyrd.models import User


page = Blueprint('settings', __name__, template_folder='./templates') #If page blueprint changes, must change form action directory

class UserTable(Table):
    """FlaskTable object for organizing feedback info into a table
    """
    email = Col('Email', column_html_attrs={'class': 'spaced-table-col'},)
    name = Col('Name', column_html_attrs={'class': 'spaced-table-col'},)
    role = Col('Role', column_html_attrs={'class': 'spaced-table-col'},)
    delete = ButtonCol('Remove', '.remove_user', url_kwargs=dict(email_='email', role_='role'), column_html_attrs={'class': 'spaced-table-col'})

class AddUserForm(FlaskForm):
    """WTforms object for the Add-User form
    """
    email = TextAreaField('email')
    password = TextAreaField('password')
    re_password = TextAreaField('password')
    name = TextAreaField('name')
    role = TextAreaField('role')

@page.route("/",methods=['GET', 'POST'])
@page.route("/add_user",methods=['GET'])
@page.route("/remove_user",methods=['GET'])
@require_role('admin',getrole=True)
def settings_display(role):
    """Default page for the ChefBoyRD settings

    Returns:
        Template that displays the necessary items in the settings page.
    table(FlaskTable object): formatted table to display in index.
    table_label(str): label for the displayed table
    main(bool): Condition to display the add-user form. Confirmation pages accessed with POST methods have main=False
    """

    #add other settings here and alter the render_template parameters as necessary

    table = _display_users()
    if (table):
        return render_template('settings/index.html', logged_in=True, table=table, table_label="Current Users", main=True, role=role)
    else:
        return render_template('settings/index.html', logged_in=True, main=True,role=role)


@page.route("/add_user",methods=['POST'])
@require_role('admin',getrole=True)
def add_user(role):
    """Processes form submission for adding user to database

    Returns:
        Template with an error or a confirmation page with the added user
    table(FlaskTable object): formatted table to display in index.
    table_label(str): label for the displayed table
    main(bool): Condition to display the add-user form. Confirmation pages accessed with POST methods have main=False
    """
    form = AddUserForm()
    if request.form.get('password') == request.form.get('re_password'):
        try:
            User.create_user(email=request.form.get('email'), password=request.form.get('password'),name=request.form.get('name'),role=request.form.get('role'))
        except ValueError:
            error = 'User already exists'
            return render_template('settings/index.html', logged_in=True, error=error, main=True, role=role)
    else:
        error = 'Passwords did not match.'
        return render_template('settings/index.html', logged_in=True, error=error, main=True,role=role)

    res = User.select().where((request.form.get('email') == User.email))
    table = UserTable(res)
    if table:
        return render_template('settings/index.html', logged_in=True, table=table, table_label="Added User", main=False,role=role)
    else:
        error = 'Internal Error. User could not be created'
        return render_template('settings/index.html', logged_in=True, error=error, main=False,role=role)

@page.route("/remove_user",methods=['POST'])
@require_role('admin')
def remove_user():
    """Processes form submission for removing user from database
    
    Returns:
        redirect to main Settings page
    """
    if (request.args.get('role_',type=str) == 'admin'):
        #require authentification.
        pass
    expr = (User.email == request.args.get('email_',type=str) )
    User.delete().where(expr).execute()
    return redirect(url_for('.settings_display'))
    

def _display_users():
    """Helper function for displaying table of Users in DB
    Returns:
        table(Table object) if successful. 0 if no users could be found

    """
    try:
        res = User.select().order_by(-User.role)
        table = UserTable(res)
        return table
    except:
        return 0