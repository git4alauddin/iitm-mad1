from flask_restx import Namespace, Resource
from models.music_model import Playlist, Song
from flask import request, redirect, url_for, flash, render_template
from flask_login import current_user
from extensions.extension import db
from api.api_models import playlist_model

#----------------------namespace_playlist---------------#
ns_playlist = Namespace('playlist')

# api playlist
@ns_playlist.route('/playlists/<string:playlist_id>')
class PlaylistApi(Resource):
    @ns_playlist.marshal_with(playlist_model)
    def get(self, playlist_id):
        playlist = Playlist.query.get(playlist_id)
        return playlist
    
    @ns_playlist.marshal_with(playlist_model)
    def delete(self, playlist_id):
        playlist = Playlist.query.get(playlist_id)
        db.session.delete(playlist)
        db.session.commit()
        return Playlist.query.get(playlist_id), 204


#----------------------namespace_playlists---------------#
ns_playlists = Namespace('playlists')

# api playlists_list
@ns_playlists.route('/playlists/<string:user_id>')
class PlaylistsListApi(Resource):
    @ns_playlists.marshal_with(playlist_model)
    def get (self, user_id):
        playlist = Playlist.query.filter_by(user_id=user_id).all()
        return playlist, 200
