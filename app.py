import streamlit as st
import pandas as pd
from src import model
import streamlit.components.v1 as components

# Page config
st.set_page_config(page_title="Moviegrad — Movie Success Predictor", page_icon="🎬", layout="wide")

# Path to the provided logo (uploaded to the environment)
LOGO_PATH = "logo.jpeg"

# Theme colors derived from the logo: teal/cyan and gold on deep navy
PRIMARY_CYAN = "#18B6C9"
SECONDARY_DEEP = "#062033"
GOLD = "#F0B84A"
MUTED = "#A9CBDC"
CARD_BG = "rgba(255,255,255,0.03)"

# Lottie animation URL (keeps subtle motion)
LOTTIE_URL = "https://assets10.lottiefiles.com/packages/lf20_touohxv0.json"

# --- CSS: centered layout, colors from logo, rounded poster card ---
st.markdown(f"""
    <style>
    :root{{--primary:{PRIMARY_CYAN};--gold:{GOLD};--deep:{SECONDARY_DEEP};--muted:{MUTED};}}
    .stApp{{background: radial-gradient(circle at 10% 10%, #031018 0%, #071e2d 40%, #0b2633 100%); color: #eaf6fb; font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;}}
    .center-container{{max-width:980px;margin:0 auto;border-radius:14px;padding:1.6rem;background:linear-gradient(180deg, rgba(255,255,255,0.01), rgba(255,255,255,0.00));box-shadow:0 16px 50px rgba(3,6,20,0.7);border:1px solid rgba(255,255,255,0.02);}}
    .header{{display:flex;align-items:center;gap:18px;justify-content:center;margin-bottom:6px}}
    .logo-img{{height:86px;border-radius:12px;box-shadow:0 8px 24px rgba(0,0,0,0.6);}}
    .title{{font-size:30px;font-weight:800;margin:0;color:var(--primary);letter-spacing:0.2px}}
    .subtitle{{color:var(--muted);margin-top:2px;text-align:center}}
    .input-card{{background:{CARD_BG};padding:1.1rem;border-radius:12px;margin-top:12px;border:1px solid rgba(255,255,255,0.02)}}
    .preview-card{{background:linear-gradient(180deg, rgba(255,255,255,0.015), rgba(255,255,255,0.01));padding:0.8rem;border-radius:12px}}
    .poster{{border-radius:12px;box-shadow:0 8px 30px rgba(2,6,23,0.6);}}
    .result-badge{{padding:10px 16px;border-radius:999px;font-weight:700}}
    .hit{{background:linear-gradient(90deg,var(--primary),#3bd0c7);color:#001918}}
    .flop{{background:linear-gradient(90deg,#3a3f4b,#1c2732);color:#f2f6f8}}
    .stButton>button{{border-radius:10px;padding:10px 20px;border:none;background:linear-gradient(90deg,var(--primary),#2fb6c1);box-shadow:0 8px 20px rgba(24,182,201,0.12)}}
    .footer{{color:var(--muted);text-align:center;margin-top:14px;font-size:13px}}
    </style>
""", unsafe_allow_html=True)

# --- Central wrapper ---
st.markdown("<div class='center-container'>", unsafe_allow_html=True)

# Header with logo and title centered
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.markdown("<div class='header'>", unsafe_allow_html=True)
    st.image(LOGO_PATH, width=86, caption=None, clamp=False)
    st.markdown("""
        <div style='text-align:left'>
            <div class='title'>Moviegrad</div>
            <div class='subtitle'>SUCCESS PREDICTOR — Predict box-office hits with confidence</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Lottie animation beneath header for motion and charm
components.html(f"""
    <div style='display:flex;justify-content:center;margin-top:6px;margin-bottom:10px;'>
      <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
      <lottie-player src=\"{LOTTIE_URL}\" background=\"transparent\" speed=\"0.9\" style=\"width:160px;height:160px;\" loop autoplay></lottie-player>
    </div>
""", height=200)

# Main content: inputs centered
with st.container():
    left_col, mid_col, right_col = st.columns([1,2,1])

    with mid_col:
        st.markdown("<div class='input-card'>", unsafe_allow_html=True)
        st.markdown("### Enter Movie Details")

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
            predict_btn = st.button("Predict Success", key="predict_with_logo")

        # Preview and result area
        st.markdown("<div class='preview-card' style='margin-top:14px'>", unsafe_allow_html=True)
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

        # Poster preview as rounded card
        if poster is not None:
            st.image(poster, use_column_width=True, output_format='auto')
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

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

# Prediction logic with themed result badges
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

            # Themed result display
            if pred == 1:
                st.markdown(f"<div style='text-align:center;margin-top:12px'><span class='result-badge hit'>🎉 HIT</span></div>", unsafe_allow_html=True)
                if score is not None:
                    st.metric(label="Confidence", value=f"{score:.1%}")
                st.balloons()
            else:
                st.markdown(f"<div style='text-align:center;margin-top:12px'><span class='result-badge flop'>❌ FLOP</span></div>", unsafe_allow_html=True)
                if score is not None:
                    st.metric(label="Confidence", value=f"{score:.1%}")

        except Exception as e:
            st.exception(e)

# Footer
st.markdown(f"<div class='footer'>Made with ❤️  </code></div>", unsafe_allow_html=True)

