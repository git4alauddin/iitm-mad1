from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask.views import MethodView
from flask_login import current_user
from extensions.extension import db
from models.music_model import Song, Album, Playlist
from models.user_model import User
import requests

# -------------------------------------------blueprint album-------------------------------------------------------------
bp_album = Blueprint('album', __name__)

class CreateAlbumView(MethodView):
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
        return render_template('create_album.html', albums=albums, suggested_songs=suggested_songs, playlists=playlists)

    def post(self):
        title = request.form.get('title')
        release_year = request.form.get('release_year')

        if not title:
            flash('Title is required.', 'danger')
            return redirect(url_for('album.create_album'))
        elif not release_year:
            flash('Release release_year is required.', 'danger')
            return redirect(url_for('album.create_album'))
        else:
            api_url = request.url_root + 'albums/albums/' + str(current_user.id)
            response = requests.post(api_url, json={'title': title, 'release_year': release_year})


            if response.status_code == 201:
                flash('Successfully created album!', 'success')
            else:
                flash('Error creating album!', 'danger')
            return redirect(url_for('user.dashboard'))
        
bp_album.add_url_rule('/create_album', view_func=CreateAlbumView.as_view('create_album'))

# view remove album
class RemoveAlbumView(MethodView):
    def get(self, id):
        api_url = request.url_root + 'albums/albums/' + str(id)
        response = requests.delete(api_url)

        if response.status_code == 204:
            flash('Successfully removed album!', 'success')
        else:
            flash('Error removing album!', 'danger')

        return redirect(url_for('user.dashboard'))

bp_album.add_url_rule('/remove_album/<string:id>/', view_func=RemoveAlbumView.as_view('remove_album'))

# view add_songs_to_album
class AlbumAddSongsView(MethodView):
    def get(self, id): 
        print(f'album_id: {id}')
        api_url = request.url_root + 'albums/albums/' + str(id) + '/songs'
        album_song_res = requests.get(api_url)

        # temporarily handling song suggestion to add to the album
        api_url = request.url_root + 'songs/songs'
        suggested_song_res = requests.get(api_url)

        if album_song_res.status_code == 200:
            songs = album_song_res.json()
            album = Album.query.get(id)

            suggested_songs = suggested_song_res.json()

            return render_template('add_songs_to_album.html', songs=songs, album=album, suggested_songs=suggested_songs)
        else:
            flash('Error fetching songsSSS!', 'danger')
            return redirect(url_for('user.dashboard'))
        
    def post(self, id):
        song_id = request.form.get('song_id')
        print(f'song_id: {song_id}')
        api_url = request.url_root + 'albums/albums/' + str(id) + '/songs/' + str(song_id)

        response = requests.post(api_url)

        if response.status_code == 201:
            flash('Successfully added song to album!', 'success')
        else:
            # temporarily handled the unique constrain error
            flash('Song is already in the album!', 'danger')
        return redirect(url_for('album.add_songs_to_album', id=id))
bp_album.add_url_rule('/add_songs_to_album/<string:id>', view_func=AlbumAddSongsView.as_view('add_songs_to_album'))

# view remove songs of a album
class AlbumRemoveSongsView(MethodView):
    def post(self, id):
        song_id = request.form.get('song_id')
        api_url = request.url_root + 'albums/albums/' + str(id) + '/songs/' + str(song_id)

        response = requests.delete(api_url)

        if response.status_code == 204:
            flash('Successfully removed song from album!', 'success')
        else:
            flash('Error removing song from album!', 'danger')

        return redirect(url_for('album.add_songs_to_album', id=id))

bp_album.add_url_rule('/album_remove_songs/<string:id>', view_func=AlbumRemoveSongsView.as_view('album_remove_songs'))

class AllAlbumsView(MethodView):
    def get(self):
        api_url = request.url_root + 'albums/albums/' 
        response = requests.get(api_url)
        albums = response.json()
        
        # stats
        tot_user = User.query.filter_by(role='user').count()
        tot_creator = User.query.filter_by(role='creator').count()
        tot_album = Album.query.count()
        tot_song = Song.query.count()
        tot_playlist = Playlist.query.count()

        stats_headings = ['Total Normal Users', 'Total Creators', 'Total Albums', 'Total Songs', 'Total Playlists']
        stats_data = [{'heading': h, 'total': t} for h, t in zip(stats_headings, [tot_user, tot_creator, tot_album, tot_song, tot_playlist])]

        return render_template('albums.html', albums=albums, stats_data=stats_data)
bp_album.add_url_rule('/all_albums', view_func=AllAlbumsView.as_view('all_albums'))