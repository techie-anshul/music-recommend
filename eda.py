# eda.py

def compute_summaries(data):
    events_df = data["events"]
    users_df = data["users"]
    locations_df = data["locations"]
    countries_df = data["countries"]
    genres_df = data["genres"]
    artists_df = data["artists"]

    # Map genre names
    genre_map = genres_df.set_index("Id")["Name"].to_dict()
    events_df["GenreName"] = events_df["GenreId"].map(genre_map)
    artists_df["GenreName"] = artists_df["GenreId"].map(genre_map)

    # Merge country names
    locations_df = locations_df.merge(countries_df, left_on="CountryId", right_on="Id", suffixes=("_loc", "_country"))

    top_users = users_df["UserName"].value_counts().head(5)
    top_event_cities = events_df["LocationId"].map(locations_df.set_index("Id_loc")["Name_loc"]).value_counts().head(5)
    top_event_genres = events_df["GenreName"].value_counts().head(5)
    top_artist_genres = artists_df["GenreName"].value_counts().head(5)

    return {
        "Top Users": top_users,
        "Top Cities by Event Count": top_event_cities,
        "Top Event Genres": top_event_genres,
        "Top Artist Genres": top_artist_genres,
    }
