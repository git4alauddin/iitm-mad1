from flask_restx import Resource, Namespace
from models.user_model import User
from models.music_model import Playlist
from flask_login import current_user
from api.api_models import user_model, user_input_model, playlist_model
from decorators.role_decorator import admin_required, user_required
from extensions.extension import db

ns_users = Namespace('users')

@ns_users.route('/users/<string:id>')
class UserApi(Resource):
    @ns_users.marshal_with(user_model)
    def get(self, id):
        user = User.query.get(id)
        return user
    
    @ns_users.expect(user_input_model)
    @ns_users.marshal_with(user_model)
    def put(self,id):
        user = User.query.get(id)
        user.role = 'creator'
        db.session.commit()
        return user, 201
    
    @ns_users.marshal_with(user_model)
    def delete(self, id):
        user = User.query.get(id)
        user.role = 'user'
        db.session.commit()
        return user


@ns_users.route('/users/<string:id>/playlists')
class UserPlaylistApi(Resource):
    @ns_users.marshal_with(playlist_model)
    def get(self, id):
        playlists = Playlist.query.filter_by(user_id=id).all()
        return playlists

@ns_users.route('/users')
class UsersListApi(Resource):
    @ns_users.marshal_with(user_model)
    def get(self):
        user = User.query.all()
        return user


