import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from bs4 import BeautifulSoup

CLIENT_ID = "9396e9ed10514693b4ff35ea60162102"
CLIENT_SECRET = "7ae9ae4749944ab39b51affa258fba58"
REDIRECT_URI = "http://example.com/"

date = input("Which year do you want to travel to ? Type the date in this format YYYY-MM-DD : ")

URL = f"https://www.billboard.com/charts/hot-100/{date}"
repsonse = requests.get(URL)
repsonse.raise_for_status()
html_file = repsonse.text

soup = BeautifulSoup(html_file, 'html.parser')

# :param limit: Stop looking after finding this many results.

# 1. Mine
titles = soup.find_all(name="h3", class_="a-no-trucate", limit=100)

# 2. Angela's
#  titles = soup.select(selector="li ul li h3")

songs = [song.getText().strip() for song in titles]
# print(songs)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope= "playlist-modify-private",
        redirect_uri= REDIRECT_URI,
        client_id= CLIENT_ID,
        client_secret= CLIENT_SECRET,
        show_dialog= True,
        cache_path= "token.txt"
    )
)
user_id = sp.current_user()["id"]
print(user_id)

# 31jf5peoatbxn3yci6taxdnas3xm
# urn = 'spotify:artist:31jf5peoatbxn3yci6taxdnas3xm'
# sp = spotipy.Spotify()

# artist = sp.artist(urn)
# print(artist)

# user = sp.user('fuck')
# print(user)
song_uris = []
year = date.split("-")[0]
for song in songs:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")