ARQIVA_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&family=DM+Mono:wght@400;500&display=swap');

/* ── Reset & Base ─────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: #1a1f2e;
}

:root {
    --teal:       #00857A;
    --teal-light: #E6F4F3;
    --teal-mid:   #B3DDD9;
    --navy:       #1a2f5e;
    --navy-light: #EEF1F8;
    --orange:     #E8580A;
    --orange-light: #FEF0E9;
    --gold:       #C49A2A;
    --gold-light: #FDF5E1;
    --ink:        #1a1f2e;
    --ink2:       #4a5168;
    --ink3:       #8891A8;
    --border:     #E2E6EF;
    --border2:    #CBD2E0;
    --surface:    #F7F9FC;
    --surface2:   #EEF1F8;
    --white:      #FFFFFF;
    --success:    #1A7A4A;
    --success-bg: #EAF5EF;
    --error:      #C13535;
    --error-bg:   #FCEAEA;
    --mono:       'DM Mono', monospace;
    --display:    'Syne', sans-serif;
    --radius:     12px;
    --radius-sm:  8px;
    --radius-lg:  16px;
    --shadow:     0 2px 12px rgba(26,47,94,0.08);
    --shadow-md:  0 4px 24px rgba(26,47,94,0.12);
}

/* ── Streamlit chrome overrides ───────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

.stApp {
    background: #F7F9FC !important;
}

[data-testid="stAppViewContainer"] {
    background: #F7F9FC !important;
}

[data-testid="stSidebar"] {
    background: var(--white) !important;
    border-right: 1.5px solid var(--border) !important;
}

[data-testid="stSidebar"] > div {
    padding-top: 0 !important;
}

/* ── Buttons ──────────────────────────────────────────────── */
.stButton > button {
    background: var(--teal) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.55rem 1.4rem !important;
    transition: all 0.18s ease !important;
    box-shadow: 0 1px 3px rgba(0,133,122,0.3) !important;
    letter-spacing: 0.01em !important;
}
.stButton > button:hover {
    background: #006d64 !important;
    box-shadow: 0 3px 10px rgba(0,133,122,0.35) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Inputs ───────────────────────────────────────────────── */
.stTextInput > div > div > input {
    background: var(--white) !important;
    border: 1.5px solid var(--border2) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--ink) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.6rem 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--teal) !important;
    box-shadow: 0 0 0 3px rgba(0,133,122,0.12) !important;
}

/* ── Progress ─────────────────────────────────────────────── */
.stProgress > div > div > div {
    background: var(--teal) !important;
}
.stProgress > div > div {
    background: var(--teal-mid) !important;
    border-radius: 99px !important;
}

/* ── Radio ────────────────────────────────────────────────── */
.stRadio > label { font-weight: 600; font-size: 0.85rem; color: var(--ink2); }
.stRadio > div { gap: 0.4rem; }

/* ── Number input ─────────────────────────────────────────── */
.stNumberInput > div > div > input {
    background: var(--white) !important;
    border: 1.5px solid var(--border2) !important;
    border-radius: var(--radius-sm) !important;
    font-family: var(--mono) !important;
    font-size: 1.2rem !important;
    font-weight: 600 !important;
    color: var(--ink) !important;
    text-align: center !important;
}

/* ── Metrics ──────────────────────────────────────────────── */
[data-testid="metric-container"] {
    background: var(--white) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 1rem !important;
    box-shadow: var(--shadow) !important;
}

/* ── Selectbox ────────────────────────────────────────────── */
.stSelectbox > div > div {
    background: var(--white) !important;
    border: 1.5px solid var(--border2) !important;
    border-radius: var(--radius-sm) !important;
}

/* ── Slider ───────────────────────────────────────────────── */
.stSlider > div > div > div > div {
    background: var(--teal) !important;
}

/* ── Custom component classes ─────────────────────────────── */
.aq-card {
    background: var(--white);
    border: 1.5px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.5rem;
    box-shadow: var(--shadow);
}

.aq-card-teal {
    background: var(--teal-light);
    border: 1.5px solid var(--teal-mid);
    border-radius: var(--radius-lg);
    padding: 1.5rem;
}

