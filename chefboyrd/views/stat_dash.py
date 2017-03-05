'''Statistics dashboard for the manager interface


Will be able to render dashboards which include statistics from the database
of the Point of sale system and other data systems for the business.
'''
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from chefboyrd.auth import require_role

page = Blueprint('dashboard', __name__, template_folder='./templates')

@page.route("/")
@require_role('admin') # Example of requireing a role(and authentication)
def dash_index():
    '''Renders the index page of the dashboards
    '''
    # Logged in always true because we require admin role
    return render_template('/dashboard/index.html', logged_in=True)
