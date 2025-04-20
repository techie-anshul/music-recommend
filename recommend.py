# recommend.py

from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
from collections import defaultdict

def build_content_matrix(events_df, genres_df):
    genre_map = genres_df.set_index("Id")["Name"].to_dict()
    event_genres = events_df[["Id", "GenreId"]].copy()
    event_genres["GenreName"] = event_genres["GenreId"].map(genre_map)
    genre_ohe = pd.get_dummies(event_genres["GenreName"])
    matrix = pd.concat([event_genres["Id"], genre_ohe], axis=1).set_index("Id")
    return matrix

def get_event_similarity_matrix(content_matrix):
    return pd.DataFrame(
        cosine_similarity(content_matrix),
        index=content_matrix.index,
        columns=content_matrix.index
    )

def get_similar_events(event_similarity_df, event_id, top_n=5):
    if event_id not in event_similarity_df.index:
        return []
    similar_scores = event_similarity_df.loc[event_id].sort_values(ascending=False)
    return list(similar_scores.iloc[1:top_n+1].index)

def hybrid_recommend(user_id, svd_model, user_event_matrix, event_similarity_df, events_df, top_n=5):
    # Get content score
    scores = defaultdict(float)
    if user_id in user_event_matrix.index:
        liked = user_event_matrix.loc[user_id][user_event_matrix.loc[user_id] >= 4].index.tolist()
        for eid in liked:
            for sim_id in get_similar_events(event_similarity_df, eid, top_n=3):
                scores[sim_id] += 1
        max_score = max(scores.values()) if scores else 1
        for k in scores:
            scores[k] /= max_score

    hybrid_scores = []
    for eid in events_df["Id"]:
        svd_score = svd_model.predict(user_id, eid).est if user_id else 0
        content_score = scores.get(eid, 0)
        hybrid_scores.append((eid, 0.6 * svd_score + 0.4 * content_score))

    return sorted(hybrid_scores, key=lambda x: x[1], reverse=True)[:top_n]
