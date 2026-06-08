import streamlit as st
from utils.state import load_leaderboard, get_total_score

def render_leaderboard_sidebar():
    board = load_leaderboard()
    player = st.session_state.get("player_name", "")
    your_score = get_total_score()

    with st.sidebar:
        st.markdown("""
        <div style='text-align:center; padding: 0.5rem 0 1rem;'>
            <div style='font-size:1.5rem; font-weight:700; color:#7c6af7;'>🧠 LLM Quest</div>
            <div style='font-size:0.75rem; color:#9090a8; margin-top:2px;'>Arqiva Live 2025</div>
        </div>
        """, unsafe_allow_html=True)

        # Current player score
        stage = st.session_state.get("stage", 1)
        scores = st.session_state.get("scores", {})

        st.markdown(f"""
        <div style='background:#13131a; border:1px solid #2a2a3a; border-radius:12px; padding:1rem; margin-bottom:1rem;'>
            <div style='font-size:0.7rem; color:#9090a8; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:4px;'>Your score</div>
            <div style='font-size:2.2rem; font-weight:700; font-family:"JetBrains Mono",monospace; color:#f7c46a;'>{your_score}</div>
            <div style='font-size:0.8rem; color:#9090a8; margin-top:2px;'>Stage {min(stage,5)} of 5</div>
        </div>
        """, unsafe_allow_html=True)

        # Stage breakdown
        stage_names = {1:"Tokeniser", 2:"Predictor", 3:"Temperature", 4:"Context", 5:"Hallucination"}
        stage_done = st.session_state.get("stage_complete", {})
        for s in range(1, 6):
            done = stage_done.get(s, False)
            pts = scores.get(s, 0)
            color = "#6af7c4" if done else "#9090a8"
            icon = "✓" if done else "○"
            st.markdown(f"""
            <div style='display:flex; justify-content:space-between; align-items:center;
                        padding:4px 8px; border-radius:6px; margin-bottom:3px;
                        background:{"rgba(106,247,196,0.08)" if done else "transparent"}'>
                <span style='font-size:0.82rem; color:{color};'>{icon} {stage_names[s]}</span>
                <span style='font-size:0.82rem; font-family:monospace; color:{color}; font-weight:600;'>{pts}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<hr style='border-color:#2a2a3a; margin:1rem 0;'>", unsafe_allow_html=True)

        # Live leaderboard
        st.markdown("<div style='font-size:0.75rem; color:#9090a8; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.5rem;'>Leaderboard</div>", unsafe_allow_html=True)

        if not board:
            st.markdown("<div style='color:#9090a8; font-size:0.85rem;'>No scores yet — be first!</div>", unsafe_allow_html=True)
        else:
            medals = ["🥇", "🥈", "🥉"]
            for i, entry in enumerate(board[:8]):
                is_you = entry["name"] == player
                rank_display = medals[i] if i < 3 else f"{i+1}."
                bg = "rgba(124,106,247,0.15)" if is_you else ("rgba(255,255,255,0.03)" if i % 2 == 0 else "transparent")
                name_display = entry["name"] + (" ←" if is_you else "")
                st.markdown(f"""
                <div style='display:flex; justify-content:space-between; align-items:center;
                            padding:5px 8px; border-radius:6px; margin-bottom:2px;
                            background:{bg}; {"border:1px solid rgba(124,106,247,0.3);" if is_you else ""}'>
                    <span style='font-size:0.82rem;'>{rank_display} {name_display}</span>
                    <span style='font-size:0.82rem; font-family:monospace; font-weight:600; color:#f7c46a;'>{entry["score"]}</span>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<hr style='border-color:#2a2a3a; margin:1rem 0;'>", unsafe_allow_html=True)

        if st.button("🏆 Full Leaderboard"):
            st.session_state["page"] = "leaderboard"
            st.rerun()
