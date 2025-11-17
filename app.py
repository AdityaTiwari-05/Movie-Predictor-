import streamlit as st
import pandas as pd
from src import model
import json

# Page config
st.set_page_config(page_title="Movie Success Predictor", page_icon="🎬", layout="wide")

# --- UI: Theme control ---
theme = st.sidebar.radio("Theme", ("Dark (default)", "High-Contrast", "Light"))

# Lottie animation URL (public) - will be embedded via HTML
LOTTIE_URL = "https://assets10.lottiefiles.com/packages/lf20_touohxv0.json"

# --- Dynamic CSS for central layout + theme variations ---
css = {
    'Dark (default)': """
    :root{--bg1:#071024;--bg2:#0b2340;--card:#0f1724;--muted:#9fb4d8;--accent:linear-gradient(90deg,#6dd5ed,#2193b0);--text:#e6eef6}
    .stApp{background:radial-gradient(circle at 10% 10%, var(--bg1) 0%, var(--bg2) 40%, #112b3c 100%);color:var(--text)}
    """,
    'High-Contrast': """
    :root{--bg1:#000000;--bg2:#0a0a0a;--card:#111111;--muted:#ffffff;--accent:linear-gradient(90deg,#ffd166,#ef476f);--text:#ffffff}
    .stApp{background:linear-gradient(180deg,var(--bg1),var(--bg2));color:var(--text)}
    """,
    'Light': """
    :root{--bg1:#f6f8fb;--bg2:#e9eef6;--card:#ffffff;--muted:#40566b;--accent:linear-gradient(90deg,#6dd5ed,#2193b0);--text:#102a43}
    .stApp{background:linear-gradient(180deg,var(--bg1),var(--bg2));color:var(--text)}
    """
}

st.markdown(
    f"""
    <style>
    {css[theme]}
    .center-container{{
        max-width:900px;width:100%;margin:0 auto;border-radius:14px;padding:1.5rem;background:rgba(255,255,255,0.02);box-shadow:0 12px 40px rgba(2,6,23,0.45);border:1px solid rgba(255,255,255,0.03);
    }}
    .header-row{{display:flex;align-items:center;gap:16px;justify-content:center;margin-bottom:10px}}
    .title{{font-size:28px;font-weight:700;margin:0}}
    .subtitle{{color:var(--muted);margin-top:4px;text-align:center}}
    .input-card{{background:var(--card);padding:1rem;border-radius:10px;margin-top:1rem}}
    .preview-card{{background:rgba(255,255,255,0.02);padding:0.8rem;border-radius:8px}}
    .footer{{color:var(--muted);text-align:center;margin-top:12px;font-size:13px}}
    .stButton>button{{border-radius:10px;padding:8px 18px;background:var(--accent);border:none}}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Central wrapper ---
st.markdown("<div class='center-container'>", unsafe_allow_html=True)

# Header with Lottie animation centered (using HTML embed)
st.markdown(
    """
    <div class='header-row'>
        <div style='text-align:center'>
            <div class='title'>🎬 Movie Success Predictor</div>
            <div class='subtitle'>Enter movie details below — subtle animation and a contrasting theme</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Embed Lottie animation using web component inside a centered div
st.components.v1.html(f"""
    <div style='display:flex;justify-content:center;margin-bottom:6px;'>
      <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
      <lottie-player src=\"{LOTTIE_URL}\" background=\"transparent\" speed=\"1\" style=\"width:220px;height:220px;\" loop autoplay></lottie-player>
    </div>
""", height=260)

# Main content: inputs centered
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

# Prediction logic (centered results)
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
st.markdown("<div class='footer'>Made with ❤️ — theme & animation added. Run with: <code>streamlit run streamlit_movie_predictor.py</code></div>", unsafe_allow_html=True)
