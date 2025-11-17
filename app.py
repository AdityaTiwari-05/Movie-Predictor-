import os
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from src import model

# ---------------- Config ----------------
st.set_page_config(page_title="Moviegrad — Movie Success Predictor",
                   page_icon="🎬", layout="wide")

# Default path (change if you store somewhere else)
LOGO_PATH = "logo.jpeg"

# Lottie animation (cinematic/clapboard style)
LOTTIE_URL = "https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json"

# Theme / palette (kept from your logo style)
PRIMARY_CYAN = "#18B6C9"
SECONDARY_DEEP = "#062033"
GOLD = "#F0B84A"
MUTED = "#A9CBDC"
CARD_BG = "rgba(255,255,255,0.03)"

# ----------------- Safe logo loader -----------------
uploaded_logo = st.sidebar.file_uploader("Upload app logo (optional)", type=["png", "jpg", "jpeg"])
logo_to_show = None
if os.path.exists(LOGO_PATH):
    logo_to_show = LOGO_PATH
elif uploaded_logo is not None:
    logo_to_show = uploaded_logo

# ---------------- CSS (centering, responsive, hover) ----------------
st.markdown(f"""
    <style>
    :root {{
        --primary: {PRIMARY_CYAN};
        --gold: {GOLD};
        --deep: {SECONDARY_DEEP};
        --muted: {MUTED};
    }}
    /* App background & base */
    .stApp {{
        background: radial-gradient(circle at 10% 10%, #031018 0%, #071e2d 40%, #0b2633 100%);
        color: #eaf6fb;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        min-height: 100vh;
        padding-top: 14px;
        padding-bottom: 30px;
    }}

    /* Central card */
    .center-container {{
        max-width: 980px;
        margin: 0 auto;
        border-radius: 14px;
        padding: 1.2rem;
        background: linear-gradient(180deg, rgba(255,255,255,0.01), rgba(255,255,255,0.00));
        box-shadow: 0 16px 50px rgba(3,6,20,0.7);
        border: 1px solid rgba(255,255,255,0.02);
    }}

    /* Header layout: logo top-left, title center-left */
    .header-row {{
        display:flex;
        align-items:center;
        gap:16px;
        justify-content:flex-start;
        margin-bottom:6px;
    }}
    .logo-top-left {{
        width:86px;
        height:auto;
        border-radius:10px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.6);
        object-fit:cover;
    }}
    .title-wrap {{
        display:flex;
        flex-direction:column;
        gap:2px;
        margin-left:6px;
    }}
    .app-title {{
        font-size:22px;
        font-weight:800;
        margin:0;
        color:var(--primary);
        letter-spacing:0.2px;
    }}
    .app-subtitle {{
        color: var(--muted);
        font-size:12px;
        margin:0;
    }}

    /* Input card / preview */
    .input-card {{
        background: {CARD_BG};
        padding: 12px;
        border-radius: 12px;
        margin-top: 12px;
        border: 1px solid rgba(255,255,255,0.02);
    }}
    .preview-card {{
        background: linear-gradient(180deg, rgba(255,255,255,0.015), rgba(255,255,255,0.01));
        padding: 10px;
        border-radius: 12px;
    }}

    /* Poster */
    .poster {{
        border-radius: 12px;
        box-shadow: 0 8px 30px rgba(2,6,23,0.6);
    }}

    /* Result badges */
    .result-badge {{
        padding:10px 16px;
        border-radius:999px;
        font-weight:700;
        display:inline-block;
    }}
    .hit {{
        background: linear-gradient(90deg,var(--primary),#3bd0c7);
        color: #001918;
    }}
    .flop {{
        background: linear-gradient(90deg,#3a3f4b,#1c2732);
        color: #f2f6f8;
    }}

    /* Button hover: scale + glow (works on desktop and mobile tap feedback) */
    .stButton>button {{
        border-radius:10px;
        padding:10px 20px;
        border:none;
        background: linear-gradient(90deg,var(--primary),#2fb6c1);
        box-shadow: 0 8px 20px rgba(24,182,201,0.12);
        transition: transform 0.18s ease, box-shadow 0.18s ease;
        cursor: pointer;
    }}
    .stButton>button:hover {{
        transform: translateY(-3px) scale(1.03);
        box-shadow: 0 18px 40px rgba(24,182,201,0.22);
    }}
    .stButton>button:active {{
        transform: translateY(0px) scale(0.995);
        box-shadow: 0 8px 20px rgba(24,182,201,0.12);
    }}

    /* Footer */
    .footer {{
        color: var(--muted);
        text-align:center;
        margin-top:14px;
        font-size:13px;
    }}

    /* Responsive adjustments */
    @media (max-width: 900px) {{
        .center-container {{
            padding: 1rem;
            margin: 0.6rem;
        }}
        .app-title {{ font-size:20px; }}
    }}
    @media (max-width: 600px) {{
        .logo-top-left {{ width:56px; }}
        .app-title {{ font-size:16px; }}
        .app-subtitle {{ font-size:11px; }}
        /* reduce Lottie size on phones */
        .lottie-container iframe, .lottie-container lottie-player {{
            width:120px !important;
            height:120px !important;
        }}
        .stButton>button {{
            padding: 10px 14px;
            font-size:14px;
        }}
    }}
    </style>
""", unsafe_allow_html=True)

# ----------------- App content -----------------
st.markdown("<div class='center-container'>", unsafe_allow_html=True)

# Header row: place logo at top-left, title next to it
col1, col2 = st.columns([1, 8])
with col1:
    if logo_to_show:
        # use small width so it stays top-left
        st.image(logo_to_show, width=72, use_column_width=False)
    else:
        # placeholder box when no logo
        st.markdown("<div style='width:72px;height:72px;border-radius:10px;background:rgba(255,255,255,0.02);display:flex;align-items:center;justify-content:center;color:#9fb4d8'>Logo</div>", unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div style='display:flex;align-items:flex-start;gap:6px'>
          <div style='display:flex;flex-direction:column;'>
            <div style='font-weight:800;font-size:20px;color:var(--primary)'>Moviegrad</div>
            <div style='font-size:12px;color:var(--muted)'>SUCCESS PREDICTOR — Predict box-office hits with confidence</div>
          </div>
        </div>
    """, unsafe_allow_html=True)

# Lottie animation: placed to the right on large screens, centered on smaller screens
# Use a small wrapper to keep it responsive
components.html(f"""
    <div style="display:flex;justify-content:center;margin-top:6px;margin-bottom:10px;" class="lottie-container">
      <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
      <lottie-player src="{LOTTIE_URL}" background="transparent" speed="0.85"
                    style="width:160px;height:160px;" loop autoplay></lottie-player>
    </div>
""", height=200)

# Main content inputs (center column)
with st.container():
    left_col, mid_col, right_col = st.columns([1, 2, 1])
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

        # Predict button centered inside 3-column trick
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        b1, b2, b3 = st.columns([1, 1, 1])
        with b2:
            predict_btn = st.button("Predict Success", key="predict_with_logo")

        # Preview card
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

        # Poster preview
        if poster is not None:
            st.image(poster, use_column_width=True)
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)  # close center-container

# ---------------- Prediction logic (unchanged aside from UI) ----------------
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
st.markdown(f"<div class='footer'>Made with ❤️ — Aditya Tiwari, Akshat Verma, Ansh Sharma</div>", unsafe_allow_html=True)
