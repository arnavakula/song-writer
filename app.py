import re
import string

import requests
import spotipy as sp
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyClientCredentials
from googlesearch import search

def app(artist):
    client_id='c607893d1e2f45c3aa20e15860e1237a'
    client_secret='3f4c602b7b914ca1beb0675087d63f16'
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    api = sp.Spotify(client_credentials_manager=client_credentials_manager)

    artist_search = api.search(q=f'artist:{artist}', type='artist')
    artist_uri = artist_search['artists']['items'][0]['uri']

    song_list = []
    for i in range(10):
        song_list.append(api.artist_top_tracks(artist_uri)['tracks'][i]['name'])

    for song in song_list:
        query = f'azlyrics {artist} {song}'

        search_list = []

        for j in search(query, num_results=5):
            search_list.append(j)
        
        
        if 'azlyrics' not in search_list[0]:
            raise Exception('valid url not found')

        url = search_list[0]
        result = requests.get(url)
        content = result.content
        soup = BeautifulSoup(content, 'html.parser')
        result.close()

        tag = soup.find('div', {'class': 'ringtone'}).find_next_sibling('div')
        lyrics = tag.text

        lyrics = re.sub('\\[.*?\\]', '', lyrics)
        lyrics = re.sub('\n\n', '\n', lyrics)

        no_punc = [char for char in lyrics if char not in string.punctuation]

        lyrics = ''.join(no_punc)

        print(song)

        # words = []
        # for word in lyrics.split(' '):
        #     if not '\n' in word:
        #         words.append(word)
        #     else:
        #         phrase = word.split('\n')
        #         for i in range(len(phrase)-1):
        #             if phrase[i] != '':
        #                 words.append(phrase[i])
        #                 words.append('\n')
        #         if phrase[-1] != '':
        #             words.append(phrase[-1])        

         


    



if __name__ == '__main__':
    app('frank ocean')
