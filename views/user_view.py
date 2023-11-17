from flask import Blueprint, render_template,redirect,url_for,flash,request
from flask_login import logout_user,login_required, current_user
from flask.views import MethodView
import requests
from extensions.extension import db
from models.music_model import Playlist, Song, Album, FlaggedContent
from models.user_model import User, FlaggedCreator

#------------------------------------blueprint user---------------------------------------#
bp_user = Blueprint('user', __name__)

# view dashboard
class DashboardView(MethodView):
    @login_required
    def get(self):
        # contents
        api_url = request.url_root + 'users/users/' + str(current_user.id) + '/playlists'
        p_response = requests.get(api_url)
        api_url = request.url_root + 'songs/songs'
        s_response = requests.get(api_url)
        api_url = request.url_root + 'users/users/' + str(current_user.id) + '/albums'
        a_response = requests.get(api_url)
            
        if s_response.status_code == 200:
            suggested_songs = s_response.json()
        if p_response.status_code == 200:
            playlists = p_response.json()
        if a_response.status_code == 200:
            albums = a_response.json()

        # stats
        tot_user = User.query.filter_by(role='user').count()
        tot_creator = User.query.filter_by(role='creator').count()
        tot_album = Album.query.count()
        tot_song = Song.query.count()
        tot_playlist = Playlist.query.count()

        stats_headings = ['Total Normal Users', 'Total Creators', 'Total Albums', 'Total Songs', 'Total Playlists']
        stats_data = [{'heading': h, 'total': t} for h, t in zip(stats_headings, [tot_user, tot_creator, tot_album, tot_song, tot_playlist])]

        # flagged_content
        flagged_contents = FlaggedContent.query.all()
        reasons = list()
        flagged_songs = list()

        for content in flagged_contents:
            flagged_song = Song.query.filter_by(id=content.song_id, creator_id=current_user.id).first()
            if flagged_song:
                reasons.append(content.reason)
                flagged_songs.append(flagged_song)

        return render_template('dashboard.html', playlists=playlists, suggested_songs=suggested_songs, albums=albums, stats_data=stats_data, flagged_songs=flagged_songs, reasons=reasons)
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

# view creator_stats
class CreatorStatsView(MethodView):
    def get(self):
        #contents
        api_url = request.url_root + 'users/users/' + str(current_user.id) + '/playlists'
        p_response = requests.get(api_url)
        api_url = request.url_root + 'songs/songs'
        s_response = requests.get(api_url)
        api_url = request.url_root + 'users/users/' + str(current_user.id) + '/albums'
        a_response = requests.get(api_url)
        
        if s_response.status_code == 200:
            suggested_songs = s_response.json()
        if p_response.status_code == 200:
            playlists = p_response.json()
        if a_response.status_code == 200:
            albums = a_response.json()

        # stats
        stats_headings = ['Total Albums', 'Total Songs', 'Total Playlists', 'Average Rating']
        tot_song = Song.query.filter_by(creator_id=current_user.id).count()
        tot_album = Album.query.filter_by(user_id=current_user.id).count()
        tot_playlist = Playlist.query.filter_by(user_id=current_user.id).count()
        average_rating = 3.4

        stats_data = [{'heading': h, 'total': t} for h, t in zip(stats_headings, [tot_album, tot_song, tot_playlist, average_rating])]

        return render_template('creator_stats.html', playlists=playlists, suggested_songs=suggested_songs, albums=albums, stats_data=stats_data)
bp_user.add_url_rule('/creator_stats', view_func=CreatorStatsView.as_view('creator_stats'))

# all creators
class AllCreatorsView(MethodView):
    def get(self):
        # query all creators
        creators = User.query.filter_by(role='creator').all()
        is_flagged = list()
        for creator in creators:
            flagged_creator = FlaggedCreator.query.filter_by(user_id=creator.id).first()
            if flagged_creator:
                is_flagged.append(True)
            else:
                is_flagged.append(False)
        
        # stats
        tot_user = User.query.filter_by(role='user').count()
        tot_creator = User.query.filter_by(role='creator').count()
        tot_album = Album.query.count()
        tot_song = Song.query.count()
        tot_playlist = Playlist.query.count()

        stats_headings = ['Total Normal Users', 'Total Creators', 'Total Albums', 'Total Songs', 'Total Playlists']
        stats_data = [{'heading': h, 'total': t} for h, t in zip(stats_headings, [tot_user, tot_creator, tot_album, tot_song, tot_playlist])]

        return render_template('creators.html', creators=creators,is_flagged=is_flagged ,stats_data=stats_data)
bp_user.add_url_rule('/all_creators', view_func=AllCreatorsView.as_view('all_creators'))

# flagged_creators
class FlagCreatorView(MethodView):
    def get(self, creator_id, admin_id):
        flagged_creator = FlaggedCreator(user_id=creator_id, admin_id=admin_id)
        db.session.add(flagged_creator)
        db.session.commit()
        flash('Creator flagged successfully!', 'success')
        return redirect(url_for('user.all_creators'))
bp_user.add_url_rule('/flag_creator/<string:creator_id>/<string:admin_id>', view_func=FlagCreatorView.as_view('flag_creator'))

class UnflagCreatorView(MethodView):
    def get(self, creator_id):
        flagged_creator = FlaggedCreator.query.filter_by(user_id=creator_id).first()
        db.session.delete(flagged_creator)
        db.session.commit()
        flash('Creator whitelisted successfully!', 'success')
        return redirect(url_for('user.all_creators'))
bp_user.add_url_rule('/unflag_creator/<string:creator_id>', view_func=UnflagCreatorView.as_view('unflag_creator'))