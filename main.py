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

while True:
    timestamp = str(time_ns())
    key_hash = md5(f"{timestamp}{PRIVATE_API_KEY}{PUBLIC_API_KEY}".encode("utf-8")).hexdigest()
    default_params = {
        'apikey': PUBLIC_API_KEY,
        'ts': timestamp,
        'hash': key_hash
    }

    name = input("What Marvel character? ")

    print("trying to find that character . . .")

    search_params = {
        **default_params,
        'nameStartsWith': name
    }

    res = get(SEARCH_URL, search_params).json()

    # refer to https://developer.marvel.com/docs#!/public/getCreatorCollection_get_0 for data shape
    characters = res['data']['results']

    if len(characters) == 0:
        print("Couldn't find any characters by this name...")
    else:
        i = 0
        IDs = []
        print(f"Please select a character)")
        for character in characters:
            i += 1
            print(f"- {i}:{character['name']}")
            IDs.append(character['id'])

        index = int(input(f"Which ID? (1-{len(characters)}) ")) - 1
        id = IDs[index]

        print("Retrieving details . . .")

        res = get(DETAILS_URL.format(id=id), params=default_params).json()

        character = res['data']['results'][0]  # should only be one returned

        print(f"Name: {character['name']}")
        print(f"Bio: {character['description']}")

