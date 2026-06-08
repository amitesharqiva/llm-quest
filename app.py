import streamlit as st
from utils.state import init_state
from utils.styles import ARQIVA_CSS
from utils.leaderboard import render_sidebar

st.set_page_config(
    page_title="AI Literacy Quest · Arqiva",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(ARQIVA_CSS, unsafe_allow_html=True)
init_state()

page  = st.session_state.get("page", "home")
stage = st.session_state.get("stage", 1)

if page == "home":
    from game_pages.home import render; render()

elif page == "game":
    render_sidebar()
    if   stage == 1: from game_pages.stage1_tokens       import render; render()
    elif stage == 2: from game_pages.stage2_prediction   import render; render()
    elif stage == 3: from game_pages.stage3_temperature  import render; render()
    elif stage == 4: from game_pages.stage4_context      import render; render()
    elif stage == 5: from game_pages.stage5_hallucination import render; render()
    elif stage == 6: from game_pages.stage6_ai_concepts  import render; render()
    elif stage == 7: from game_pages.stage7_arqiva_usecases import render; render()
    elif stage == 8: from game_pages.stage8_ai_safety    import render; render()
    elif stage >= 9: from game_pages.finish              import render; render()

elif page == "leaderboard":
    render_sidebar()
    from game_pages.leaderboard import render; render()
