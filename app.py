# imports
from flask import Flask 
from extensions.extension import api, db, bcrypt, migrate, login_manager 
from configs.config import DevelopmentConfig

# import views
from views.index_view import bp_index
from views.auth_view import bp_auth
from views.user_view import bp_user
from views.admin_view import bp_admin
from views.song_view import bp_song
from views.playlist_view import bp_playlist
from views.album_view import bp_album

# import resources
from api.user_resource import ns_users
from api.song_resource import ns_songs
from api.playlist_resource import ns_playlists
from api.album_resource import ns_albums


# initialize app
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# initialize extensions
db.init_app(app)
bcrypt.init_app(app)
api.init_app(app)
migrate.init_app(app, db)

login_manager.init_app(app)
login_manager.login_view = 'index.home'
login_manager.login_message_category = 'info'

# register blueprints
app.register_blueprint(bp_index)
app.register_blueprint(bp_auth)
app.register_blueprint(bp_user)
app.register_blueprint(bp_admin)
app.register_blueprint(bp_song)
app.register_blueprint(bp_playlist)
app.register_blueprint(bp_album)

# register namespaces
api.add_namespace(ns_users)
api.add_namespace(ns_songs)
api.add_namespace(ns_playlists)
api.add_namespace(ns_albums)


if __name__ == '__main__':
    app.run(debug=True)