# data_loader.py

import pandas as pd
from config import *

def load_all_data():
    # Re-load all required CSVs including the newly uploaded ones
    users_df = pd.read_csv("C:/Users/arnav/Downloads/Compressed/archive_2/users.csv")
    events_df = pd.read_csv("C:/Users/arnav/Downloads/Compressed/archive_2/events.csv")
    locations_df = pd.read_csv("C:/Users/arnav/Downloads/Compressed/archive_2/locations.csv")
    countries_df = pd.read_csv("C:/Users/arnav/Downloads/Compressed/archive_2/countries.csv")
    genres_df = pd.read_csv("C:/Users/arnav/Downloads/Compressed/archive_2/genres.csv")
    event_history_df = pd.read_csv("C:/Users/arnav/Downloads/Compressed/archive_2/eventhistory.csv")
    favorite_artists_df = pd.read_csv("C:/Users/arnav/Downloads/Compressed/archive_2/favoriteartists.csv")
    favorite_genres_df = pd.read_csv("C:/Users/arnav/Downloads/Compressed/archive_2/favoritegenres.csv")
    event_artists_df = pd.read_csv("C:/Users/arnav/Downloads/Compressed/archive_2/eventartists.csv")

    # Handle artists.csv manually
    parsed_rows = []
    with open("C:/Users/arnav/Downloads/Compressed/archive_2/artists.csv", "r", encoding="utf-8") as f:
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
