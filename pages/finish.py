import streamlit as st
import time
from utils.state import get_total_score, load_leaderboard, get_rank, save_to_leaderboard

def render():
    save_to_leaderboard()
    total = get_total_score()
    player = st.session_state.get("player_name", "Player")
    rank = get_rank(player)
    scores = st.session_state.get("scores", {})
    elapsed = int(time.time() - st.session_state.get("start_time", time.time()))
    mins = elapsed // 60
    secs = elapsed % 60

    # Grade
    if total >= 900:
        grade, grade_color, grade_msg = "S", "#f7c46a", "LLM Grandmaster"
    elif total >= 700:
        grade, grade_color, grade_msg = "A", "#6af7c4", "Token Wizard"
    elif total >= 500:
        grade, grade_color, grade_msg = "B", "#7c6af7", "Context Crafter"
    elif total >= 300:
        grade, grade_color, grade_msg = "C", "#9090a8", "Prompt Apprentice"
    else:
        grade, grade_color, grade_msg = "D", "#f76a6a", "Hallucination Victim"

    st.markdown(f"""
    <div style='text-align:center; padding:2rem 0;'>
        <div style='font-size:1rem; color:#9090a8; margin-bottom:0.5rem;'>Quest Complete</div>
        <div style='font-size:2.8rem; font-weight:700; color:#e8e8f0;'>{player}</div>
        <div style='font-size:6rem; font-weight:700; color:{grade_color}; line-height:1; margin:0.5rem 0;'>{grade}</div>
        <div style='font-size:1.2rem; color:{grade_color}; font-weight:600; margin-bottom:0.5rem;'>{grade_msg}</div>
        <div style='font-size:0.85rem; color:#9090a8;'>Time: {mins}m {secs:02d}s</div>
    </div>
    """, unsafe_allow_html=True)

    # Score breakdown
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div style='background:#13131a; border:1px solid #2a2a3a; border-radius:14px;
                    padding:1.5rem; text-align:center;'>
            <div style='font-size:0.72rem; color:#9090a8; text-transform:uppercase;
                        letter-spacing:0.1em; margin-bottom:0.5rem;'>Total Score</div>
            <div style='font-size:3rem; font-weight:700; font-family:monospace; color:#f7c46a;'>{total}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style='background:#13131a; border:1px solid #2a2a3a; border-radius:14px;
                    padding:1.5rem; text-align:center;'>
            <div style='font-size:0.72rem; color:#9090a8; text-transform:uppercase;
                        letter-spacing:0.1em; margin-bottom:0.5rem;'>Leaderboard Rank</div>
            <div style='font-size:3rem; font-weight:700; font-family:monospace; color:#7c6af7;'>#{rank or "?"}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div style='background:#13131a; border:1px solid #2a2a3a; border-radius:14px;
                    padding:1.5rem; text-align:center;'>
            <div style='font-size:0.72rem; color:#9090a8; text-transform:uppercase;
                        letter-spacing:0.1em; margin-bottom:0.5rem;'>Time</div>
            <div style='font-size:3rem; font-weight:700; font-family:monospace; color:#6af7c4;'>{mins}:{secs:02d}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Stage breakdown
    stage_names = {1: ("⚡", "Token Slicer"), 2: ("🔮", "Next Word Prophet"),
                   3: ("🌡️", "Temperature Lab"), 4: ("📦", "Context Window"), 5: ("🕵️", "Hallucination Hunter")}
    max_pts = {1: 510, 2: 660, 3: 360, 4: 500, 5: 840}

    st.markdown("<div style='font-size:0.85rem; color:#9090a8; margin-bottom:0.8rem; text-transform:uppercase; letter-spacing:0.08em;'>Stage breakdown</div>", unsafe_allow_html=True)
    cols = st.columns(5)
    for i, col in enumerate(cols, 1):
        icon, name = stage_names[i]
        pts = scores.get(i, 0)
        mx = max_pts[i]
        pct = min(pts / mx * 100, 100) if mx > 0 else 0
        with col:
            st.markdown(f"""
            <div style='background:#13131a; border:1px solid #2a2a3a; border-radius:12px;
                        padding:1rem; text-align:center;'>
                <div style='font-size:1.5rem; margin-bottom:4px;'>{icon}</div>
                <div style='font-size:0.72rem; color:#9090a8; margin-bottom:8px;'>{name}</div>
                <div style='font-size:1.4rem; font-weight:700; font-family:monospace; color:#f7c46a;'>{pts}</div>
                <div style='background:#2a2a3a; border-radius:4px; height:4px; margin-top:6px;'>
                    <div style='background:#7c6af7; width:{pct}%; height:4px; border-radius:4px;'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # What you learned
    st.markdown("""
    <div style='background:#13131a; border:1px solid #2a2a3a; border-radius:14px; padding:1.5rem; margin-bottom:1.5rem;'>
        <div style='font-size:0.78rem; color:#7c6af7; font-weight:700; letter-spacing:0.1em;
                    text-transform:uppercase; margin-bottom:1rem;'>What you learned today</div>
        <div style='display:grid; grid-template-columns:1fr 1fr; gap:0.8rem;'>
            <div style='font-size:0.88rem; color:#e8e8f0;'>⚡ <strong>Tokens</strong> — LLMs read chunks, not words</div>
            <div style='font-size:0.88rem; color:#e8e8f0;'>🔮 <strong>Prediction</strong> — LLMs are next-token engines</div>
            <div style='font-size:0.88rem; color:#e8e8f0;'>🌡️ <strong>Temperature</strong> — controls randomness</div>
            <div style='font-size:0.88rem; color:#e8e8f0;'>📦 <strong>Context window</strong> — limited memory</div>
            <div style='font-size:0.88rem; color:#e8e8f0;'>🕵️ <strong>Hallucination</strong> — confident but wrong</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏆 View Full Leaderboard", use_container_width=True):
            st.session_state["page"] = "leaderboard"
            st.rerun()
    with col2:
        if st.button("🔄 Play Again", use_container_width=True):
            name = st.session_state.get("player_name", "")
            for key in list(st.session_state.keys()):
                if key != "player_name":
                    del st.session_state[key]
            from utils.state import init_state
            import time
            init_state()
            st.session_state["player_name"] = name
            st.session_state["page"] = "game"
            st.session_state["stage"] = 1
            st.session_state["start_time"] = time.time()
            st.session_state["stage_start_time"] = time.time()
            st.rerun()
