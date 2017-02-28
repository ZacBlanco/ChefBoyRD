'''Statistics dashboard for the manager interface


Will be able to render dashboards which include statistics from the database
of the Point of sale system and other data systems for the business.
'''
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from flask_login import login_required

page = Blueprint('dashboard', __name__, template_folder='templates')

@page.route("/")
@login_required
def dash_index():
    '''Renders the index page of the dashboards
    '''
    render_template('dashboard/index.html')
