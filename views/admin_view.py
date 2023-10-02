from flask import Blueprint, render_template,redirect,url_for,flash,request
from flask.views import MethodView
import requests

bp_admin = Blueprint('admin', __name__)

class Users(MethodView):
    def get(self):
        # set the method, ip, and port for the api
        # now it is default to localhost:5000
        api_url = request.url_root + 'users/users'
        response = requests.get(api_url)

        if response.status_code == 200:
            users = response.json()
            return render_template('users.html', users=users)
        else:
            flash('Failed to fetch users', 'danger')
            return redirect(url_for('user.dashboard'))
bp_admin.add_url_rule('/users', view_func=Users.as_view('users'))