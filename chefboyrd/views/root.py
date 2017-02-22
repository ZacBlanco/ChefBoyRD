'''The homepage'''
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

page = Blueprint('main', __name__, template_folder='templates')

users = ["zac", 'jarod', 'richard', 'seobo', 'ben', 'jeffrey']

@page.route('/')
def show():
    '''Render Homepage'''
    try:
        return render_template('default.html', users=users)
    except TemplateNotFound:
        abort(404)

@page.route('/hello')
def showhello():
    return "Hi"
