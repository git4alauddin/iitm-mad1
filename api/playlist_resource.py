from flask_restx import Namespace, Resource
from models.music_model import Playlist, Song
from flask import request, redirect, url_for, flash, render_template
from flask_login import current_user
from extensions.extension import db
from api.api_models import playlist_model

ns_playlist = Namespace('playlist')

@ns_playlist.route('/playlists/<string:user_id>')
class PlaylistApi(Resource):
    @ns_playlist.marshal_with(playlist_model)
    def get (self, user_id):
        playlist = Playlist.query.filter_by(user_id=user_id).all()
        return playlist


