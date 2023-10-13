import json
import re
import string

import requests
import spotipy as sp
from bs4 import BeautifulSoup
from googlesearch import search
from spotipy.oauth2 import SpotifyClientCredentials

import ids

def app(artist):
    spotify, genius_header = init_apis()

    artist_search = spotify.search(q=f'artist:{artist}', type='artist')
    artist_uri = artist_search['artists']['items'][0]['uri']

    song_list = []
    for i in range(10):
        song_list.append(spotify.artist_top_tracks(artist_uri)['tracks'][i]['name'])

    for song in song_list:
        query = f'http://api.genius.com/search?q={artist}-{song}'

        search_req = requests.get(query, headers=genius_header)
        url = search_req.json()['response']['hits'][0]['result']['url']

        result = requests.get(url)
        content = result.content
        soup = BeautifulSoup(content, 'html.parser')
        result.close()

        lyrics = ''

        for tag in soup.select('div[class^="Lyrics__Container"], .song_body-lyrics p'):
            t = tag.get_text(strip=True, separator='\n')

            if t:
                lyrics += t

        lyrics = re.sub('\\[.*?\\]', '', lyrics)
        lyrics = re.sub('\n\n', '\n', lyrics)


        words = []
        for word in lyrics.split(' '):
            if not '\n' in word:
                words.append(word)
            else:
                phrase = word.split('\n')
                for i in range(len(phrase)-1):
                    if phrase[i] != '':
                        words.append(phrase[i])
                        words.append('\n')
                if phrase[-1] != '':
                    words.append(phrase[-1])         
        
        print(words)
         

def init_apis():
    spot_client_id=ids.SPOT_CLIENT_ID
    spot_client_secret=ids.SPOT_CLIENT_SECRET
    spot_client_credentials_manager = SpotifyClientCredentials(client_id=spot_client_id, client_secret=spot_client_secret)
    spotify = sp.Spotify(client_credentials_manager=spot_client_credentials_manager)

    genius_access_token = ids.GENIUS_ACCESS_TOKEN
    genius_header = {'Authorization': f'Bearer {genius_access_token}'}

    return spotify, genius_header

if __name__ == '__main__':
    app('phoebe bridgers')
