from flask import Blueprint, render_template,redirect,url_for,flash,request
from flask_login import logout_user,login_required, current_user
from flask.views import MethodView

from models.music_model import Song, FlaggedContent
from models.user_model import User, FlaggedCreator

from decorators.contents import admin_stats, user_contents, user_stats
from decorators.role_decorator import user_required, creator_required, admin_required

from extensions.extension import db
import requests
'''
+--------------------------------------------------------------+
|                         blueprint user                       |
+--------------------------------------------------------------+
'''
bp_user = Blueprint('user', __name__)

#------------------------------------dashboard----------------------------#
class DashboardView(MethodView):
    @login_required
    def get(self):
        # contents
        suggested_songs, playlists, albums = user_contents()

        # stats
        stats_data = admin_stats()

        # flagged_content
        flagged_contents = FlaggedContent.query.all()
        reasons = list()
        flagged_songs = list()

        for content in flagged_contents:
            flagged_song = Song.query.filter_by(id=content.song_id, creator_id=current_user.id).first()
            if flagged_song:
                reasons.append(content.reason)
                flagged_songs.append(flagged_song)

        # check if current user is in the flagged creators
        flagged_creator = FlaggedCreator.query.filter_by(user_id=current_user.id).first()
        if flagged_creator:
            is_flagged_creator = True
        else:
            is_flagged_creator = False

        return render_template('dashboard.html', playlists=playlists, suggested_songs=suggested_songs, albums=albums, stats_data=stats_data, flagged_songs=flagged_songs, reasons=reasons, is_flagged_creator=is_flagged_creator)
bp_user.add_url_rule('/dashboard', view_func=DashboardView.as_view('dashboard'))

#------------------------------------logout----------------------------#
class LogoutView(MethodView):
    @login_required
    def get(self):
        logout_user()
        flash('logged out!', 'success')

        return redirect(url_for('index.home'))
bp_user.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))

#------------------------------------creator_register----------------------------#
class CreatorRegisterView(MethodView):
    @user_required
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

#------------------------------------creator_stats----------------------------#
class CreatorStatsView(MethodView):
    @creator_required
    def get(self):
        #contents
        suggested_songs, playlists, albums = user_contents()

        # stats
        stats_data = user_stats()

        return render_template('creator_stats.html', playlists=playlists, suggested_songs=suggested_songs, albums=albums, stats_data=stats_data)
bp_user.add_url_rule('/creator_stats', view_func=CreatorStatsView.as_view('creator_stats'))

#------------------------------------all_creators----------------------------#
class AllCreatorsView(MethodView):
    @admin_required
    def get(self):
        creators = User.query.filter_by(role='creator').all()
        is_flagged = list()
        for creator in creators:
            flagged_creator = FlaggedCreator.query.filter_by(user_id=creator.id).first()
            if flagged_creator:
                is_flagged.append(True)
            else:
                is_flagged.append(False)
        # stats
        stats_data = admin_stats()

        return render_template('creators.html', creators=creators,is_flagged=is_flagged ,stats_data=stats_data)
bp_user.add_url_rule('/all_creators', view_func=AllCreatorsView.as_view('all_creators'))

#------------------------------------flag_creator----------------------------#
class FlagCreatorView(MethodView):
    @admin_required
    def get(self, creator_id, admin_id):
        flagged_creator = FlaggedCreator(user_id=creator_id, admin_id=admin_id)
        db.session.add(flagged_creator)
        db.session.commit()

        flash('Creator blacklisted successfully!', 'success')
        return redirect(url_for('user.all_creators'))
bp_user.add_url_rule('/flag_creator/<string:creator_id>/<string:admin_id>', view_func=FlagCreatorView.as_view('flag_creator'))

#------------------------------------unflag_creator----------------------------#
class UnflagCreatorView(MethodView):
    @admin_required
    def get(self, creator_id):
        flagged_creator = FlaggedCreator.query.filter_by(user_id=creator_id).first()
        db.session.delete(flagged_creator)
        db.session.commit()

        flash('Creator whitelisted successfully!', 'success')

        return redirect(url_for('user.all_creators'))
bp_user.add_url_rule('/unflag_creator/<string:creator_id>', view_func=UnflagCreatorView.as_view('unflag_creator'))