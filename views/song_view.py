from flask import Blueprint, render_template,redirect,url_for,flash,request, current_app
from flask.views import MethodView
from forms.music_form import MusicForm
from flask_login import current_user
from extensions.extension import db 
from decorators.role_decorator import creator_required
from werkzeug.utils import secure_filename
import os
import random
from models.music_model import Song, SongFile, Album, Playlist
from models.user_model import User
import requests
from sqlalchemy import or_

# --------------------------------------blueprint song--------------------------------------------------------
bp_song = Blueprint('song', __name__)
# view song_upload
class UploadSongView(MethodView):
    def get(self):
        form = MusicForm()

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
        return render_template('upload_song.html', form=form, playlists=playlists, suggested_songs=suggested_songs, albums=albums)
    @creator_required
    def post(self):
        form = MusicForm()

        if form.validate_on_submit():
            title = form.title.data
            if not title:
                flash('Title is required', 'danger')
                return redirect(url_for('song.upload_song'))
            artist = form.artist.data
            if not artist:
                flash('Artist is required', 'danger')
                return redirect(url_for('song.upload_song'))
            genre = form.genre.data
            if not genre:
                flash('Genre is required', 'danger')
                return redirect(url_for('song.upload_song'))
            lyrics = form.lyrics.data
            if not lyrics:
                flash('Lyrics is required', 'danger')
                return redirect(url_for('song.upload_song'))

            audio_file = form.audio_file.data
            if audio_file:
                
                random_suffix = random.randint(0, 10000)
                
                creator_id = current_user.id
                original_filename = secure_filename(audio_file.filename)
                file_extension = original_filename.rsplit('.', 1)[1]
                new_file_name = f'{artist}_{title}_{random_suffix}.{file_extension}'

                audio_file_path = os.path.join(current_app.config['SONG_UPLOAD_FOLDER'], new_file_name)
                audio_file.save(audio_file_path)

                # create song object to insert into the table
                song = Song(
                    title=title,
                    artist=artist,
                    genre=genre,  
                    
                    creator_id=creator_id,  
                    lyrics=lyrics
                    )
                try:
                    db.session.add(song)
                    db.session.commit()

                    # add the song_file
                    song_file = SongFile(song_id=song.id, file_name=new_file_name)
                    db.session.add(song_file)
                    db.session.commit()
      
                    flash('Song added successfully!', 'success')
                    return redirect(url_for('user.dashboard'))
                except Exception as e:
                    db.session.rollback()
                    flash(f'Error: {str(e)}', 'danger')
            
                return redirect(url_for('user.dashboard'))
            else:
                flash('Please select an audio file', 'danger')
                return redirect(url_for('song.upload_song'))
        else:
            flash('All fields are required', 'danger')
            return redirect(url_for('song.upload_song'))
bp_song.add_url_rule('/upload_song', view_func=UploadSongView.as_view('upload_song'))

# view play_song
class PlaySongView(MethodView):
    def get(self, id):
        # main logic
        song = Song.query.get(id)
        song_file = SongFile.query.filter_by(song_id=id).first()
        song.hits += 1
        db.session.commit()

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
        return render_template('play_song.html', song=song, song_file=song_file, playlists=playlists, suggested_songs=suggested_songs, albums=albums)
bp_song.add_url_rule('/play_song/<string:id>', view_func=PlaySongView.as_view('play_song'))

# song lyrics view
class SongLyricsView(MethodView):
    def get(self, id):
        # main logic to retrieve song lyrics
        song = Song.query.get(id)
        lyrics = song.lyrics

        # admin content
        api_url = request.url_root + 'songs/songs'
        songs = requests.get(api_url)
        songs = songs.json()

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

        return render_template('song_lyrics.html', song=song, lyrics=lyrics, playlists=playlists, suggested_songs=suggested_songs, albums=albums, songs=songs)

bp_song.add_url_rule('/song_lyrics/<string:id>', view_func=SongLyricsView.as_view('song_lyrics'))


# view uploaded_songs
class UploadedSongsView(MethodView):
    def get(self):
        api_url = request.url_root + 'users/users/' + str(current_user.id) + '/songs'
        songs = requests.get(api_url)
        songs = songs.json()
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
        
        return render_template('uploaded_songs.html', songs=songs, playlists=playlists, suggested_songs=suggested_songs, albums=albums)
bp_song.add_url_rule('/uploaded_songs', view_func=UploadedSongsView.as_view('uploaded_songs'))

# view delete a song
class DeleteSongView(MethodView):
    def get(self, id):
        api_url = request.url_root + 'songs/songs/' + str(id)
        response = requests.delete(api_url)
        if response.status_code == 204:
            flash('Successfully deleted song!', 'success')
        else:
            flash('Error deleting song!', 'danger')
        return redirect(url_for('song.uploaded_songs'))
bp_song.add_url_rule('/delete_song/<string:id>', view_func=DeleteSongView.as_view('delete_song'))
class AllSongsView(MethodView):
    def get(self):
        api_url = request.url_root + 'songs/songs'
        songs = requests.get(api_url)
        songs = songs.json()

        

        # stats
        tot_user = User.query.filter_by(role='user').count()
        tot_creator = User.query.filter_by(role='creator').count()
        tot_album = Album.query.count()
        tot_song = Song.query.count()
        tot_playlist = Playlist.query.count()

        stats_headings = ['Total Normal Users', 'Total Creators', 'Total Albums', 'Total Songs', 'Total Playlists']
        stats_data = [{'heading': h, 'total': t} for h, t in zip(stats_headings, [tot_user, tot_creator, tot_album, tot_song, tot_playlist])]
        return render_template('songs.html', songs=songs, stats_data=stats_data)
bp_song.add_url_rule('/all_songs', view_func=AllSongsView.as_view('all_songs'))

class SongSearchView(MethodView):
    def get(self):
      
        query = request.args.get('query')
        query = f"%{query}%"
    
        songs = Song.query.filter(
                or_(
                    Song.title.contains(query),
                    Song.artist.contains(query),
                    Song.genre.contains(query)
                )
            ).all()

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

        return render_template('song_search.html', songs=songs, playlists=playlists, suggested_songs=suggested_songs, albums=albums)
bp_song.add_url_rule('/song_search', view_func=SongSearchView.as_view('song_search'))