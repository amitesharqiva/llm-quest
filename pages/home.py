import streamlit as st, time
from utils.state import init_state

STAGES = [
    ("⚡", "Token Slicer",        "How AI reads text",          "#00857A"),
    ("🔮", "Word Prediction",     "How AI generates language",  "#1a2f5e"),
    ("🌡️", "Temperature",         "Controlling AI creativity",  "#E8580A"),
    ("📦", "Context Window",      "AI memory limits",           "#C49A2A"),
    ("🕵️", "Hallucination Hunter","Spotting AI mistakes",       "#6B3FA0"),
    ("🤖", "AI Concepts",         "LLM vs Chatbot vs Agent",    "#00857A"),
    ("💼", "AI at Arqiva",        "Real use cases & ROI",       "#1a2f5e"),
    ("🔒", "AI Safety",           "Stay safe, stay smart",      "#C13535"),
]

def render():
    # Arqiva top bar
    st.markdown("""
    <div style='background:#1a2f5e; border-radius:14px; padding:1.4rem 2rem;
                display:flex; align-items:center; justify-content:space-between; margin-bottom:2rem;
                box-shadow:0 4px 20px rgba(26,47,94,0.18);'>
        <div>
            <div style='font-family:"Syne",sans-serif; font-size:2rem; font-weight:800;
                        color:white; letter-spacing:0.05em;'>ARQIVA</div>
            <div style='font-size:0.75rem; color:#8BA3CC; letter-spacing:0.15em;
                        text-transform:uppercase; margin-top:1px;'>AI Literacy Quest</div>
        </div>
        <div style='text-align:right;'>
            <div style='font-size:0.72rem; color:#8BA3CC; text-transform:uppercase; letter-spacing:0.1em;'>Arqiva Live 2025</div>
            <div style='background:#00857A; color:white; font-size:0.72rem; font-weight:700;
                        padding:3px 12px; border-radius:20px; display:inline-block; margin-top:4px;
                        letter-spacing:0.06em; text-transform:uppercase;'>8 Stages · Learn AI by Playing</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Hero
    col_l, col_r = st.columns([3, 2])
    with col_l:
        st.markdown("""
        <div style='padding:0.5rem 0 1.5rem;' class='fade-up'>
            <div style='font-family:"Syne",sans-serif; font-size:3.2rem; font-weight:800;
                        color:#1a2f5e; line-height:1.1; margin-bottom:1rem;'>
                Understand AI.<br>
                <span style='color:#00857A;'>Beat your colleagues.</span>
            </div>
            <p style='font-size:1.05rem; color:#4a5168; line-height:1.7; max-width:520px;'>
                8 interactive puzzles that teach you how AI actually works — no jargon, no lectures.
                From tokens and temperature to safety and Arqiva use cases. Play at your own pace, score points, climb the leaderboard.
            </p>
            <div style='display:flex; gap:12px; flex-wrap:wrap; margin-top:1rem;'>
                <div style='background:#E6F4F3; border:1px solid #B3DDD9; border-radius:8px;
                            padding:6px 14px; font-size:0.82rem; font-weight:600; color:#00857A;'>⏱ ~30 mins</div>
                <div style='background:#EEF1F8; border:1px solid #C5CCE0; border-radius:8px;
                            padding:6px 14px; font-size:0.82rem; font-weight:600; color:#1a2f5e;'>👥 Up to 50 players</div>
                <div style='background:#FEF0E9; border:1px solid #F5C4A9; border-radius:8px;
                            padding:6px 14px; font-size:0.82rem; font-weight:600; color:#E8580A;'>🏆 Live leaderboard</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_r:
        st.markdown("""
        <div style='background:white; border:1.5px solid #E2E6EF; border-radius:16px;
                    padding:1.8rem; box-shadow:0 4px 24px rgba(26,47,94,0.10); margin-top:0.5rem;'>
            <div style='font-family:"Syne",sans-serif; font-size:1.1rem; font-weight:700;
                        color:#1a2f5e; margin-bottom:1.2rem;'>Join the quest</div>
        """, unsafe_allow_html=True)

        name = st.text_input("Your name", placeholder="e.g. Ami Hassan", key="name_input", label_visibility="collapsed")
        team = st.text_input("Team / Department (optional)", placeholder="e.g. Engineering, Operations", key="team_input", label_visibility="collapsed")

        st.markdown("<div style='margin-top:-0.3rem; margin-bottom:0.8rem; font-size:0.82rem; color:#8891A8;'>Optional — for team scoring on the leaderboard</div>", unsafe_allow_html=True)

        ready = name and len(name.strip()) >= 2
        if ready:
            if st.button("🚀  Start the Quest", use_container_width=True):
                st.session_state.update({
                    "player_name": name.strip(),
                    "player_team": team.strip() if team else "",
                    "page": "game", "stage": 1,
                    "start_time": time.time(),
                    "stage_start_time": time.time(),
                })
                st.rerun()
        else:
            st.markdown("""
            <div style='background:#F7F9FC; border:1.5px dashed #CBD2E0; border-radius:8px;
                        padding:10px; text-align:center; font-size:0.85rem; color:#8891A8;'>
                Enter your name to begin
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Stage grid
    st.markdown("""
    <div style='font-family:"Syne",sans-serif; font-size:1.2rem; font-weight:700;
                color:#1a2f5e; margin-bottom:1rem;'>What you'll learn</div>
    """, unsafe_allow_html=True)

    cols = st.columns(4)
    for i, (icon, name_s, desc, color) in enumerate(STAGES):
        with cols[i % 4]:
            num = i + 1
            st.markdown(f"""
            <div style='background:white; border:1.5px solid #E2E6EF; border-radius:12px;
                        padding:1.1rem; margin-bottom:0.8rem; box-shadow:0 2px 8px rgba(26,47,94,0.05);
                        transition:all 0.2s; cursor:default;
                        border-top:3px solid {color};'>
                <div style='display:flex; align-items:center; gap:8px; margin-bottom:0.4rem;'>
                    <span style='font-size:1.3rem;'>{icon}</span>
                    <span style='font-size:0.68rem; font-weight:700; color:{color};
                                text-transform:uppercase; letter-spacing:0.08em;'>Stage {num}</span>
                </div>
                <div style='font-family:"Syne",sans-serif; font-size:0.92rem; font-weight:700;
                            color:#1a2f5e; margin-bottom:3px;'>{name_s}</div>
                <div style='font-size:0.78rem; color:#4a5168; line-height:1.4;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    # How scoring works
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background:#1a2f5e; border-radius:14px; padding:1.5rem 2rem;'>
        <div style='font-family:"Syne",sans-serif; font-size:1rem; font-weight:700;
                    color:white; margin-bottom:1rem;'>How scoring works</div>
        <div style='display:grid; grid-template-columns:1fr 1fr 1fr; gap:1rem;'>
            <div style='text-align:center;'>
                <div style='font-size:1.5rem; margin-bottom:4px;'>⚡</div>
                <div style='font-size:0.82rem; font-weight:600; color:white;'>Speed bonus</div>
                <div style='font-size:0.75rem; color:#8BA3CC; margin-top:2px;'>Answer fast, earn extra points</div>
            </div>
            <div style='text-align:center;'>
                <div style='font-size:1.5rem; margin-bottom:4px;'>🎯</div>
                <div style='font-size:0.82rem; font-weight:600; color:white;'>Accuracy</div>
                <div style='font-size:0.75rem; color:#8BA3CC; margin-top:2px;'>Right answers score highest</div>
            </div>
            <div style='text-align:center;'>
                <div style='font-size:1.5rem; margin-bottom:4px;'>🔥</div>
                <div style='font-size:0.82rem; font-weight:600; color:white;'>Streak bonus</div>
                <div style='font-size:0.75rem; color:#8BA3CC; margin-top:2px;'>Consecutive wins multiply points</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
