import os
import spotipy
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URI = os.environ.get("REDIRECT_URI")

date = input("Which year do you want to travel to ? Type the date in this format YYYY-MM-DD : ")
URL = f"https://www.billboard.com/charts/hot-100/{date}"
repsonse = requests.get(URL)
repsonse.raise_for_status()
html_file = repsonse.text

soup = BeautifulSoup(html_file, 'html.parser')

# :param limit: Stop looking after finding this many results.

titles = soup.find_all(name="h3", class_="a-no-trucate", limit=100)

songs = [song.getText().strip() for song in titles]

sp = spotipy.Spotify(
    auth_manager= SpotifyOAuth(
        client_id= CLIENT_ID,
        client_secret= CLIENT_SECRET,
        redirect_uri= REDIRECT_URI,
        scope=  "playlist-modify-private",
        show_dialog=True,
        cache_path= "token.txt"
    )
)

# current_user = sp.current_user()
# print(current_user)
# {'display_name': 'user_name', 
# 'external_urls': {'spotify': 'https://open.spotify.com/user/31jf5peoatbxn3yci6taxdnas3xm'}, 
# 'href': 'https://api.spotify.com/v1/users/31jf5peoatbxn3yci6taxdnas3xm', 
# 'id': '31dkcdk7sfux4d7uqngwvnisqitq', 
# 'images': [], 
# 'type': 'user', 
# 'uri': 'spotify:user:31dkcdk7sfux4d7uqngwvnisqitq', 
# 'followers': {'href': None, 'total': 0}  }

user_id = sp.current_user()["id"]

song_uris = []
year = date.split("-")[0]
for song in songs:
    
    search_result = sp.search(q=f"track:{song} year:{year}", type="track")
    # print(search_result)
    try :
        uri = search_result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print("Song Not Found. Skipped")
# print(song_uris)

playlist = sp.user_playlist_create(user= user_id,name=f"{date} Billboard 100",public=False)
playlist_id = playlist["id"]
# print(playlist_id)
# print(song_uris)

# sp.playlist_add_items(playlist_id=playlist_id, items=song_uris)
sp.user_playlist_add_tracks(
    user= user_id,
    playlist_id= playlist_id,
    tracks= song_uris
)