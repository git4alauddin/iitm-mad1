from models.music_model import Album, Song, Playlist
from models.user_model import User
from flask import request
from flask_login import current_user
from extensions.extension import db
import requests

def admin_stats():
    tot_user = User.query.filter_by(role='user').count()
    tot_creator = User.query.filter_by(role='creator').count()
    tot_album = Album.query.count()
    tot_song = Song.query.count()
    tot_playlist = Playlist.query.count()

    stats_headings = ['Total Normal Users', 'Total Creators', 'Total Albums', 'Total Songs', 'Total Playlists']
    stats_data = [{'heading': h, 'total': t} for h, t in zip(stats_headings, [tot_user, tot_creator, tot_album, tot_song, tot_playlist])]
    return stats_data

def admin_stats_visuals():
    tot_user = User.query.filter_by(role='user').count()
    tot_creator = User.query.filter_by(role='creator').count()
    tot_album = Album.query.count()
    tot_song = Song.query.count()
    tot_playlist = Playlist.query.count()

    stats_headings = ['Total Normal Users', 'Total Creators', 'Total Albums', 'Total Songs', 'Total Playlists']
    stats_data = [{'heading': h, 'total': t} for h, t in zip(stats_headings, [tot_user, tot_creator, tot_album, tot_song, tot_playlist])]

    labels = ['Total Normal Users', 'Total Creators', 'Total Albums', 'Total Songs', 'Total Playlists']
    values = [tot_user, tot_creator, tot_album, tot_song, tot_playlist]

    return stats_data, labels, values

def user_contents():
    suggested_songs = Song.query.order_by(db.func.random()).limit(4).all()
    api_url = request.url_root + 'users/users/' + str(current_user.id) + '/playlists'
    p_response = requests.get(api_url)
    api_url = request.url_root + 'users/users/' + str(current_user.id) + '/albums'
    a_response = requests.get(api_url)
    if p_response.status_code == 200:
                playlists = p_response.json()
    if a_response.status_code == 200:
        albums = a_response.json()

    return suggested_songs, playlists, albums