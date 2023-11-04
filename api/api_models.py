from extensions.extension import api 
from flask_restx import fields

#-----------------------user---------------#
user_model = api.model("User", {
    "id": fields.String,
    "username": fields.String,
    "role": fields.String
})

user_input_model = api.model("UserInput", {
    "id": fields.String(required=True, description="User ID")
})

#-----------------------song---------------#
song_model = api.model("Song", {
    "id": fields.String,
    "creator_id": fields.String,
    "title": fields.String,
    "artist": fields.String
})


#-----------------------playlist---------------#
playlist_model = api.model("Playlist", {
    "id": fields.String,
    "title": fields.String,
    "user_id": fields.String
})

playlist_input_model = api.model("PlaylistInput", {
    "id": fields.String,
    "title": fields.String
})

#-----------------------album---------------#
album_model = api.model("Album", {
    "id": fields.String,
    "title": fields.String,
    "user_id": fields.String
})

album_input_model = api.model("AlbumInput", {
    "id": fields.String,
    "title": fields.String,
    "release_year": fields.Integer
})