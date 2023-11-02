from flask import Blueprint, render_template,redirect,url_for,flash,request
from flask_login import logout_user,login_required, current_user
from flask.views import MethodView
import requests
from models.music_model import Playlist

#------------------------------------blueprint_user---------------------------------------#
bp_user = Blueprint('user', __name__)

# view dashboard
class DashboardView(MethodView):
    @login_required
    def get(self):
        api_url = request.url_root + 'users/users/' + str(current_user.id) + '/playlists'
        p_response = requests.get(api_url)
        api_url = request.url_root + 'songs/songs'
        s_response = requests.get(api_url)
        if s_response.status_code == 200:
            suggested_songs = s_response.json()
        if p_response.status_code == 200:
            playlists = p_response.json()
        return render_template('dashboard.html', playlists=playlists, suggested_songs=suggested_songs)
bp_user.add_url_rule('/dashboard', view_func=DashboardView.as_view('dashboard'))

# view logout
class LogoutView(MethodView):
    def get(self):
        logout_user()
        flash('logged out!', 'success')
        return redirect(url_for('index.home'))
bp_user.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))

# view register as creator
class CreatorRegisterView(MethodView):
    def get(self):
        api_url = request.url_root + 'users/users/' + str(current_user.id)
        response = requests.put(api_url, json={'id': current_user.id})

        if response.status_code == 201:
            flash('Successfully registered as creator!', 'success')
            return redirect(url_for('user.dashboard'))
        else:
            flash('Error registering as creator!', 'danger')
            return redirect(url_for('user.dashboard'))
bp_user.add_url_rule('/register/creator', view_func=CreatorRegisterView.as_view('creator_register'))