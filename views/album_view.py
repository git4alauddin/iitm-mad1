from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask.views import MethodView
from flask_login import current_user

from decorators.contents import admin_stats, user_contents
from decorators.role_decorator import creator_required, admin_or_creator_required, admin_required

from models.music_model import Album
from models.user_model import FlaggedCreator
import requests
'''
+--------------------------------------------------------------+
|                         blueprint album                      |
+--------------------------------------------------------------+
'''
bp_album = Blueprint('album', __name__)

#------------------------------------create_album---------------------------------#
class CreateAlbumView(MethodView):
    @creator_required
    def get(self):
        flagged_creator = FlaggedCreator.query.filter_by(user_id=current_user.id).first()
        if flagged_creator:
            flash('You can not create album now!', 'danger')
            return redirect(url_for('user.dashboard'))
        else:
            #contents
            suggested_songs, playlists, albums = user_contents()
            return render_template('create_album.html', albums=albums, suggested_songs=suggested_songs, playlists=playlists)

    @creator_required
    def post(self):
        title = request.form.get('title')
        release_year = request.form.get('release_year')

        if not title:
            flash('Title is required.', 'danger')
            return redirect(url_for('album.create_album'))
        elif not release_year:
            flash('Release release_year is required.', 'danger')
            return redirect(url_for('album.create_album'))
        elif not release_year.isnumeric() and len(release_year) != 4:
            flash('Release year must be a year.', 'danger')
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

#--------------------------------------remove_album---------------------------------#
class RemoveAlbumView(MethodView):
    @admin_or_creator_required
    def get(self, id):
        api_url = request.url_root + 'albums/albums/' + str(id)
        response = requests.delete(api_url)

        if response.status_code == 204:
            flash('Successfully removed album!', 'success')
        else:
            flash('Error removing album!', 'danger')
        if current_user.role == 'creator':
            return redirect(url_for('user.dashboard'))
        else:
            return redirect(url_for('album.all_albums'))

bp_album.add_url_rule('/remove_album/<string:id>/', view_func=RemoveAlbumView.as_view('remove_album'))

#---------------------------------------add_songs_to_album----------------------------#
class AlbumAddSongsView(MethodView):
    @creator_required
    def get(self, id): 
        flagged_creator = FlaggedCreator.query.filter_by(user_id=current_user.id).first()
        if flagged_creator:
            flash('You can not upload song now!', 'danger')
            return redirect(url_for('user.dashboard'))
        else:
            api_url = request.url_root + 'albums/albums/' + str(id) + '/songs'
            album_song_res = requests.get(api_url)

            if album_song_res.status_code == 200:
                songs = album_song_res.json()
                album = Album.query.get(id)

                #contents
                suggested_songs, playlists, albums = user_contents()

                api_url = request.url_root + 'users/users/' + str(current_user.id) + '/songs'
                s_songs = requests.get(api_url)
                s_songs = s_songs.json()
                uploaded_songs = s_songs
                
                return render_template('add_songs_to_album.html', songs=songs, album=album, suggested_songs=suggested_songs, playlists=playlists, albums=albums, uploaded_songs=uploaded_songs)
            else:
                flash('Error fetching songs!', 'danger')
                return redirect(url_for('user.dashboard'))

    @creator_required  
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

#---------------------------------------remove_songs_from_album----------------------------#
class AlbumRemoveSongsView(MethodView):
    @creator_required
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

#---------------------------------------all_albums------------------------------------#
class AllAlbumsView(MethodView):
    @admin_required
    def get(self):
        api_url = request.url_root + 'albums/albums/' 
        response = requests.get(api_url)
        albums = response.json()

        # stats
        stats_data = admin_stats()
        
        return render_template('albums.html', albums=albums, stats_data=stats_data)
bp_album.add_url_rule('/all_albums', view_func=AllAlbumsView.as_view('all_albums'))