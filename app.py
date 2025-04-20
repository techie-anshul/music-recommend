# app.py

import streamlit as st
from data_loader import load_all_data
from eda import compute_summaries
from models import train_svd_model
from recommend import *

st.set_page_config(page_title="Techno Event Recommender", layout="wide")
st.title("🎧 Techno Music Event Recommender")

data = load_all_data()
summaries = compute_summaries(data)

st.subheader("📊 Data Insights")
for k, v in summaries.items():
    st.write(f"**{k}**")
    st.dataframe(v)

st.subheader("🧠 Training SVD Model...")
svd_model, predictions, rmse = train_svd_model(data["event_history"])
st.success(f"✅ SVD RMSE: {rmse:.4f}")

st.subheader("🎯 Generate Recommendations")

user_id = st.selectbox("Choose User ID", data["users"]["Id"].unique())
if st.button("Get Recommendations"):
    user_event_matrix = data["event_history"].pivot(index="UserId", columns="EventId", values="Rate").fillna(0)
    content_matrix = build_content_matrix(data["events"], data["genres"])
    similarity_df = get_event_similarity_matrix(content_matrix)
    
    top_recs = hybrid_recommend(user_id, svd_model, user_event_matrix, similarity_df, data["events"], top_n=5)
    st.markdown("### 🎵 Top 5 Events for You:")
    for eid, score in top_recs:
        name = data["events"].query("Id == @eid")["Name"].values[0]
        st.write(f"- {name} (Score: {score:.2f})")
