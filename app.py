import spotipy as sp
from spotipy.oauth2 import SpotifyClientCredentials

def app(artist):
    client_id=''
    client_secret=''
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_id)
    api = sp.Spotify(client_credentials_manager=client_credentials_manager)

    artist_search = api.search(q=f'artist:{artist}', type='artist')
    artist_uri = artist_search['artists']['items'][0]['uri']

    for i in range(10):
        print(api.artist_top_tracks(artist_uri)['tracks'][i]['name'])


if __name__ == '__main__':
    app('frank ocean')
