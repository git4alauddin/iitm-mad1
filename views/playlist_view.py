from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask.views import MethodView
from flask_login import current_user
from extensions.extension import db
from models.music_model import Song, Playlist
import requests


bp_playlist = Blueprint('playlist', __name__)

class CreatePlaylistView(MethodView):
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
        return render_template('create_playlist.html', playlists=playlists, suggested_songs=suggested_songs, albums=albums)

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
            else:
                flash('Error creating playlist!', 'danger')
            return redirect(url_for('user.dashboard'))
        
bp_playlist.add_url_rule('/create_playlist/', view_func=CreatePlaylistView.as_view('create_playlist'))

# view remove playlist
class RemovePlaylistView(MethodView):
    def get(self, id):
        api_url = request.url_root + 'playlists/playlists/' + str(id)
        response = requests.delete(api_url)

        if response.status_code == 204:
            flash('Successfully removed playlist!', 'success')
        else:
            flash('Error removing playlist!', 'danger')

        return redirect(url_for('user.dashboard'))

bp_playlist.add_url_rule('/remove_playlist/<string:id>/', view_func=RemovePlaylistView.as_view('remove_playlist'))

# view add_songs_to_playlist
class PlaylistAddSongsView(MethodView):
    def get(self, id):
        api_url = request.url_root + 'playlists/playlists/' + str(id) + '/songs'
        playlist_song_res = requests.get(api_url)

        # temporarily handling song suggestion to add to the playlist
        api_url = request.url_root + 'songs/songs'
        suggested_song_res = requests.get(api_url)

        if playlist_song_res.status_code == 200:
            songs = playlist_song_res.json()
            playlist = Playlist.query.get(id)

            suggested_songs = suggested_song_res.json()

            return render_template('add_songs_to_playlist.html', songs=songs, playlist=playlist, suggested_songs=suggested_songs)
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
        else:
            # temporarily handled the unique constrain error
            flash('Song is already in the playlist!', 'danger')
        return redirect(url_for('playlist.add_songs_to_playlist', id=id))
bp_playlist.add_url_rule('/add_songs_to_playlist/<string:id>', view_func=PlaylistAddSongsView.as_view('add_songs_to_playlist'))

# view remove songs of a playlist
class PlaylistRemoveSongsView(MethodView):
    def post(self, id):
        song_id = request.form.get('song_id')
        api_url = request.url_root + 'playlists/playlists/' + str(id) + '/songs/' + str(song_id)

        response = requests.delete(api_url)

        if response.status_code == 204:
            flash('Successfully removed song from playlist!', 'success')
        else:
            flash('Error removing song from playlist!', 'danger')

        return redirect(url_for('playlist.add_songs_to_playlist', id=id))

bp_playlist.add_url_rule('/playlist_remove_songs/<string:id>', view_func=PlaylistRemoveSongsView.as_view('playlist_remove_songs'))
