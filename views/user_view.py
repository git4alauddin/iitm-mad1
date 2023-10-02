from flask import Blueprint, render_template,redirect,url_for,flash,request
from flask_login import logout_user,login_required
from flask.views import MethodView

#------------------------------------blueprint_user---------------------------------------#
bp_user = Blueprint('user', __name__)

# view dashboard
class DashboardView(MethodView):
    @login_required
    def get(self):
        return render_template('dashboard.html')
bp_user.add_url_rule('/dashboard', view_func=DashboardView.as_view('dashboard'))

# view logout
class LogoutView(MethodView):
    def get(self):
        logout_user()
        flash('logged out!', 'success')
        return redirect(url_for('index.home'))
bp_user.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))