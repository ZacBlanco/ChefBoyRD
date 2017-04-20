from wtforms import TextAreaField, SubmitField
from flask_wtf import FlaskForm
from flask import Blueprint, render_template, abort, url_for, redirect, request
from jinja2 import TemplateNotFound
from chefboyrd.auth import require_role

page = Blueprint('feedbackC', __name__, template_folder='./templates')

class CommentForm(FlaskForm):
    """WTforms object for the feedback form submission"""
    comment_field = TextAreaField()
    submit_field = SubmitField("Submit")

@page.route("/",methods=['GET', 'POST'])
@require_role('notanadmin',getrole=True)
def feedback_submit(role):
    """
    By default displays a webpage text box for user to submit customer feedback.
    Redirects to

    Returns:
        The template to display with the appropriate parameters
    form: form that specifies the query instructions.
    """
    #get all of the feedback objects and insert it into table
    form = CommentForm()
    if (request.method== 'POST'):
        if (request.form.__contains__('comment_field')):
            #put the data in DB
            comment = request.form['comment_field']
            return render_template('feedbackC/confirmation.html', logged_in=True, comment=comment,role=role)
        else:
            return render_template('feedbackC/index.html', logged_in=True,role=role)
    else:
        return render_template('feedbackC/index.html', logged_in=True,role=role)