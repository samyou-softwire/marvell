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

PAGE_SIZE = 20

while True:
    timestamp = str(time_ns())
    key_hash = md5(f"{timestamp}{PRIVATE_API_KEY}{PUBLIC_API_KEY}".encode("utf-8")).hexdigest()
    default_params = {
        'apikey': PUBLIC_API_KEY,
        'ts': timestamp,
        'hash': key_hash,
    }

    name = input("What Marvel character? ")

    keep_searching = True
    ID = None
    offset = 0

    while keep_searching:

        print("Trying to find that character . . .")

        search_params = {
            **default_params,
            'nameStartsWith': name,
            'limit': PAGE_SIZE,
            'offset': offset
        }

        res = get(SEARCH_URL, search_params).json()

        # refer to https://developer.marvel.com/docs#!/public/getCreatorCollection_get_0 for data shape

        data = res['data']
        total = data['total']
        offset = data['offset']

        characters = data['results']

        if total == 0:
            print("Couldn't find any characters by this name...")
            keep_searching = False
        elif total == 1:
            ID = characters[0]['id']
            keep_searching = False
        else:
            IDs = []
            i = 0
            print(f"Please select a character)")
            for character in characters:
                i += 1
                print(f"- {i}: {character['name']}")
                IDs.append(character['id'])

            choice = input(f"Which ID? (1-{len(characters)}), or 'n' for next page ")

            if choice == "n":
                if offset + PAGE_SIZE >= total:
                    print("There are no more pages...")
                    keep_searching = False
                else:
                    offset += PAGE_SIZE
            else:
                index = int(choice) - 1
                ID = IDs[index]
                keep_searching = False
                found_a_character = True

    if ID:  # if any previous branch resulted in a result
        print("Retrieving details . . .")

        res = get(DETAILS_URL.format(id=ID), params=default_params).json()

        character = res['data']['results'][0]  # should only be one returned

        print(f"Name: {character['name']}")
        print(f"Bio: {character['description']}")

