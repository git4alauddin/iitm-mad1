from flask_restx import Namespace, Resource
from extensions.extension import db
from models.music_model import Album
from api.api_models import album_model

ns_albums = Namespace('albums')

@ns_albums.route('/albums/<string:id>')
class AlbumApi(Resource):
    @ns_albums.marshal_with(album_model)
    def get(self, id):
        album = Album.query.get(id)
        return album, 200