'''Module for authentication
'''
from functools import wraps
import flask
from flask import Blueprint, render_template, url_for, redirect
import flask_login
from chefboyrd import LM as login_manager
from chefboyrd.models import User
from werkzeug.security import check_password_hash

auth_pages = Blueprint('auth_pages', __name__, template_folder="./views/templates")

@login_manager.user_loader
def user_loader(email):
    '''Loads the user via a DB call'''
    users = User.select().where(User.email == email)
    if len(users) > 0:
        return users[0]
    else:
        return

@login_manager.unauthorized_handler
def unauth():
    '''Function to handle requests to resources that are not authorized or authenticated.'''
    return render_template('unauthorized.html'), 401

def require_login(func):
    '''Wrapper around the login_required wrapper from flask-login

        This allows us to keep the same style and also not have to have multiple imports for
        roles and require_login
    '''
    @wraps(func)
    @flask_login.login_required
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper

def require_role(role):
    '''Decorate a function with this in order to require a specific role to access a view.

    By decorating a function with @require_role you are implicity forcing @login_required as well.
    Example:

            @APP.route('/admin-dashboard')
            @require_role('admin')
            def view_dash():
                ...

    If a user is not authorized then the flask_login.unauthorized handler is called.
    '''
    def real_wrap(func):
        @wraps(func)
        @flask_login.login_required
        def wrapper(*args, **kwargs):
            user = flask_login.current_user
            if user.role == role:
                return func(*args, **kwargs)
            else:
                return login_manager.unauthorized()
        return wrapper
    return real_wrap

@auth_pages.route('/login', methods=['GET', 'POST'])
def login():
    '''Function which logs a user into the application'''

    if flask_login.current_user.is_authenticated:
        return redirect(url_for('index'))

    if flask.request.method == 'GET':
        return render_template('login.html')

    email = flask.request.form['email']
    users = User.select().where(User.email == email)

    if len(users) <= 0:
        return render_template('login.html', error='Unable to login user {}'.format(email))
    else:
        user = users[0]

    if check_password_hash(user.password, flask.request.form['pw']):
        user.id = user.email
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('index'))

    # Last resort - just return an error about logging in
    return render_template('login.html', error='Unable to login user {}'.format(email)), 401

@auth_pages.route('/logout')
def logout():
    ''''Logs a user out and renders the login template with a message'''
    flask_login.logout_user()
    return render_template('login.html', error="Successfully logged out")