"""Contains methods that render the interface for customers to submit in-store ratings

written by: Seo Bo Shim, Jarod Morin
tested by: Seo Bo Shim
debugged by: Seo Bo Shim
"""

from wtforms import TextAreaField, SubmitField, DecimalField
from flask_wtf import FlaskForm
from flask import Blueprint, render_template, abort, url_for, redirect, request, flash
from jinja2 import TemplateNotFound
from chefboyrd.auth import require_role
from chefboyrd.controllers import feedback_controller
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

page = Blueprint('feedbackC', __name__, template_folder='./templates')

class CommentForm(FlaskForm):
    """WTforms object for the feedback form submission
    """

    food_rating = DecimalField()
    service_rating = DecimalField()
    clean_rating = DecimalField()
    ambience_rating = DecimalField()
    overall_rating = DecimalField()
    submit = SubmitField("submit")

@page.route("/",methods=['GET', 'POST'])
@require_role(['notanadmin','admin'],getrole=True)
def feedback_submit(role):
    """By default displays a webpage text box for user to submit customer feedback.
    Displays a confirmation message when submitted

    Returns:
        The template to display with the appropriate parameters
    form: form that specifies the query instructions.
    """
    #get all of the feedback objects and insert it into table
    form = CommentForm()

    if (request.method == 'POST'):
        rating = {'food':form.food_rating.data,
                    'service':form.service_rating.data,
                    'clean':form.clean_rating.data,
                    'ambience':form.ambience_rating.data,
                    'overall':form.overall_rating.data}
        feedback_controller.update_db_rating(rating)
        flash("Thank you for your feedback!")
        return render_template('feedbackC/index.html', logged_in=True,role=role)
    else:
        return render_template('feedbackC/index.html', logged_in=True,role=role)