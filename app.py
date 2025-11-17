import streamlit as st
import pandas as pd
from src import model

# Page config
st.set_page_config(page_title="Movie Success Predictor", page_icon="🎬", layout="wide")

# --- Centralized CSS for aesthetics and centering ---
st.markdown(
    """
    <style>
    :root{
        --card-bg: rgba(255,255,255,0.04);
        --accent: linear-gradient(90deg,#6dd5ed,#2193b0);
        --glass: rgba(255,255,255,0.03);
    }
    .stApp {
        background: radial-gradient(circle at 10% 10%, #071024 0%, #0b2340 40%, #112b3c 100%);
        color: #e6eef6;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2rem 1rem;
    }
    .center-container{
        max-width: 900px;
        width: 100%;
        margin: 0 auto;
        border-radius: 14px;
        padding: 1.5rem;
        background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
        box-shadow: 0 12px 40px rgba(2,6,23,0.7);
        border: 1px solid rgba(255,255,255,0.03);
    }
    .header-row{display:flex;align-items:center;gap:16px;justify-content:center;margin-bottom:10px}
    .title {font-size:28px;font-weight:700;margin:0}
    .subtitle{color:#bcd6ff;margin-top:4px;text-align:center}
    .input-card{background:var(--card-bg);padding:1rem;border-radius:10px;margin-top:1rem}
    .preview-card{background:var(--glass);padding:0.8rem;border-radius:8px}
    .centered {display:flex;align-items:center;justify-content:center}
    .footer{color:#9fb4d8;text-align:center;margin-top:12px;font-size:13px}
    .stButton>button{border-radius:10px;padding:8px 18px}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Central wrapper ---
st.markdown("<div class='center-container'>", unsafe_allow_html=True)

# Header centered
st.markdown(
    """
    <div class='header-row'>
        <div style='text-align:center'>
            <div class='title'>🎬 Movie Success Predictor</div>
            <div class='subtitle'>Enter movie details below — centered and focused UX for quick experimentation</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Main content: inputs and preview centered using columns
with st.container():
    left_col, mid_col, right_col = st.columns([1, 2, 1])

    with mid_col:
        st.markdown("<div class='input-card'>", unsafe_allow_html=True)
        st.markdown("### Movie Details (centered)")

        genre = st.selectbox("🎭 Genre", ['Action', 'Comedy', 'Drama', 'Thriller', 'Horror', 'Romance', 'Sci-Fi', 'Fantasy'])

        c1, c2 = st.columns(2)
        with c1:
            budget = st.slider("💰 Budget (M$)", 1, 300, 50)
            director_score = st.slider("🎬 Director Score (0–10)", 0.0, 10.0, 5.0)
            runtime = st.slider("⏱ Runtime (minutes)", 80, 180, 120)
        with c2:
            cast_popularity = st.slider("🌟 Cast Popularity (0–100)", 0.0, 100.0, 50.0)
            release_month = st.selectbox("📅 Release Month", list(range(1,13)), index=5)
            marketing_spend = st.slider("📣 Marketing Spend (M$)", 1, 100, 10)

        is_sequel = st.radio("🔁 Is it a Sequel?", ("No", "Yes"))
        is_sequel = 1 if is_sequel == "Yes" else 0

        poster = st.file_uploader("Upload Poster (optional)", type=["png", "jpg", "jpeg"]) 

        st.markdown("</div>", unsafe_allow_html=True)

        # Centered action
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        btn_col1, btn_col2, btn_col3 = st.columns([1,1,1])
        with btn_col2:
            predict_btn = st.button("Predict Success", key="predict_centered")

        # Preview and result
        st.markdown("<div class='preview-card' style='margin-top:12px'>", unsafe_allow_html=True)
        preview_df = pd.DataFrame([{
            'Genre': genre,
            'Budget (M$)': budget,
            'Director': director_score,
            'Runtime': runtime,
            'Cast Pop': cast_popularity,
            'Release Mo.': release_month,
            'Marketing (M$)': marketing_spend,
            'Sequel': 'Yes' if is_sequel else 'No'
        }])
        st.table(preview_df)
        if poster is not None:
            st.image(poster, use_column_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# Close central container wrapper
st.markdown("</div>", unsafe_allow_html=True)

# Hidden fields and default values
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
    'title': 'User Input Movie'
}

# Prediction logic
if predict_btn:
    with st.spinner("Predicting..."):
        try:
            try:
                model.train_model(pd.read_csv("data/movies_100k.csv"))
            except FileNotFoundError:
                if hasattr(model, 'load_model'):
                    model.load_model()
                else:
                    st.warning("Training data not found and model.load_model() not available. Prediction may fail.")

            df_input = pd.DataFrame([input_dict])
            result = model.predict_single(df_input)

            pred = int(result['prediction'][0]) if ('prediction' in result and len(result['prediction'])>0) else 0
            score = float(result['score'][0]) if ('score' in result and len(result['score'])>0) else None

            # Centered result display
            if pred == 1:
                st.markdown("<div style='text-align:center;margin-top:12px'>", unsafe_allow_html=True)
                st.success("🎉 Prediction: Hit! This movie is likely to succeed at the box office.")
                if score is not None:
                    st.metric(label="Confidence", value=f"{score:.1%}")
                st.balloons()
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div style='text-align:center;margin-top:12px'>", unsafe_allow_html=True)
                st.error("❌ Prediction: Flop. Consider revising budget, marketing or casting choices.")
                if score is not None:
                    st.metric(label="Confidence", value=f"{score:.1%}")
                st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            st.exception(e)

# Footer
st.markdown("<div class='footer'>Made with ❤️ — Aditya Tiwari,Akshat Verma,Ansh Sharma</div>", unsafe_allow_html=True)
