from flask_restx import Resource, Namespace
from flask import current_app
from models.music_model import Song, SongFile
from api.api_models import song_model
from extensions.extension import db
import os
'''
+--------------------------------------------------------------+
|                         namespace songs                      |
+--------------------------------------------------------------+
'''
ns_songs = Namespace('songs')

#---------------------------------/songs/<string:id>-------------------------------#
@ns_songs.route('/songs/<string:id>')
class SongApi(Resource):
    @ns_songs.marshal_with(song_model)
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

#---------------------------------/songs-------------------------------#
@ns_songs.route('/songs')
class SongsListApi(Resource):
    @ns_songs.marshal_with(song_model)
    def get(self):
        song = Song.query.all()
        return song, 200