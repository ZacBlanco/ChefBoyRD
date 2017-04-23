from wtforms import TextAreaField, SubmitField, DecimalField
from flask_wtf import FlaskForm
from flask import Blueprint, render_template, abort, url_for, redirect, request
from jinja2 import TemplateNotFound
from chefboyrd.auth import require_role
from chefboyrd.controllers import feedback_controller
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

page = Blueprint('feedbackC', __name__, template_folder='./templates')

class CommentForm(FlaskForm):
    """WTforms object for the feedback form submission"""

    food_rating = DecimalField()
    service_rating = DecimalField()
    clean_rating = DecimalField()
    ambience_rating = DecimalField()
    overall_rating = DecimalField()

    comment_field = TextAreaField()

    submit_field = SubmitField("submit")

@page.route("/",methods=['GET', 'POST'])
@require_role(['notanadmin','admin'],getrole=True)
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
        if (request.form['submit_field'] == 'Back'):
            return render_template('feedbackC/index.html', logged_in=True,role=role)

        rating = {'food':food_rating,
                    'service':service_rating,
                    'clean':clean_rating,
                    'ambience':ambience_rating,
                    'overall':overall_rating,
                    'comment':comment_field}
        update_db_rating(rating)
        if (request.form['comment_field']):
            comment = request.form['comment_field']
            return render_template('feedbackC/confirmation.html', logged_in=True, comment=comment,role=role)
        else:
            return render_template('feedbackC/index.html', logged_in=True,role=role)
    else:
        return render_template('feedbackC/index.html', logged_in=True,role=role)