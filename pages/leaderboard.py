import streamlit as st
from utils.state import load_leaderboard

def render():
    if st.button("← Back"):
        st.session_state["page"] = "game" if st.session_state.get("stage", 1) <= 5 else "game"
        st.rerun()

    st.markdown("""
    <div style='text-align:center; padding:1.5rem 0 2rem;'>
        <div style='font-size:3rem; margin-bottom:0.5rem;'>🏆</div>
        <h1 style='font-size:2.5rem; font-weight:700; color:#e8e8f0; margin:0;'>Leaderboard</h1>
        <div style='font-size:0.9rem; color:#9090a8; margin-top:0.5rem;'>LLM Quest — Arqiva Live 2025</div>
    </div>
    """, unsafe_allow_html=True)

    board = load_leaderboard()
    player = st.session_state.get("player_name", "")

    if not board:
        st.markdown("""
        <div style='text-align:center; padding:3rem; color:#9090a8;'>
            No scores yet — be the first to finish!
        </div>
        """, unsafe_allow_html=True)
        return

    medals = ["🥇", "🥈", "🥉"]

    for i, entry in enumerate(board):
        is_you = entry["name"] == player
        rank_icon = medals[i] if i < 3 else f"#{i+1}"
        elapsed = entry.get("time", 0)
        mins = elapsed // 60
        secs = elapsed % 60
        time_str = f"{mins}:{secs:02d}"

        score_color = "#f7c46a" if i == 0 else ("#9090a8" if i == 1 else ("#f7a86a" if i == 2 else "#e8e8f0"))

        st.markdown(f"""
        <div style='background:{"rgba(124,106,247,0.12)" if is_you else ("#13131a" if i % 2 == 0 else "#1c1c26")};
                    border:{"1px solid rgba(124,106,247,0.4)" if is_you else "1px solid #2a2a3a"};
                    border-radius:10px; padding:1rem 1.5rem; margin-bottom:6px;
                    display:flex; align-items:center; justify-content:space-between;'>
            <div style='display:flex; align-items:center; gap:16px;'>
                <span style='font-size:1.4rem; min-width:2rem;'>{rank_icon}</span>
                <div>
                    <div style='font-weight:600; font-size:1rem; color:#e8e8f0;'>
                        {entry["name"]}
                        {' <span style="background:rgba(124,106,247,0.2); color:#7c6af7; font-size:0.7rem; padding:2px 8px; border-radius:10px; font-weight:700; margin-left:6px;">YOU</span>' if is_you else ''}
                    </div>
                    <div style='font-size:0.78rem; color:#9090a8; margin-top:2px;'>Completed in {time_str}</div>
                </div>
            </div>
            <div style='font-size:1.8rem; font-weight:700; font-family:monospace; color:{score_color};'>
                {entry["score"]}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Refresh Scores", use_container_width=True):
            st.rerun()
    with col2:
        if st.button("🎮 Play Again", use_container_width=True):
            name = st.session_state.get("player_name", "")
            for key in list(st.session_state.keys()):
                if key != "player_name":
                    del st.session_state[key]
            from utils.state import init_state
            import time
            init_state()
            st.session_state["player_name"] = name
            st.session_state["page"] = "home"
            st.rerun()
