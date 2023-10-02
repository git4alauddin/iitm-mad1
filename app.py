# imports
from flask import Flask 
from extensions.extension import api, db, bcrypt, login_manager 
from configs.config import DevelopmentConfig

# import views
from views.index_view import bp_index
from views.auth_view import bp_auth
from views.user_view import bp_user
from views.music_view import bp_music
from views.admin_view import bp_admin

# import resources
from api.user_resource import ns_user, ns_users
from api.song_resource import ns_song, ns_songs


# initialize app
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# initialize extensions
db.init_app(app)
bcrypt.init_app(app)
api.init_app(app)

login_manager.init_app(app)
login_manager.login_view = 'index.home'

# register blueprints
app.register_blueprint(bp_index)
app.register_blueprint(bp_auth)
app.register_blueprint(bp_user)
app.register_blueprint(bp_music)
app.register_blueprint(bp_admin)

# register namespaces
api.add_namespace(ns_user)
api.add_namespace(ns_users)
api.add_namespace(ns_song)
api.add_namespace(ns_songs)


if __name__ == '__main__':
    app.run(debug=True)