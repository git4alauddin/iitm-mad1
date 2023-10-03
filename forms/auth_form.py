# imports
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField, PasswordField, EmailField
from wtforms.validators import input_required, Length, ValidationError, Email
from models.user_model import User

# form register
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[input_required(), Length(min=4, max=20)], render_kw={'placeholder': 'Username', 'class': 'form-control'})
    email = EmailField('Email', validators=[input_required(), Email()], render_kw={'placeholder': 'Email', 'class': 'form-control'})
    password = PasswordField('Password', validators=[input_required(), Length(min=4, max=20)], render_kw={'placeholder': 'Password', 'class': 'form-control'})
    submit = SubmitField('Register')  
    
# form login
class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[input_required(), Email()], render_kw={'placeholder': 'Email'})
    password = PasswordField('Password', validators=[input_required(), Length(min=4, max=20)], render_kw={'placeholder': 'Password'})
    submit = SubmitField('Login')