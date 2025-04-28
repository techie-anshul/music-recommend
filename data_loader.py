# data_loader.py

import pandas as pd
from config import *

def load_all_data():
    users_df = pd.read_csv(USERS_CSV)
    events_df = pd.read_csv(EVENTS_CSV)
    locations_df = pd.read_csv(LOCATIONS_CSV)
    countries_df = pd.read_csv(COUNTRIES_CSV)
    genres_df = pd.read_csv(GENRES_CSV)
    event_history_df = pd.read_csv(EVENT_HISTORY_CSV)
    favorite_artists_df = pd.read_csv(FAVORITE_ARTISTS_CSV)
    favorite_genres_df = pd.read_csv(FAVORITE_GENRES_CSV)
    event_artists_df = pd.read_csv(EVENT_ARTISTS_CSV)

    # Handle artists.csv manually
    parsed_rows = []
    with open(ARTISTS_CSV, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) >= 3:
                try:
                    artist_id = int(parts[0])
                    name = parts[1].strip('"')
                    genre_id = int(parts[2])
                    parsed_rows.append((artist_id, name, genre_id))
                except:
                    continue
    artists_df = pd.DataFrame(parsed_rows, columns=["Id", "Name", "GenreId"])

    return {
        "users": users_df,
        "events": events_df,
        "locations": locations_df,
        "countries": countries_df,
        "genres": genres_df,
        "event_history": event_history_df,
        "favorite_artists": favorite_artists_df,
        "favorite_genres": favorite_genres_df,
        "event_artists": event_artists_df,
        "artists": artists_df,
    }
