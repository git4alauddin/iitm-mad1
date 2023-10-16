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
from models.music_model import Song, SongFile, Playlist


bp_music = Blueprint('music', __name__)
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
bp_music.add_url_rule('/upload_song', view_func=UploadSongView.as_view('upload_song'))

# view play_song
class PlaySongView(MethodView):
    def get(self, id):
        song = Song.query.get(id)
        song_file = SongFile.query.filter_by(song_id=id).first()
        song.hits += 1
        db.session.commit()
        return render_template('play_song.html', song=song, song_file=song_file)
bp_music.add_url_rule('/play_song/<string:id>', view_func=PlaySongView.as_view('play_song'))

# view songs_list
class SongsListView(MethodView):
    def get(self):
        songs = Song.query.filter_by(creator_id=current_user.id)
        return render_template('songs_list.html', songs=songs)
bp_music.add_url_rule('/songs_list', view_func=SongsListView.as_view('songs_list'))


# view create_playlist
class CreatePlaylistView(MethodView):
    def get(self, page=1):
        # Fetch the list of songs created by the  users for the checkboxes
        # trying pagination 
        per_page = 2
        songs = Song.query.paginate(page=page, per_page=per_page)
        return render_template('create_playlist.html', songs=songs)

    def post(self, page):
        title = request.form.get('title')
        selected_song_ids = request.form.getlist('songs[]')  # Get selected song IDs

        if not title:
            flash('Title is required.', 'danger')
            return redirect(url_for('music.create_playlist'))
        elif not selected_song_ids:
            flash('Please select at least one song.', 'danger')
            return redirect(url_for('music.create_playlist'))
        else:
            # Create a new playlist and add it to the database
            playlist = Playlist(title=title, user_id=current_user.id)
            db.session.add(playlist)
            db.session.commit()

            # Add selected songs to the playlist
            songs_to_update = Song.query.filter(Song.id.in_(selected_song_ids)).all()
            for song in songs_to_update:
                playlist.songs.append(song)

            db.session.commit()

            flash('Playlist created successfully!', 'success')
            return redirect(url_for('user.dashboard'))

bp_music.add_url_rule('/create_playlist/<int:page>', view_func=CreatePlaylistView.as_view('create_playlist'))