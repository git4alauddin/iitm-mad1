from flask import Blueprint, render_template
from flask.views import MethodView
from flask import request
import requests

#------------------------blueprint_index----------------------------#
bp_index = Blueprint('index', __name__)                       


# view home
class HomeView(MethodView):
    def get(self):
        # contents
        api_url = request.url_root + 'songs/songs'
        s_response = requests.get(api_url)
        if s_response.status_code == 200:
            suggested_songs = s_response.json()
        return render_template('home.html', suggested_songs=suggested_songs)
bp_index.add_url_rule('/home', view_func=HomeView.as_view('home'))