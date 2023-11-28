from flask import Blueprint, render_template,redirect,url_for,flash,request, current_app
from flask.views import MethodView
from flask_login import current_user, login_required

from forms.music_form import MusicForm
from extensions.extension import db 
from models.music_model import Song, SongFile, FlaggedContent, Rating
from sqlalchemy import or_

from werkzeug.utils import secure_filename
import os
import random
import requests

from decorators.contents import admin_stats, user_contents
from decorators.role_decorator import creator_required, admin_or_creator_required, admin_required
'''
+--------------------------------------------------------------+
|                         blueprint song                       |
+--------------------------------------------------------------+
'''
bp_song = Blueprint('song', __name__)

#------------------------------------upload_song----------------------------#
class UploadSongView(MethodView):
    @creator_required
    def get(self):
        form = MusicForm()

        #contents
        suggested_songs, playlists, albums = user_contents()

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

                # for demo purpose
                new_file_name ='demo.mp3'

                audio_file_path = os.path.join(current_app.config['SONG_UPLOAD_FOLDER'], new_file_name)
                audio_file.save(audio_file_path)

                # song object
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

#------------------------------------play_song----------------------------#
class PlaySongView(MethodView):
    @login_required
    def get(self, id):
        song = Song.query.get(id)
        song_file = SongFile.query.filter_by(song_id=id).first()
        song.hits += 1
        db.session.commit()

        #contents
        suggested_songs, playlists, albums = user_contents()

        return render_template('play_song.html', song=song, song_file=song_file, playlists=playlists, suggested_songs=suggested_songs, albums=albums)
bp_song.add_url_rule('/play_song/<string:id>', view_func=PlaySongView.as_view('play_song'))

#------------------------------------song_lyrics----------------------------#
class SongLyricsView(MethodView):
    @login_required
    def get(self, id):
        song = Song.query.get(id)
        lyrics = song.lyrics

        # admin
        api_url = request.url_root + 'songs/songs'
        songs = requests.get(api_url)
        songs = songs.json()

        #contents
        suggested_songs, playlists, albums = user_contents()

        return render_template('song_lyrics.html', song=song, lyrics=lyrics, playlists=playlists, suggested_songs=suggested_songs, albums=albums, songs=songs)
bp_song.add_url_rule('/song_lyrics/<string:id>', view_func=SongLyricsView.as_view('song_lyrics'))


#------------------------------------uploaded_songs----------------------------#
class UploadedSongsView(MethodView):
    @admin_or_creator_required
    def get(self):
        api_url = request.url_root + 'users/users/' + str(current_user.id) + '/songs'
        songs = requests.get(api_url)
        songs = songs.json()

        #contents
        suggested_songs, playlists, albums = user_contents()
        
        return render_template('uploaded_songs.html', songs=songs, playlists=playlists, suggested_songs=suggested_songs, albums=albums)
bp_song.add_url_rule('/uploaded_songs', view_func=UploadedSongsView.as_view('uploaded_songs'))

#------------------------------------delete_song----------------------------#
class DeleteSongView(MethodView):
    @admin_or_creator_required
    def get(self, id):
        api_url = request.url_root + 'songs/songs/' + str(id)
        response = requests.delete(api_url)
        if response.status_code == 204:
            flash('Successfully deleted song!', 'success')
        else:
            flash('Error deleting song!', 'danger')
        if current_user.role == 'creator':
            return redirect(url_for('song.uploaded_songs'))
        else:
            return redirect(url_for('song.all_songs', genre='all'))
bp_song.add_url_rule('/delete_song/<string:id>', view_func=DeleteSongView.as_view('delete_song'))

#------------------------------------all_songs----------------------------#
class AllSongsView(MethodView):
    @admin_required
    def get(self, genre):
        if genre == 'all':
            songs = Song.query.all()
        else:
            songs = Song.query.filter_by(genre=genre).all()
        
        is_flagged = list()
        for song in songs:
            flagged_song = FlaggedContent.query.filter_by(song_id=song.id).first()
            if flagged_song:
                is_flagged.append(True)
            else:
                is_flagged.append(False)
        
        # stats
        stats_data = admin_stats()

        return render_template('songs.html', songs=songs,is_flagged=is_flagged ,stats_data=stats_data)
bp_song.add_url_rule('/all_songs/<string:genre>', view_func=AllSongsView.as_view('all_songs'))

#------------------------------------song_search----------------------------#
class SongSearchView(MethodView):
    @login_required
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
        suggested_songs, playlists, albums = user_contents()

        return render_template('song_search.html', songs=songs, playlists=playlists, suggested_songs=suggested_songs, albums=albums)
bp_song.add_url_rule('/song_search', view_func=SongSearchView.as_view('song_search'))

#------------------------------------flag_song----------------------------#
class FlagSongView(MethodView):
    @admin_required
    def get(self, song_id):
        song_to_flag = Song.query.get(song_id)

        is_flagged = FlaggedContent.query.filter_by(song_id=song_id).first()
        if is_flagged:
            is_flagged = True
        else:
            is_flagged = False
            
        # songs
        songs = Song.query.all()

        # stats
        stats_data = admin_stats()

        return render_template('flag_song.html', song_to_flag=song_to_flag, is_flagged=is_flagged,stats_data=stats_data, songs=songs)
    
    @admin_required
    def post(self, song_id):
        reason = request.form.get('reason')
        song_id = song_id
        admin_id = request.form.get('admin_id')

        flagged_content = FlaggedContent(song_id=song_id, reason=reason, admin_id=admin_id)
        db.session.add(flagged_content)
        db.session.commit()
        flash ('Content flagged successfully!', 'success')
        return redirect (url_for('song.all_songs', genre='all'))
bp_song.add_url_rule('/flag_song/<song_id>', view_func=FlagSongView.as_view('flag_song'))

#------------------------------------unflag_song----------------------------#
class UnflagSongView(MethodView):
    @admin_required
    def get(self, song_id):
        flagged_content = FlaggedContent.query.filter_by(song_id=song_id).first()
        print(f'found song: {flagged_content.reason}')
        db.session.delete(flagged_content)
        db.session.commit()
        flash ('Content unflagged successfully!', 'success')
        return redirect (url_for('song.all_songs', genre='all'))
bp_song.add_url_rule('/unflag_song/<song_id>', view_func=UnflagSongView.as_view('unflag_song'))

#------------------------------------rate_song----------------------------#
class RateSongView(MethodView):
    @login_required
    def get(self, song_id, rating):
        user_id = current_user.id 

        song = Song.query.get(song_id)
        if song:
            existing_rating = Rating.query.filter_by(user_id=user_id, song_id=song_id).first()
            if existing_rating:
                existing_rating.value = rating
            else:
                new_rating = Rating(user_id=user_id, song_id=song_id, value=rating)
                db.session.add(new_rating)

        song = Song.query.get(song_id)
        if song:
            total_ratings = sum(rating.value for rating in song.ratings)
            avg_rating = total_ratings / len(song.ratings)
            song.average_rating = round(avg_rating, 1)

        db.session.commit()
        flash('Rating submitted successfully!', 'success')
        return redirect(url_for('user.dashboard'))
bp_song.add_url_rule('/rate_song/<string:song_id>/<int:rating>', view_func=RateSongView.as_view('rate_song'))