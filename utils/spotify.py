import os

import spotipy
from spotipy import SpotifyClientCredentials
# from spotipy.oauth2 import SpotifyOAuth

from dotenv import load_dotenv

load_dotenv('../.env')

# print(os.getenv('SPOTIPY_CLIENT_ID'))
# print(os.environ['SPOTIPY_CLIENT_ID'])

# SPOTIPY_CLIENT_ID = '064f7f00e33f41f2ba917f2f07083867'
# SPOTIPY_CLIENT_SECRET = 'f36494cbb9914a2ab07ddb449aadbb98'
# SPOTIPY_REDIRECT_URI = 'http://localhost:9000'
#
# os.environ['SPOTIPY_CLIENT_ID'] = SPOTIPY_CLIENT_ID
# os.environ['SPOTIPY_CLIENT_SECRET'] = SPOTIPY_CLIENT_SECRET
# os.environ['SPOTIPY_REDIRECT_URI'] = SPOTIPY_REDIRECT_URI

scope = "user-library-read"

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.environ.get('SPOTIPY_CLIENT_ID'),
                                                                client_secret=os.environ.get('SPOTIPY_CLIENT_SECRET')))
# spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


def get_song_data(title, artist=None):
    # get results with only song name
    title = title.replace("$", "s")
    results = spotify.search(q='track:' + title, type='track')['tracks']['items']
    # if that doesn't work get results with song name and first artist
    if len(results) == 0:
        artist = ' ' + artist.lower().split('featuring')[0] if artist else ''
        results = spotify.search(q='track:' + title + artist, type='track')['tracks']['items']
        # if that doesn't work return None
        if len(results) == 0:
            return None, None, None
    song_data = results[0]
    artists = spotify.artists([ar['id'] for ar in song_data['artists']][:50])
    song_data['artist_popularity'] = [ar['popularity'] for ar in artists['artists']]
    artist_genres = []
    for ag in [ar['genres'] for ar in artists['artists']]:
        artist_genres += ag
    song_data['artist_genres'] = list(dict.fromkeys(artist_genres))
    audio_features = spotify.audio_features([song_data['id']])
    try:
        audio_analysis = spotify.audio_analysis(song_data['id'])
    except spotipy.SpotifyException:
        audio_analysis = None

    return song_data, audio_features[0], audio_analysis
