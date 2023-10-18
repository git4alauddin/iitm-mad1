from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask.views import MethodView
from flask_login import current_user
from extensions.extension import db
from models.music_model import Song, Playlist

bp_album = Blueprint('album', __name__)

class CreateAlbumView(MethodView):
    def get(self):
        pass # TODO