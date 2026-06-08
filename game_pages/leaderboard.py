"""Full leaderboard page"""
import streamlit as st
from utils.state import load_leaderboard

def render():
    if st.button("← Back"):
        st.session_state["page"] = "game"; st.rerun()

    st.markdown("""
    <div style='background:#1a2f5e;border-radius:14px;padding:1.5rem 2rem;margin-bottom:1.5rem;text-align:center;'>
        <div style='font-family:"Syne",sans-serif;font-size:0.7rem;font-weight:700;color:#8BA3CC;
                    text-transform:uppercase;letter-spacing:0.12em;margin-bottom:0.3rem;'>Arqiva AI Literacy Quest</div>
        <div style='font-size:2rem;margin-bottom:0.3rem;'>🏆</div>
        <div style='font-family:"Syne",sans-serif;font-size:2rem;font-weight:800;color:white;'>Leaderboard</div>
    </div>
    """, unsafe_allow_html=True)

    board  = load_leaderboard()
    player = st.session_state.get("player_name","")

    if not board:
        st.markdown("<div style='text-align:center;padding:3rem;color:#8891A8;'>No scores yet — be the first to finish!</div>", unsafe_allow_html=True)
        return

    medals = ["🥇","🥈","🥉"]
    for i, entry in enumerate(board):
        is_you = entry["name"] == player
        rank   = medals[i] if i < 3 else f"#{i+1}"
        e      = int(entry.get("time",0))
        t_str  = f"{e//60}:{e%60:02d}"
        stages = entry.get("stages", 0)

        bg     = "#E6F4F3" if is_you else ("white" if i % 2 == 0 else "#F7F9FC")
        border = "#B3DDD9" if is_you else "#E2E6EF"
        nc     = "#00857A" if is_you else "#1a2f5e"

        st.markdown(f"""
        <div style='background:{bg};border:1.5px solid {border};border-radius:10px;
                    padding:0.9rem 1.4rem;margin-bottom:5px;display:flex;align-items:center;justify-content:space-between;'>
            <div style='display:flex;align-items:center;gap:14px;'>
                <span style='font-size:1.3rem;min-width:2rem;'>{rank}</span>
                <div>
                    <div style='font-weight:700;font-size:1rem;color:{nc};'>
                        {entry["name"]} {"<span style='background:#E6F4F3;color:#00857A;font-size:0.68rem;padding:2px 8px;border-radius:10px;font-weight:700;margin-left:6px;'>YOU</span>" if is_you else ""}
                    </div>
                    <div style='font-size:0.78rem;color:#8891A8;margin-top:1px;'>
                        {entry.get("team","")+' · ' if entry.get("team") else ""}{stages}/8 stages · {t_str}
                    </div>
                </div>
            </div>
            <div style='font-family:"Syne",sans-serif;font-size:1.8rem;font-weight:800;color:{"#C49A2A" if i==0 else "#1a2f5e"};'>
                {entry["score"]}
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔄 Refresh", use_container_width=True): st.rerun()
    with c2:
        if st.button("🎮 Play Again", use_container_width=True):
            for k in list(st.session_state.keys()): del st.session_state[k]
            from utils.state import init_state; init_state()
            st.session_state["page"] = "home"; st.rerun()
