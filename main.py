import os
from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

CLIENT_ID = os.environ['Client_id']
CLIENT_SECRET = os.environ['Client_secret']



sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri='https://example.com/callback',
        scope="playlist-modify-private",
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]


date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")


soup = bs(response.text, 'html.parser')
song_names_spans = soup.find_all(name="h3", class_="a-no-trucate")
songs_list = [songs.getText().strip() for songs in song_names_spans]
print(songs_list)
artist_names_spans = soup.find_all(name="span", class_="a-no-trucate")
artists_list = [artist.getText().strip() for artist in artist_names_spans]
songs_and_artists=dict(zip(songs_list,artists_list))
#print(artists_list)
for n in range(len(songs_list)):
    pprint(f"{n}. {songs_list[n]} by {artists_list[n]}")

song_uris=[]
year = date.split("-")[0]
for songs in range(len(songs_list)):
    print(f"songs: {songs_list[songs]} artists: {artists_list[songs]}")
    result = sp.search(q=f"track:{songs_list[songs]} artist:{artists_list[songs]}",type ="track")
    try:
        uri=result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{songs_list[songs]} doesn't exist in Spotify, Skipped.")

print(song_uris)
playlist=sp.user_playlist_create(user_id,name=f"{date} Billboard 100",public=False,description="Musical Time Machine")
print(playlist)
sp.playlist_add_items(playlist_id=playlist['id'],items=song_uris)