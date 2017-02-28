'''Module for authentication
'''
import flask
from flask import render_template, url_for, redirect
import flask_login
from chefboyrd import LM as login_manager
from chefboyrd.models.user import User
from chefboyrd import APP
from werkzeug.security import check_password_hash


@login_manager.user_loader
def user_loader(email):
    users = User.select().where(User.email == email)
    if len(users) == 1:
        return users[0]
    else:
        return

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    users = User.select().where(User.email == email)
    if len(users) == 0:
        return
    user = users[0]

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = check_password_hash(user.password, request.form['pw'])

    return user

# def role_required(r):
#     @wraps(r)
#     return

@APP.route('/login', methods=['GET', 'POST'])
def login():

    if flask_login.current_user.is_authenticated:
        return redirect(url_for('protected'))

    if flask.request.method == 'GET':
        return render_template('login.html')

    email = flask.request.form['email']
    users = User.select().where(User.email == email)
    if len(users) == 0:
        return render_template('login.html', error='Unable to login user {}'.format(email))
    else:
        user = users[0]
    if check_password_hash(user.password, flask.request.form['pw']):
        user = User()
        user.id = email
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('protected'))

    return 'Bad login'

@APP.route('/logout')
def logout():
    ''''Logs a user out and renders the default template'''
    flask_login.logout_user()
    return render_template('default.html')

@APP.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: {}'.format(flask_login.current_user.email)