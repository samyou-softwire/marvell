import datetime
from hashlib import md5
from os import getenv
from time import time_ns

from requests import get
from dotenv import load_dotenv

load_dotenv()

public_api_key = getenv("MARVEL_PUBLIC_API_KEY")
private_api_key = getenv("MARVEL_PRIVATE_API_KEY")

URL = "https://gateway.marvel.com:443/v1/public/characters/1"

# name = input("What Marvel character? ")

timestamp = str(time_ns())
hash = md5(f"{timestamp}{private_api_key}{public_api_key}".encode("utf-8")).hexdigest()
params = {
    'apikey': public_api_key,
    'ts': timestamp,
    'hash': hash
}

res = get(URL, params=params).json()
print(res)
