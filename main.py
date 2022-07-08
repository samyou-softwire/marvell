import datetime
from hashlib import md5
from os import getenv
from time import time_ns

from requests import get
from dotenv import load_dotenv

load_dotenv()

PUBLIC_API_KEY = getenv("MARVEL_PUBLIC_API_KEY")
PRIVATE_API_KEY = getenv("MARVEL_PRIVATE_API_KEY")

SEARCH_URL = "https://gateway.marvel.com:443/v1/public/characters"
DETAILS_URL = "https://gateway.marvel.com:443/v1/public/characters/{id}"

timestamp = str(time_ns())
key_hash = md5(f"{timestamp}{PRIVATE_API_KEY}{PUBLIC_API_KEY}".encode("utf-8")).hexdigest()
default_params = {
    'apikey': PUBLIC_API_KEY,
    'ts': timestamp,
    'hash': key_hash
}

# name = input("What Marvel character? ")
name = "Spider-Man"

print("trying to find that character . . .")

search_params = {
    **default_params,
    'nameStartsWith': name
}

res = get(SEARCH_URL, search_params).json()

print(res['data']['results'][0]['name'])
