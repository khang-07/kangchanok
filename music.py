import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

scope = "user-library-read user-follow-read user-top-read user-read-recently-played playlist-read-private streaming app-remote-control ugc-image-upload"

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# this will overwrite each time so it doesn't overflow
async def get_liked(): 
    liked = {"liked" : []}
    results = spotify.current_user_saved_tracks()
    for i, item in enumerate(results["items"]):
        track = item["track"]
        info = {
            "index" : i,
            "artist" : track["artists"][0]["name"],
            "track" : track["name"]
        }
        liked["liked"].append(info)
    with open("data.json", "w") as write_file:
        write_file.write(json.dumps(liked, indent=4))

async def all_playlists():
    all = {"playlists" : []}
    playlists = spotify.user_playlists("ienjrf2ebr0884kdsmstnypkd")
    for i, playlist in enumerate(playlists["items"]):
        all["playlists"].append(playlist["name"])
    if playlists["next"]:
        playlists = spotify.next(playlists)
    else:
        playlists = None
    with open("data.json", "w") as write_file:
        write_file.write(json.dumps(all, indent=4))

async def get_playlist(name):
    songs = {"songs" : []}
    id = ""
    playlists = spotify.user_playlists("ienjrf2ebr0884kdsmstnypkd")
    
    for i, playlist in enumerate(playlists["items"]):
        if(playlist["name"] == name):
            id = playlist["id"]
    if playlists["next"]:
        playlists = spotify.next(playlists)
    else:
        playlists = None

    data = spotify.playlist(id)
    for i, item in enumerate(data["tracks"]["items"]):
        songs["songs"].append(item["track"]["name"])
    print(json.dumps(songs, indent=4, sort_keys=True))
    with open("data.json", "w") as write_file:
        write_file.write(json.dumps(songs, indent=4))