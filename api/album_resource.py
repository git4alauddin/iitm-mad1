from flask_restx import Namespace, Resource
from extensions.extension import db
from models.music_model import Album
from api.api_models import album_model

#----------------------namespace_album---------------#
ns_album = Namespace('album')

# api album
@ns_album.route('/albums/<string:album_id>')
class AlbumApi(Resource):
    @ns_album.marshal_with(album_model)
    def get(self, album_id):
        album = Album.query.get(album_id)
        return album
    
    def delete(self, album_id):
        album = Album.query.get(album_id)
        db.session.delete(album)
        db.session.commit()
        return album
        


#----------------------namespace_albums---------------#
ns_albums = Namespace('albums')

# api playlists_list
@ns_albums.route('/albums/<string:user_id>')
class AlbumsListApi(Resource):
    @ns_albums.marshal_with(album_model)
    def get (self, user_id):
        album = Album.query.filter_by(user_id=user_id).all()
        return album, 200