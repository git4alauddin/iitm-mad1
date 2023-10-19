from flask import Blueprint, render_template,redirect,url_for,flash,request, current_app
from flask.views import MethodView
from forms.music_form import MusicForm
from flask_login import current_user
from extensions.extension import db 
from decorators.role_decorator import creator_required
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import random
from models.music_model import Song, SongFile
import requests


bp_song = Blueprint('song', __name__)
# view song_upload
class UploadSongView(MethodView):
    def get(self):
        form = MusicForm()
        return render_template('upload_song.html', form=form)
    @creator_required
    def post(self):
        form = MusicForm()

        if form.validate_on_submit():
            audio_file = form.audio_file.data
            if audio_file:
                title = form.title.data
                artist = form.artist.data
                random_suffix = random.randint(0, 10000)
                
                creator_id = current_user.id
                original_filename = secure_filename(audio_file.filename)
                file_extension = original_filename.rsplit('.', 1)[1]
                new_file_name = f'{artist}_{title}_{random_suffix}.{file_extension}'

                audio_file_path = os.path.join(current_app.config['SONG_UPLOAD_FOLDER'], new_file_name)
                audio_file.save(audio_file_path)

                # extract remaining song info
                genre = form.genre.data
                lyrics = form.lyrics.data

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
                return redirect(url_for('music.upload_song'))
        else:
            flash('All fields are required', 'danger')
            return redirect(url_for('music.upload_song'))
bp_song.add_url_rule('/upload_song', view_func=UploadSongView.as_view('upload_song'))

# view play_song
class PlaySongView(MethodView):
    def get(self, id):
        song = Song.query.get(id)
        song_file = SongFile.query.filter_by(song_id=id).first()
        song.hits += 1
        db.session.commit()
        return render_template('play_song.html', song=song, song_file=song_file)
bp_song.add_url_rule('/play_song/<string:id>', view_func=PlaySongView.as_view('play_song'))

# view uploaded_songs
class UploadedSongsView(MethodView):
    def get(self):
        api_url = request.url_root + 'users/users/' + str(current_user.id) + '/songs'
        songs = requests.get(api_url)
        songs = songs.json()
        
        return render_template('uploaded_songs.html', songs=songs)
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
