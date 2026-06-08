import streamlit as st
from utils.state import init_state
from utils.leaderboard import render_leaderboard_sidebar

st.set_page_config(
    page_title="LLM Quest",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject global CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

/* Hide default streamlit chrome */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Base theme */
:root {
    --bg: #0a0a0f;
    --surface: #13131a;
    --surface2: #1c1c26;
    --border: #2a2a3a;
    --accent: #7c6af7;
    --accent2: #f7c46a;
    --accent3: #6af7c4;
    --danger: #f76a6a;
    --text: #e8e8f0;
    --text2: #9090a8;
    --mono: 'JetBrains Mono', monospace;
}

.stApp {
    background: var(--bg);
    color: var(--text);
}

/* Streamlit button overrides */
.stButton > button {
    background: var(--accent) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    padding: 0.5rem 1.5rem !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #9984f9 !important;
    transform: translateY(-1px);
}

/* Metric cards */
[data-testid="metric-container"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
}

/* Progress bar */
.stProgress > div > div {
    background: var(--accent) !important;
}

/* Radio buttons */
.stRadio > div {
    gap: 0.5rem;
}

/* Text input */
.stTextInput > div > div > input {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
    font-family: var(--mono) !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

/* Custom card */
.quest-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

.quest-card.highlight {
    border-color: var(--accent);
    box-shadow: 0 0 20px rgba(124,106,247,0.15);
}

/* Token chip */
.token-chip {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 6px;
    font-family: var(--mono);
    font-size: 0.85rem;
    font-weight: 600;
    margin: 2px;
    cursor: default;
}

/* Score flash */
@keyframes scoreFlash {
    0% { transform: scale(1); }
    50% { transform: scale(1.2); color: #6af7c4; }
    100% { transform: scale(1); }
}
.score-flash { animation: scoreFlash 0.4s ease; }

/* Stage badge */
.stage-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

/* Alert boxes */
.alert-success {
    background: rgba(106, 247, 196, 0.1);
    border: 1px solid rgba(106, 247, 196, 0.3);
    border-radius: 10px;
    padding: 1rem;
    color: #6af7c4;
}
.alert-error {
    background: rgba(247, 106, 106, 0.1);
    border: 1px solid rgba(247, 106, 106, 0.3);
    border-radius: 10px;
    padding: 1rem;
    color: #f76a6a;
}
.alert-info {
    background: rgba(124, 106, 247, 0.1);
    border: 1px solid rgba(124, 106, 247, 0.3);
    border-radius: 10px;
    padding: 1rem;
    color: #a89af9;
}

/* Leaderboard row */
.lb-row {
    display: flex;
    align-items: center;
    padding: 0.6rem 0.8rem;
    border-radius: 8px;
    margin-bottom: 4px;
    font-size: 0.9rem;
}
.lb-row.you {
    background: rgba(124,106,247,0.15);
    border: 1px solid rgba(124,106,247,0.3);
}
.lb-row:not(.you) {
    background: var(--surface2);
}

/* Pill selector */
.pill-option {
    display: inline-block;
    padding: 8px 18px;
    border-radius: 20px;
    border: 1px solid var(--border);
    cursor: pointer;
    margin: 4px;
    font-weight: 500;
    transition: all 0.2s;
}

/* Concept label */
.concept-tag {
    display: inline-block;
    background: rgba(124,106,247,0.15);
    color: var(--accent);
    border: 1px solid rgba(124,106,247,0.3);
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.5rem;
}

/* Number big display */
.big-number {
    font-size: 3.5rem;
    font-weight: 700;
    font-family: var(--mono);
    color: var(--accent2);
    line-height: 1;
}

/* Hide streamlit red error borders */
[data-baseweb="input"] { border-color: var(--border) !important; }
</style>
""", unsafe_allow_html=True)

init_state()

# ── Routing ──────────────────────────────────────────────────────────────────
page = st.session_state.get("page", "home")

if page == "home":
    from pages import home
    home.render()
elif page == "game":
    stage = st.session_state.get("stage", 1)
    if stage == 1:
        from pages import stage1_tokeniser
        stage1_tokeniser.render()
    elif stage == 2:
        from pages import stage2_prediction
        stage2_prediction.render()
    elif stage == 3:
        from pages import stage3_temperature
        stage3_temperature.render()
    elif stage == 4:
        from pages import stage4_context
        stage4_context.render()
    elif stage == 5:
        from pages import stage5_hallucination
        stage5_hallucination.render()
    elif stage == 6:
        from pages import finish
        finish.render()
elif page == "leaderboard":
    from pages import leaderboard
    leaderboard.render()

# Always show sidebar during game
if page in ("game",):
    render_leaderboard_sidebar()
