from flask import Blueprint, render_template, request
from flask.views import MethodView

from decorators.contents import admin_stats, admin_stats_visuals
from decorators.role_decorator import admin_required

from models.music_model import Song
from sqlalchemy import or_
'''
+--------------------------------------------------------------+
|                         blueprint admin                      |
+--------------------------------------------------------------+
'''
bp_admin = Blueprint('admin', __name__)

#------------------------------------admin_visuals---------------------------------#
class AdminVisualsView(MethodView):
    @admin_required
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
    @admin_required
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