import streamlit as st
import pandas as pd
from src import model

st.title("🎬 Movie Success Predictor")

st.markdown("### Enter Movie Details")

genre = st.selectbox("Genre", ['Action', 'Comedy', 'Drama', 'Thriller', 'Horror', 'Romance', 'Sci-Fi', 'Fantasy'])
budget = st.slider("Budget (in million $)", 1, 300, 50)
director_score = st.slider("Director Score (0–10)", 0.0, 10.0, 5.0)
runtime = st.slider("Runtime (in minutes)", 80, 180, 120)
cast_popularity = st.slider("Cast Popularity (0–100)", 0.0, 100.0, 50.0)
release_month = st.slider("Release Month", 1, 12, 6)
marketing_spend = st.slider("Marketing Spend (in million $)", 1, 100, 10)
is_sequel = st.selectbox("Is it a Sequel?", [0, 1])

input_dict = {
    'genre': genre,
    'budget_million': budget,
    'director_score': director_score,
    'runtime_minutes': runtime,
    'cast_popularity': cast_popularity,
    'release_month': release_month,
    'marketing_spend': marketing_spend,
    'is_sequel': is_sequel,
    'box_office_hit': 0,
    'movie_id': 1,
    'title': 'Test Movie'
}

if st.button("Predict Success"):
    model.train_model(pd.read_csv("data/movies_100k.csv"))
    result = model.predict_single(pd.DataFrame([input_dict]))
    label = "🎉 Hit!" if result['prediction'][0] == 1 else "❌ Flop"
    st.success(f"Prediction: {label}")