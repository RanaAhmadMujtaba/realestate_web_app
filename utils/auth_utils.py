from flask import session
from werkzeug.security import check_password_hash
from functools import wraps
from flask import redirect, flash

def validate_login(username, password, users):
    for user in users:
        if user['username'] == username and check_password_hash(user['password'], password):
            return user
    return None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash("Login required.")
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

def is_admin():
    return session.get('role') == 'admin'

def is_viewer():
    return session.get('role') == 'viewer'
