import json
import pandas as pd

RAW_FILE = "data/raw/anime_raw.json"
OUT_DIR = "data/processed/"

with open(RAW_FILE, encoding="utf-8") as f:
    raw = json.load(f)

anime_rows = []
anime_genre_rows = []
anime_studio_rows = []
studio_rows = {}
genre_lookup = {}

seen_ids = set()
unique_anime = []

for a in raw:
    anime_id = a["mal_id"]
    if anime_id not in seen_ids:
        seen_ids.add(anime_id)
        unique_anime.append(a)
    else:
        print(f"⚠️  Duplicate found: {anime_id} - {a.get('title', 'Unknown')}")

print(f"Original: {len(raw)} anime")
print(f"Unique: {len(unique_anime)} anime")
print(f"Duplicates removed: {len(raw) - len(unique_anime)}")

def format_pg_array(titles_list):
    if not titles_list:
        return None

    filtered = []
    for title in titles_list:
        if title and title.strip():
            if cleaned := title.strip().strip(',').strip():
                filtered.append(cleaned)
    
    if not filtered:
        return None

    escaped = []
    for title in filtered:        
        title = (title
                 .replace('\\', '\\\\')
                 .replace('"', '\\"')
                 .replace('{', '\\{')
                 .replace('}', '\\}')
                )
        escaped.append(title)
    
    return '{' + ','.join(escaped) + '}'
      
for a in unique_anime:
    anime_id = a["mal_id"]
    alt_titles = [title["title"] for title in a["titles"] if title["type"] != "Default"]
    
    anime_rows.append({
        "anime_id": anime_id,
        "title": a["title"],
        "alternative_titles": format_pg_array(alt_titles),
        "synopsis": a["synopsis"],
        "year": a["year"],
        "type": a["type"],
        "rating": a["rating"],
        "episodes": a["episodes"],
        "score": a["score"],
        "rank": a["rank"],
        "popularity": a["popularity"],
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
        studio_id = s["mal_id"]
        studio_name = s["name"]

        if studio_id not in studio_rows:
            studio_rows[studio_id] = studio_name

        anime_studio_rows.append({
            "anime_id": anime_id, 
            "studio_id": studio_id,
        })

anime_df = pd.DataFrame(anime_rows)

int_columns = ['year', 'episodes', 'rank', 'popularity', 'members', 'favorites']

for col in int_columns:
    if col in anime_df.columns:
        anime_df[col] = anime_df[col].astype('Int64')

anime_genres_df = pd.DataFrame(anime_genre_rows)
anime_studios_df = pd.DataFrame(anime_studio_rows)

studios_df = pd.DataFrame([
    {"studio_id": k, "name": v} for k, v in studio_rows.items()
])

genres_df = pd.DataFrame([
    {"genre_id": k, "name": v} for k, v in genre_lookup.items()
])

anime_df.to_csv(f"{OUT_DIR}anime.csv", index=False)
anime_genres_df.to_csv(f"{OUT_DIR}anime_genres.csv", index=False)
anime_studios_df.to_csv(f"{OUT_DIR}anime_studios.csv", index=False)
studios_df.to_csv(f"{OUT_DIR}studios.csv", index=False)
genres_df.to_csv(f"{OUT_DIR}genres.csv", index=False)

print("...CSV files generated...")
