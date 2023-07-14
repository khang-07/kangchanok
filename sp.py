from dotenv import load_dotenv
from os import getenv
from base64 import b64encode
from requests import post, get, head
from codecs import decode
import json

load_dotenv()

client_id = "628c8d846a204d0db49a33120fe3be67"
client_secret = "8c1d7a4c6f5f491d8f8e2a93df27d6dd"
redirect_uri = "http://localhost:8888/callback"

def get_token():
    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(b64encode(auth_bytes), "utf-8")
    print(auth_base64)
    
    url = "https://accounts.spotify.com/api/token"
    my_header = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    my_data = {
        "grant_type": "client_credentials"
    }
    result = post(url, headers=my_header, data=my_data)
    return json.loads(result.content)["access_token"]
    
def get_auth_header(token):
    return {"Authorization": f"Bearer {token}"}

def search(token, name, type):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={name}&type={type}&limit=1"
    query_url = f"{url}{query}"
    result = get(query_url, headers=headers)
    a = json.loads(result.content)[f"{type}s"]["items"][0]["name"]
    print(json.dumps(a, indent=4))

def auth_user():
    scope = "user-library-read"
    url = "https://accounts.spotify.com/authorize?"
    auth_url = f"{url}response_type=code&client_id={client_id}&scope={scope}&redirect_uri={redirect_uri}"
    result = get(auth_url, allow_redirects=True)
    print(auth_url)
    print(decode(result.content))
    print(result.history)

token = get_token()
search(token, "bygone days", "track")
search(token, "joe hisaishi", "artist")
auth_user()