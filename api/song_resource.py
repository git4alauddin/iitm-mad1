from flask_restx import Resource, Namespace
from models.music_model import Song, SongFile
from api.api_models import song_model
from extensions.extension import db
from decorators.role_decorator import admin_required
import os
from flask import current_app

ns_song = Namespace('song')

@ns_song.route('/songs/<string:id>')
class SongApi(Resource):
    @ns_song.marshal_with(song_model)
    def get(self, id):
        song = Song.query.get(id)
        return song
    
    def delete(self, id):
        song = Song.query.get(id)

        # delete song
        song_file = SongFile.query.filter_by(song_id=id).first()
        file_name = song_file.file_name
        song_file_path = os.path.join(current_app.config['SONG_UPLOAD_FOLDER'], file_name)
        if os.path.exists(song_file_path):
            os.remove(song_file_path)
        
        # delete song_metadata
        db.session.delete(song_file)
        db.session.delete(song)
        db.session.commit()
        return {'message': 'Song deleted'}, 204

@ns_song.route('/songs')
class SongsListApi(Resource):
    @ns_song.marshal_with(song_model)
    def get(self):
        song = Song.query.all()
        return song
    
ns_songs = Namespace('songs')
@ns_songs.route('/songs')
class SongsListApi(Resource):
    # @admin_required
    @ns_songs.marshal_with(song_model)
    def get(self):
        song = Song.query.all()
        return song