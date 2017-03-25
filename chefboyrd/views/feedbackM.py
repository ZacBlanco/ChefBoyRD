from flask import Blueprint, render_template, abort, url_for, redirect

page = Blueprint('feedbackM', __name__, template_folder='./templates')

@page.route("/",methods=['GET', 'POST'])
@require_role('admin')
def feedback_table():

	if customer_controller.new_customer(name):
        return render_template('default.html', users=[name])
    else:
        return render_template('default.html', users=['Failed'])


@page