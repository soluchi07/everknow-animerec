import json
import pandas as pd

RAW_FILE = "data/raw/anime_raw.json"
OUT_DIR = "data/processed/"

with open(RAW_FILE, encoding="utf-8") as f:
    raw = json.load(f)

anime_rows = []
anime_genre_rows = []
studio_rows = {}
genre_lookup = {}

for a in raw:
    anime_id = a["mal_id"]

    anime_rows.append({
        "anime_id": anime_id,
        "title": a["title"],
        "alternative_titles": [title["title"] for title in a["titles"] if title["type"] != "Default"],
        "synopsis": a["synopsis"],
        "year": a["year"],
        "type": a["type"],
        "rating": a["rating"],
        "episodes": a["episodes"],
        "score": a["score"],
        "rank": a["rank"],
        "popularity": a["popularity"],
        "studio_id": a["studios"][0]["mal_id"] if a["studios"] else "",
        "members": a["members"],
        "favorites": a["favorites"]
    })
    
    for g in a["genres"]:
        genre_id = g["mal_id"]
        genre_name = g["name"]

        if genre_id not in genre_lookup:
            genre_lookup[genre_id] = genre_name

        anime_genre_rows.append({
            "anime_id": anime_id, 
            "genre_id": genre_id,
        })
    
    for s in a["studios"]:
        studio_rows[s["mal_id"]] = s["name"]

anime_df = pd.DataFrame(anime_rows)
anime_genres_df = pd.DataFrame(anime_genre_rows)

studios_df = pd.DataFrame([
    {"studio_id": k, "name": v} for k, v in studio_rows.items()
])

genres_df = pd.DataFrame([
    {"genre_id": k, "name": v} for k, v in genre_lookup.items()
])

anime_df.to_csv(f"{OUT_DIR}anime.csv", index=False)
anime_genres_df.to_csv(f"{OUT_DIR}anime_genres.csv", index=False)
studios_df.to_csv(f"{OUT_DIR}studios.csv", index=False)
genres_df.to_csv(f"{OUT_DIR}genres.csv", index=False)
