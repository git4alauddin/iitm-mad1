from extensions.extension import db
from datetime import datetime
import uuid

# form defaults
def generate_uuid():
    return str(uuid.uuid4())

# songs
class Song(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid, unique=True)
    title = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    lyrics = db.Column(db.Text)
    genre = db.Column(db.String(50))
    rating = db.Column(db.Float, default=0)
    hits = db.Column(db.Integer, default=0)
    creator_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)

# song_files
class SongFile(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid, unique=True)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)

# albums
class Album(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid, unique=True)
    title = db.Column(db.String(100), nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    hits = db.Column(db.Integer, default=0)
    songs = db.relationship('Song', secondary='album_songs', backref='albums')

album_songs = db.Table('album_songs',
    db.Column('album_id', db.String(36), db.ForeignKey('album.id'), primary_key=True),
    db.Column('song_id', db.String(36), db.ForeignKey('song.id'), primary_key=True)
)

# playlists
class Playlist(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid, unique=True)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    hits = db.Column(db.Integer, default=0)
    songs = db.relationship('Song', secondary='playlist_songs', backref='playlists')

playlist_songs = db.Table('playlist_songs',
    db.Column('playlist_id', db.String(36), db.ForeignKey('playlist.id'), primary_key=True),
    db.Column('song_id', db.String(36), db.ForeignKey('song.id'), 
    primary_key=True)
)

# flagged_contents
class FlaggedContent(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid, unique=True)
    song_id = db.Column(db.String(36), db.ForeignKey('song.id'), nullable=False)
    reason = db.Column(db.String(200))
    admin_id = db.Column(db.String(36), db.ForeignKey('admin.id'), nullable=False)


# subscriptions
class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subscription_type = db.Column(db.String(20), nullable=False)  # Free, Premium, etc.
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)