from flask import Blueprint, render_template,redirect,url_for,flash,request
from flask.views import MethodView
import requests
from extensions.extension import db
from models.music_model import Song,Album,Playlist,FlaggedContent
from models.user_model import User
from sqlalchemy import or_
from decorators.contents import admin_stats, user_contents, admin_stats_visuals

# --------------------------------------blueprint admin--------------------------------------------------------
bp_admin = Blueprint('admin', __name__)

# view admin_visuals
class AdminVisualsView(MethodView):
    def get(self):
        # stats
        stats_data, labels, values = admin_stats_visuals()

        genres = ['romantic', 'pop', 'hip-hop', 'rock']
        genre_counts = [0, 0, 0, 0]
        for song in Song.query.all():
            for i, genre in enumerate(genres):
                if song.genre == genre:
                    genre_counts[i] += 1
        
        return render_template('admin_visuals.html', labels=labels, values=values, stats_data=stats_data, genre_counts=genre_counts, genres=genres)
bp_admin.add_url_rule('/admin_visuals', view_func=AdminVisualsView.as_view('admin_visuals'))


class AdminSearchView(MethodView):
    def get(self):
      
        query = request.args.get('query')
        query = f"%{query}%"
    
        songs = Song.query.filter(
                or_(
                    Song.title.contains(query),
                    Song.artist.contains(query),
                    Song.genre.contains(query)
                )
            ).all()
        
        # stats
        stats_data = admin_stats()

        return render_template('admin_search.html', songs=songs, stats_data=stats_data)
bp_admin.add_url_rule('/admin_search', view_func=AdminSearchView.as_view('admin_search'))