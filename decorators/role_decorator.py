from functools import wraps
from flask import flash, url_for, redirect
from flask_login import current_user, login_required

# user
def user_required(func):
    @wraps(func)
    @login_required
    def decoreated_view(*args, **kwargs):
        if current_user.is_authenticated and current_user.role == 'user':
            return func(*args, **kwargs)
        else:
            flash('Sorry! Access denied', 'danger')
            return redirect(url_for('user.dashboard'))
    return decoreated_view

# creator
def creator_required(func):
    @wraps(func)
    @login_required
    def decoreated_view(*args, **kwargs):
        if current_user.is_authenticated and current_user.role == 'creator':
            return func(*args, **kwargs)
        else:
            flash('Sorry! Access denied', 'danger')
            return redirect(url_for('user.dashboard'))
    return decoreated_view

# admin
def admin_required(func):
    @wraps(func)
    @login_required
    def decoreated_view(*args, **kwargs):
        if current_user.is_authenticated and current_user.role == 'admin':
            return func(*args, **kwargs)
        else:
            flash('Sorry! Access denied', 'danger')
            return redirect(url_for('user.dashboard'))
    return decoreated_view

# admin or creator
def admin_or_creator_required(func):
    @wraps(func)
    @login_required
    def decorated_view(*args, **kwargs):
        if current_user.is_authenticated and (current_user.role == 'admin' or current_user.role == 'creator'):
            return func(*args, **kwargs)
        else:
            flash('Sorry! Access denied', 'danger')
            return redirect(url_for('user.dashboard'))
    return decorated_view