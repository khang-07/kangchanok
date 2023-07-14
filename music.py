import json
import spotipy
from pprint import pprint
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials

scope = "user-library-read user-follow-read user-top-read user-read-recently-played playlist-read-private streaming app-remote-control ugc-image-upload user-read-playback-state,user-modify-playback-state"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope), client_credentials_manager=SpotifyClientCredentials())

# this will overwrite each time so it doesn't overflow
async def get_liked(): 
    liked = {"liked" : []}
    results = sp.current_user_saved_tracks()
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
    playlists = sp.user_playlists("ienjrf2ebr0884kdsmstnypkd")
    for i, playlist in enumerate(playlists["items"]):
        all["playlists"].append(playlist["name"])
    if playlists["next"]:
        playlists = sp.next(playlists)
    else:
        playlists = None
    with open("data.json", "w") as write_file:
        write_file.write(json.dumps(all, indent=4))

async def get_playlist(name):
    songs = {"songs" : []}
    id = ""
    playlists = sp.user_playlists("ienjrf2ebr0884kdsmstnypkd")
    
    for i, playlist in enumerate(playlists["items"]):
        if(playlist["name"] == name):
            id = playlist["id"]
    if playlists["next"]:
        playlists = sp.next(playlists)
    else:
        playlists = None

    data = sp.playlist(id)
    for i, item in enumerate(data["tracks"]["items"]):
        songs["songs"].append(item["track"]["name"])
    with open("data.json", "w") as write_file:
        write_file.write(json.dumps(songs, indent=4))

async def search(message_list):
    message = " ".join(map(str, message_list))
    print(message)
    result = sp.search(q=message, limit=1, type="track")
    track = result["tracks"]["items"][0]
    print("+++++++++++++++++++++++")
    print(track["name"])
    sp.start_playback(uris=[track["uri"]])
    print("———————————————————————")
    print(type(sp.currently_playing))
    # testing = json.dumps(result["tracks"]["items"][0].keys(), indent=4)
    """artist_uri = result["tracks"]["items"][0]["album"]["artists"][0]["uri"]
    top_tracks = sp.artist_top_tracks(artist_uri)["tracks"][:10]

    # first tracks :  start playing
    track_uri = (top_tracks[0]["uri"])
    sp.start_playback(uris=[track_uri])

    for track in top_tracks[1:]:
        sp.add_to_queue(uri=track["uri"])"""
