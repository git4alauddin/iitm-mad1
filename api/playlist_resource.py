from flask_restx import Namespace, Resource
from flask import request
from models.music_model import Playlist, Song
from extensions.extension import db
from api.api_models import playlist_model, song_model, playlist_input_model
'''
+--------------------------------------------------------------+
|                         namespace playlists                  |
+--------------------------------------------------------------+
'''
ns_playlists = Namespace('playlists')

#---------------------------------/playlists/<string:id>-------------------------------#
@ns_playlists.route('/playlists/<string:id>')
class PlaylistApi(Resource):
    @ns_playlists.marshal_with(playlist_model)
    def get(self, id):
        playlist = Playlist.query.get(id)
        return playlist, 200
    
    @ns_playlists.expect(playlist_input_model)
    @ns_playlists.marshal_with(playlist_model)
    def post(self, id):
        title = request.json.get('title')
        playlist = Playlist(title=title, user_id=id)
        db.session.add(playlist)
        db.session.commit()
        return playlist, 201
    
    @ns_playlists.marshal_with(playlist_model)
    def delete(self, id):
        playlist = Playlist.query.get(id)
        db.session.delete(playlist)
        db.session.commit()
        return Playlist.query.get(id), 204

#----------------------------------/playlists/<string:id>/songs-------------------------------#
@ns_playlists.route('/playlists/<string:id>/songs')
class PlaylistSongsApi(Resource):
    @ns_playlists.marshal_with(song_model)
    def get(self, id):
        playlist = Playlist.query.get(id)
        if not playlist:
            return {'error': 'Playlist not found'}, 404
        songs = playlist.songs
        return songs, 200

#-----------------------------/playlists/<string:id>/songs/<string:song_id-----------------------------#
@ns_playlists.route('/playlists/<string:id>/songs/<string:song_id>')
class PlaylistSongApi(Resource):
    @ns_playlists.marshal_with(song_model)
    def get(self, id, song_id):
        playlist = Playlist.query.get(id)
        if not playlist:
            return {'error': 'Playlist not found'}, 404
        
        song = None 
        for s in playlist.songs:
            if s.id == song_id:
                song = s
        if song:
            return song 
        else:
            return {"message": "Song not found"}, 404
        
    @ns_playlists.marshal_with(song_model)
    def post(self, id, song_id):
        playlist = Playlist.query.get(id)
        if not playlist:
            return {'error': 'Playlist not found'}, 404
        
        song = Song.query.get(song_id)
        if not song:
            return {'error': 'Song not found'}, 404

        playlist.songs.append(song)
        db.session.commit()

        return song, 201
        
    def delete(self, id, song_id):
        playlist = Playlist.query.get(id)
        if not playlist:
            return {'error': 'Playlist not found'}, 404
        
        song = None 
        for s in playlist.songs:
            if s.id == song_id:
                song = s
        if song:
            playlist.songs.remove(song)
            db.session.commit()
            return {"message": "Song deleted"}, 204
        else:
            return {"message": "Song not found"}, 404

#----------------------------------/playlists/-----------------------------------#
@ns_playlists.route('/playlists/')
class PlaylistsListApi(Resource):
    @ns_playlists.marshal_with(playlist_model)
    def get (self):
        playlist = Playlist.query.all()
        return playlist, 200
