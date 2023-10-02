# imports
from sqlite3 import IntegrityError
from flask import Blueprint, render_template, redirect, url_for, flash
from flask.views import MethodView

from models.user_model import User, Admin
from forms.auth_form import RegisterForm, LoginForm

from flask_login import login_user, login_required, logout_user

from extensions.extension import db, bcrypt


#------------------------------------blueprint_auth---------------------------------------#
bp_auth = Blueprint('auth', __name__)

# view register
class RegisterView(MethodView):
    
    def get(self):
        form = RegisterForm()
        return render_template('register.html', form=form)
    
    def post(self):
        form = RegisterForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)

            try:
                db.session.add(user)
                db.session.commit()
                flash('Account created! Please login', 'success')
                return redirect(url_for('auth.user_login'))
            except IntegrityError:
                flash('That email is already in use. Please choose a different one.', 'danger')
        return redirect(url_for('auth.register'))
bp_auth.add_url_rule('/register', view_func=RegisterView.as_view('register'))

# view user_login
class UserLoginView(MethodView):
    def get(self):
        form = LoginForm()
        return render_template('user_login.html', form=form)
    
    def post(self):
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                
                login_user(user)
                return redirect(url_for('user.dashboard'))
            else:
                flash('Invalid_credentials!', 'danger')

        return redirect(url_for('auth.user_login'))  
bp_auth.add_url_rule('/user_login', view_func=UserLoginView.as_view('user_login'))


# view admin_login
class AdminLoginView(MethodView):
    def get(self):
        form = LoginForm()
        return render_template('admin_login.html', form=form)
    
    def post(self):
        form = LoginForm()
        if form.validate_on_submit():
            admin = Admin.query.filter_by(email=form.email.data).first()
            if admin and bcrypt.check_password_hash(admin.password, form.password.data):
                login_user(admin)
                return redirect(url_for('user.dashboard'))
            else:
                flash('Invalid_credentials!', 'danger')

        return redirect(url_for('auth.admin_login'))   
bp_auth.add_url_rule('/admin_login', view_func=AdminLoginView.as_view('admin_login'))

