#-------------------base_config------------------#
class Config():
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    SECRET_KEY = 'my_secret_key'

# env_development
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///music-dev-db.sqlite'
    SECRET_KEY = 'my-very-secret-key'

    # song upload
    # ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg', 'flac', 'm4a', 'aac'}
    SONG_UPLOAD_FOLDER = 'static/songs'
    
# env_production
class ProductionConfig(Config):
    pass