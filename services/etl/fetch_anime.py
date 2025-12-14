import requests
import time
import json

BASE_URL = "https://api.jikan.moe/v4/anime"

all_anime = []
page = 1

while True:
    # if page % 3 == 0:
    #     time.sleep(3)        
    print(f"...Adding Page {page}...")
        
    resp = requests.get(BASE_URL, params={"page": page})
    resp.raise_for_status()
    payload = resp.json()

    anime_list = payload["data"]
    
    all_anime.extend(anime_list) # essentially all_anime += anime_list
    
    print(f"[...Page {page} added!...]")
    
    if not payload["pagination"]["has_next_page"]:
        break

    page += 1
    
    time.sleep(0.5)  # to avoid too many requests

no_of_entries = len(all_anime)
print(f"Fetched {no_of_entries} anime")

filename = "anime_raw.json"

with open(filename, 'w') as f:
    json.dump(all_anime, f, indent=4)

print(f"Array successfully saved to {filename}")