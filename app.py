import streamlit as st
import pandas as pd
from src import model

# Page config
st.set_page_config(page_title="Movie Success Predictor", page_icon="🎬", layout="wide")

# --- Custom CSS for aesthetics ---
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        color: #f1f5f9;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    .block-container {
        padding: 2rem 3rem;
        border-radius: 12px;
        background: rgba(255,255,255,0.03);
        box-shadow: 0 8px 30px rgba(2,6,23,0.6);
    }
    .card {
        background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.02));
        border-radius: 10px;
        padding: 1rem;
    }
    .metric-label {
        color: #a8c0ff;
    }
    .big-title {
        font-size:28px;
        font-weight:700;
        margin-bottom:0.2rem;
    }
    .muted {
        color: #cbd5e1;
        font-size:14px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Header ---
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("""
    <div class='big-title'>🎬 Movie Success Predictor</div>
    <div class='muted'>A compact, friendly interface to estimate whether a movie will be a box-office <strong>Hit</strong> or a <strong>Flop</strong>. Enter the details and press Predict.</div>
    """, unsafe_allow_html=True)
with col2:
    st.image("https://images.unsplash.com/photo-1517604931442-7cc7c41b3c3d?q=80&w=400&auto=format&fit=crop&s=8f3b3f93d8b4d4fa5b5e2b8d2b2b7a8c", width=140)

st.markdown("---")

# --- Main Input Card ---
with st.container():
    left, right = st.columns([2, 1])
    with left:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### Enter Movie Details", unsafe_allow_html=True)

        # nicer controls grouped
        genre = st.selectbox("🎭 Genre", ['Action', 'Comedy', 'Drama', 'Thriller', 'Horror', 'Romance', 'Sci-Fi', 'Fantasy'])

        c1, c2 = st.columns(2)
        with c1:
            budget = st.slider("💰 Budget (million $)", 1, 300, 50)
            director_score = st.slider("🎬 Director Score (0–10)", 0.0, 10.0, 5.0)
            runtime = st.slider("⏱ Runtime (minutes)", 80, 180, 120)
        with c2:
            cast_popularity = st.slider("🌟 Cast Popularity (0–100)", 0.0, 100.0, 50.0)
            release_month = st.selectbox("📅 Release Month", list(range(1,13)), index=5)
            marketing_spend = st.slider("📣 Marketing Spend (million $)", 1, 100, 10)

        is_sequel = st.radio("🔁 Is it a Sequel?", ("No", "Yes"))
        is_sequel = 1 if is_sequel == "Yes" else 0

        poster = st.file_uploader("Upload Poster (optional)", type=["png", "jpg", "jpeg"])

        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### Quick Preview", unsafe_allow_html=True)
        preview_df = pd.DataFrame([{
            'Genre': genre,
            'Budget (M$)': budget,
            'Director': director_score,
            'Runtime (min)': runtime,
            'Cast Pop': cast_popularity,
            'Release Mo.': release_month,
            'Marketing (M$)': marketing_spend,
            'Sequel': 'Yes' if is_sequel else 'No'
        }])
        st.table(preview_df)

        if poster is not None:
            st.image(poster, use_column_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

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

# --- Predict button and action ---
col_a, col_b, col_c = st.columns([1, 1, 2])
with col_b:
    predict_btn = st.button("Predict Success", key="predict")

if predict_btn:
    with st.spinner("Running model and making prediction..."):
        try:
            # try to train/load dataset (kept as original behavior but cached in model module would be better)
            try:
                model.train_model(pd.read_csv("data/movies_100k.csv"))
            except FileNotFoundError:
                # If dataset isn't available, try to call a model loader
                if hasattr(model, 'load_model'):
                    model.load_model()
                else:
                    st.warning("Training data not found and model.load_model() not available. Prediction may fail.")

            df_input = pd.DataFrame([input_dict])
            result = model.predict_single(df_input)

            pred = int(result['prediction'][0]) if ('prediction' in result and len(result['prediction'])>0) else 0
            score = float(result['score'][0]) if ('score' in result and len(result['score'])>0) else None

            if pred == 1:
                st.success("🎉 Prediction: Hit! This movie is likely to succeed at the box office.")
                if score is not None:
                    st.metric(label="Confidence", value=f"{score:.1%}")
                st.balloons()
            else:
                st.error("❌ Prediction: Flop. Consider revising budget, marketing or casting choices.")
                if score is not None:
                    st.metric(label="Confidence", value=f"{score:.1%}")

        except Exception as e:
            st.exception(e)

# --- Extra information and tips ---
with st.expander("Model details & UX tips", expanded=False):
    st.markdown(
        "- The model uses features like genre, budget, director score, runtime, cast popularity, release month, marketing spend and sequel status.\n"
        "- For better predictions: increase marketing spend, attach a popular cast, or release in high-attendance months.\n"
        "- If you want persistent models and faster responses, place trained model artifacts under `src/model_artifacts/` and expose a `load_model()` in `src.model`."
    )

st.markdown("<div class='muted' style='text-align:center;margin-top:1.2rem;'>Made with ❤️ — tweak the CSS above to match your brand.</div>", unsafe_allow_html=True)
