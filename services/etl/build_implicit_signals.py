import pandas as pd

anime = pd.read_csv("data/processed/anime.csv")

signals = []

for _, row in anime.iterrows():
    anime_id = row["anime_id"]

    if pd.notna(row["popularity"]):
        signals.append({
            "anime_id": anime_id,
            "signal_type": "popularity",
            "strength": 1 / (row["popularity"] + 1)
        })

    if pd.notna(row["favorites"]):
        signals.append({
            "anime_id": anime_id,
            "signal_type": "favorites",
            "strength": row["favorites"]
        })

    if pd.notna(row["score"]):
        signals.append({
            "anime_id": anime_id,
            "signal_type": "score",
            "strength": row["score"]
        })

signals_df = pd.DataFrame(signals)
signals_df.to_csv("data/processed/implicit_interactions.csv", index=False)