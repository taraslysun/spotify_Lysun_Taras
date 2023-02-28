from dotenv import load_dotenv
import os
import base64
import json
from requests import post, get

load_dotenv()

client_id = os.getenv('CLIENT-ID')
client_secret = os.getenv('CLIENT-SECRET')

def get_token():

    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {

    "Authorization": "Basic "+ auth_base64,

    "Content-Type": "application/x-www-form-urlencoded" }

    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]

    return token


def get_auth_header(token):
    return {'Authorization': 'Bearer '+token}

def search_for_artist(token, artist_name):
    url = 'https://api.spotify.com/v1/search'
    headers = get_auth_header(token)
    query = f'?q={artist_name}&type=artist&limit=1'

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)['artists']['items']
    if not json_result:
        print('No artists found')
        return None
    return json_result[0]


def get_songs_by_artists(token, artist_id):
    url = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US'
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)['tracks']
    return json_result


def song_by_id(token, song_id):
    url = f'https://api.spotify.com/v1/tracks/{song_id}'
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

token = get_token()
artist_name = input('Enter artist name: ')
result = search_for_artist(token, artist_name)
artist_id = result['id']
songs = get_songs_by_artists(token, artist_id)
artist_info = {'name': result['name'],
               'most popular song': songs[0]['name'],
               'artist_id': artist_id,
               'Country of most popular song': song_by_id(token, songs[0]['id'])['available_markets'],
               'top 10 songs': [str(idx+1)+'. '+song['name'] for idx,song in enumerate(songs)]
               }


for idx, information in enumerate(artist_info):
    print(f"{idx+1}. {information}")
art_inf = input('Enter what you want to know about artist: ')
info_index = int(art_inf) - 1
print(list(artist_info.values())[info_index])
