from flask import Blueprint, render_template
from flask.views import MethodView
from flask import request
import requests
from forms.auth_form import RegisterForm

#-----------------------------blueprint_index-------------------------------#
bp_index = Blueprint('index', __name__)                       


# view home
class HomeView(MethodView):
    def get(self):
        form = RegisterForm()
        return render_template('home.html', form=form)
bp_index.add_url_rule('/home', view_func=HomeView.as_view('home'))