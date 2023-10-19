from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask.views import MethodView
from flask_login import current_user
from extensions.extension import db
from models.music_model import Song, Playlist
import requests


bp_playlist = Blueprint('playlist', __name__)
# view create_playlist
class CreatePlaylistView(MethodView):
    def get(self):
        playlists = Playlist.query.filter_by(user_id=current_user.id).all()
        return render_template('create_playlist.html', playlists=playlists)

    def post(self):
        title = request.form.get('title')

        if not title:
            flash('Title is required.', 'danger')
            return redirect(url_for('playlist.create_playlist'))
        else:
            api_url = request.url_root + 'playlists/playlists/' + str(current_user.id)
            response = requests.post(api_url, json={'title': title})

            if response.status_code == 201:
                flash('Successfully created playlist!', 'success')
                return redirect(url_for('user.dashboard'))
            else:
                flash('Error creating playlist!', 'danger')
                return redirect(url_for('user.dashboard'))
        
bp_playlist.add_url_rule('/create_playlist/', view_func=CreatePlaylistView.as_view('create_playlist'))

class PlaylistSongsView(MethodView):
    def get(self, id):
        api_url = request.url_root + 'playlists/playlists/' + str(id) + '/songs'
        playlist_song_res = requests.get(api_url)

        api_url = request.url_root + 'songs/songs'
        suggested_song_res = requests.get(api_url)

        if playlist_song_res.status_code == 200:
            songs = playlist_song_res.json()
            playlist = Playlist.query.get(id)

            # suggest songs to add to the playlist
            suggested_songs = suggested_song_res.json()

            return render_template('add_songs.html', songs=songs, playlist=playlist, suggested_songs=suggested_songs)
        else:
            flash('Error fetching songs!', 'danger')
            return redirect(url_for('user.dashboard'))
        
    def post(self, id):
        song_id = request.form.get('song_id')
        print(f'song_id: {song_id}')
        api_url = request.url_root + 'playlists/playlists/' + str(id) + '/songs/' + str(song_id)

        response = requests.post(api_url)

        if response.status_code == 201:
            flash('Successfully added song to playlist!', 'success')
            return redirect(url_for('playlist.add_songs', id=id))
        else:
            # temporarily
            flash('Song is already in the playlist!', 'danger')
            return redirect(url_for('playlist.add_songs', id=id))
bp_playlist.add_url_rule('/add_songs/<string:id>', view_func=PlaylistSongsView.as_view('add_songs'))
