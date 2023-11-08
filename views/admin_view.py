from flask import Blueprint, render_template,redirect,url_for,flash,request
from flask.views import MethodView
import requests
from models.music_model import Song,Album,Playlist
from models.user_model import User

# --------------------------------------blueprint admin--------------------------------------------------------
bp_admin = Blueprint('admin', __name__)

# view admin_visuals
class AdminVisualsView(MethodView):
    def get(self):
        # stats
        tot_user = User.query.filter_by(role='user').count()
        tot_creator = User.query.filter_by(role='creator').count()
        tot_album = Album.query.count()
        tot_song = Song.query.count()
        tot_playlist = Playlist.query.count()

        stats_headings = ['Total Normal Users', 'Total Creators', 'Total Albums', 'Total Songs', 'Total Playlists']
        stats_data = [{'heading': h, 'total': t} for h, t in zip(stats_headings, [tot_user, tot_creator, tot_album, tot_song, tot_playlist])]

        labels = ['Total Normal Users', 'Total Creators', 'Total Albums', 'Total Songs', 'Total Playlists']
        values = [tot_user, tot_creator, tot_album, tot_song, tot_playlist]

        # songs with different generes: romantic, pop, hip-hop, rock
        # songs with different genres: romantic, pop, hip-hop, rock
        genres = ['romantic', 'pop', 'hip-hop', 'rock']
        genre_counts = [0, 0, 0, 0]
        for song in Song.query.all():
            for i, genre in enumerate(genres):
                if song.genre == genre:
                    genre_counts[i] += 1
        
        return render_template('admin_visuals.html', labels=labels, values=values, stats_data=stats_data, genre_counts=genre_counts, genres=genres)
bp_admin.add_url_rule('/admin_visuals', view_func=AdminVisualsView.as_view('admin_visuals'))


