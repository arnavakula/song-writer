import re
import string
import json

import requests
import spotipy as sp
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyClientCredentials
from googlesearch import search

def app(artist):
    client_id=''
    client_secret=''
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    spotify = sp.Spotify(client_credentials_manager=client_credentials_manager)

    genius_access_token = ''
    genius_header = {'Authorization': f'Bearer {genius_access_token}'}

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

        #remove new lines and bracketed text (usually artist names)
        # lyrics = re.sub('\[.*?\]', '', lyrics)
        # lyrics = lyrics.lower().encode('utf-8')

        lyrics = re.sub('\\[.*?\\]', '', lyrics)
        lyrics = re.sub('\n\n', '\n', lyrics)

        # no_punc = [char for char in lyrics if char not in string.punctuation]
        # lyrics = ''.join(no_punc)

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

    




        # no_punc = [char for char in lyrics if char not in string.punctuation]

        # lyrics = ''.join(no_punc)

        # print(lyrics)

        # result = requests.get(url)
        # soup = BeautifulSoup(result.text, 'html.parser')        

        # result.close()

        # lyrics = ''

        # for tag in soup.select('div[class^="Lyrics__Container"], .song_body-lyrics p'):
        #     t = tag.get_text(strip=True, separator='\n')
        #     if t:
        #         lyrics += t

        # #remove new lines and bracketed text (usually artist names)
        # lyrics = re.sub('\n', ' ', lyrics)
        # lyrics = re.sub('\[.*?\]', '', lyrics)

        # lyrics = remove_punctuation(lyrics)

        # #lower case and unicode encoding
        # lyrics = lyrics.lower().encode('utf-8')    

         


    



if __name__ == '__main__':
    app('phoebe bridgers')
