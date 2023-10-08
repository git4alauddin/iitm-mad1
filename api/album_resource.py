from flask_restx import Namespace, Resource
from models.music_model import Album
from api.api_models import album_model


#----------------------namespace_playlists---------------#
ns_playlists = Namespace('playlists')

# api playlists_list
@ns_playlists.route('/playlists/<string:user_id>')
class PlaylistsListApi(Resource):
    @ns_playlists.marshal_with(album_model)
    def get (self, user_id):
        album = Album.query.filter_by(user_id=user_id).all()
        return album, 200