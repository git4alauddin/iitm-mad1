from extensions.extension import db
from datetime import datetime
import uuid

# form defaults
def generate_uuid():
    return str(uuid.uuid4())
def generate_date():
    return datetime.utcnow()

# songs
class Song(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid, unique=True)
    title = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.Date, default=generate_date, nullable=False)
    lyrics = db.Column(db.Text)
    genre = db.Column(db.String(50))
    rating = db.Column(db.Float, default=0)
    creator_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    playlist_id = db.Column(db.String(36), db.ForeignKey('playlist.id'))
    album_id = db.Column(db.String(36), db.ForeignKey('album.id'))

# song_files
class SongFile(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid, unique=True)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)

# albums
class Album(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid, unique=True)
    title = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50))

# playlists
class Playlist(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid, unique=True)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    songs = db.relationship('Song', secondary='playlist_song_association', backref='playlists')

playlist_song_association = db.Table('playlist_song_association',
    db.Column('playlist_id', db.String(36), db.ForeignKey('playlist.id')),
    db.Column('song_id', db.String(36), db.ForeignKey('song.id'))
)

# flagged_contents
class FlaggedContent(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid, unique=True)
    song_id = db.Column(db.String(36), db.ForeignKey('song.id'), nullable=False)
    reason = db.Column(db.String(200))
    admin_id = db.Column(db.String(36), db.ForeignKey('admin.id'), nullable=False)

# user-creator_switches
class UserCreatorRelation(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid, unique=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    creator_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)

# subscriptions
class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subscription_type = db.Column(db.String(20), nullable=False)  # Free, Premium, etc.
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)




    