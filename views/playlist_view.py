from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask.views import MethodView
from flask_login import current_user
from extensions.extension import db
from models.music_model import Song, Playlist


bp_playlist = Blueprint('playlist', __name__)
# view create_playlist
class CreatePlaylistView(MethodView):
    def get(self, page=1):
        # Fetch the list of songs created by the  users for the checkboxes
        # trying pagination 
        per_page = 3
        songs = Song.query.paginate(page=page, per_page=per_page)
        return render_template('create_playlist.html', songs=songs)

    def post(self, page):
        title = request.form.get('title')
        selected_song_ids = request.form.getlist('songs[]')  # Get selected song IDs

        if not title:
            flash('Title is required.', 'danger')
            return redirect(url_for('playlist.create_playlist', page=1))
        elif not selected_song_ids:
            flash('Please select at least one song.', 'danger')
            return redirect(url_for('playlist.create_playlist', page=1))
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

bp_playlist.add_url_rule('/create_playlist/<int:page>', view_func=CreatePlaylistView.as_view('create_playlist'))