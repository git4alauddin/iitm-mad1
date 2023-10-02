from flask import Blueprint, render_template
from flask.views import MethodView

#------------------------blueprint_index----------------------------#
bp_index = Blueprint('index', __name__)                       


# view home
class HomeView(MethodView):
    def get(self):
        return render_template('home.html')
bp_index.add_url_rule('/home', view_func=HomeView.as_view('home'))