.aq-card-navy {
    background: var(--navy);
    border-radius: var(--radius-lg);
    padding: 1.5rem;
    color: white;
}

.aq-tag {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 99px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.07em;
    text-transform: uppercase;
}

.aq-tag-teal  { background: var(--teal-light);   color: var(--teal); border: 1px solid var(--teal-mid); }
.aq-tag-navy  { background: var(--navy-light);   color: var(--navy); border: 1px solid #C5CCE0; }
.aq-tag-orange{ background: var(--orange-light); color: var(--orange); border: 1px solid #F5C4A9; }
.aq-tag-gold  { background: var(--gold-light);   color: var(--gold);  border: 1px solid #E8D9A0; }

.aq-alert-success {
    background: var(--success-bg);
    border: 1.5px solid #A8D8BC;
    border-left: 4px solid var(--success);
    border-radius: var(--radius-sm);
    padding: 1rem 1.2rem;
    color: var(--success);
    font-weight: 500;
}

.aq-alert-error {
    background: var(--error-bg);
    border: 1.5px solid #EFBCBC;
    border-left: 4px solid var(--error);
    border-radius: var(--radius-sm);
    padding: 1rem 1.2rem;
    color: var(--error);
    font-weight: 500;
}

.aq-alert-info {
    background: var(--teal-light);
    border: 1.5px solid var(--teal-mid);
    border-left: 4px solid var(--teal);
    border-radius: var(--radius-sm);
    padding: 1rem 1.2rem;
    color: #005c55;
}

.aq-concept-box {
    background: var(--white);
    border: 1.5px solid var(--border);
    border-left: 4px solid var(--teal);
    border-radius: var(--radius-sm);
    padding: 1rem 1.2rem;
    margin-bottom: 1.2rem;
}

.option-btn-base {
    width: 100%;
    text-align: left;
    background: var(--white);
    border: 1.5px solid var(--border2);
    border-radius: var(--radius-sm);
    padding: 0.85rem 1.1rem;
    margin-bottom: 6px;
    font-size: 0.92rem;
    color: var(--ink);
    cursor: pointer;
    transition: all 0.15s;
    font-family: 'DM Sans', sans-serif;
}
.option-btn-base:hover { border-color: var(--teal); background: var(--teal-light); }
.option-correct { background: var(--success-bg) !important; border-color: var(--success) !important; color: var(--success) !important; font-weight: 600; }
.option-wrong   { background: var(--error-bg)   !important; border-color: var(--error)   !important; color: var(--error)   !important; }

.score-bar-bg   { background: var(--border); border-radius: 99px; height: 8px; }
.score-bar-fill { height: 8px; border-radius: 99px; background: var(--teal); transition: width 0.5s ease; }

.lb-row-you     { background: var(--teal-light); border: 1.5px solid var(--teal-mid); border-radius: var(--radius-sm); padding: 0.65rem 1rem; margin-bottom: 4px; }
.lb-row-other   { background: var(--surface);    border: 1.5px solid var(--border);   border-radius: var(--radius-sm); padding: 0.65rem 1rem; margin-bottom: 4px; }

/* ── Animations ───────────────────────────────────────────── */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50%       { transform: scale(1.06); }
}
@keyframes shimmer {
    0%   { background-position: -200% center; }
    100% { background-position: 200% center; }
}

.fade-up   { animation: fadeUp 0.4s ease both; }
.pulse-anim { animation: pulse 0.5s ease; }

.shimmer-text {
    background: linear-gradient(90deg, var(--teal), var(--navy), var(--teal));
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 3s linear infinite;
}

/* ── Stage progress dots ──────────────────────────────────── */
.stage-dot-done   { width:10px; height:10px; border-radius:50%; background:var(--teal); display:inline-block; }
.stage-dot-active { width:10px; height:10px; border-radius:50%; background:var(--navy); display:inline-block; box-shadow:0 0 0 3px rgba(26,47,94,0.2); }
.stage-dot-lock   { width:10px; height:10px; border-radius:50%; background:var(--border2); display:inline-block; }
</style>
"""
