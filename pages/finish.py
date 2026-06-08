"""Finish/results page"""
import streamlit as st, time
from utils.state import get_total_score, load_leaderboard, get_rank, save_to_leaderboard

def render():
    save_to_leaderboard()
    total   = get_total_score()
    player  = st.session_state.get("player_name", "")
    team    = st.session_state.get("player_team", "")
    rank    = get_rank(player)
    scores  = st.session_state.get("scores", {})
    elapsed = int(time.time() - st.session_state.get("start_time", time.time()))
    mins, secs = elapsed // 60, elapsed % 60

    if total >= 1800:   grade, gc, gm = "S", "#C49A2A", "AI Grandmaster"
    elif total >= 1400: grade, gc, gm = "A", "#00857A", "AI Strategist"
    elif total >= 1000: grade, gc, gm = "B", "#1a2f5e", "Digital Native"
    elif total >= 600:  grade, gc, gm = "C", "#E8580A", "AI Apprentice"
    else:               grade, gc, gm = "D", "#8891A8", "Getting Started"

    # Header
    st.markdown(f"""
    <div style='background:#1a2f5e;border-radius:16px;padding:2rem 2.5rem;margin-bottom:1.5rem;text-align:center;'>
        <div style='font-size:0.8rem;color:#8BA3CC;text-transform:uppercase;letter-spacing:0.12em;margin-bottom:0.3rem;'>Quest Complete · Arqiva AI Literacy</div>
        <div style='font-family:"Syne",sans-serif;font-size:2.5rem;font-weight:800;color:white;'>{player}</div>
        {f'<div style="color:#8BA3CC;font-size:0.9rem;margin-top:2px;">{team}</div>' if team else ""}
        <div style='font-size:5rem;font-weight:800;color:{gc};font-family:"Syne",sans-serif;line-height:1;margin:0.8rem 0;'>{grade}</div>
        <div style='font-size:1.2rem;font-weight:700;color:{gc};margin-bottom:0.3rem;'>{gm}</div>
        <div style='font-size:0.85rem;color:#8BA3CC;'>Completed in {mins}m {secs:02d}s</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    for col, val, label, color in [
        (c1, total, "Total Score", "#C49A2A"),
        (c2, f"#{rank}" if rank else "—", "Leaderboard Rank", "#00857A"),
        (c3, f"{mins}:{secs:02d}", "Time", "#1a2f5e"),
    ]:
        with col:
            st.markdown(f"""
            <div style='background:white;border:1.5px solid #E2E6EF;border-radius:14px;
                        padding:1.5rem;text-align:center;box-shadow:0 2px 8px rgba(26,47,94,0.06);'>
                <div style='font-size:0.72rem;color:#8891A8;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.4rem;'>{label}</div>
                <div style='font-family:"Syne",sans-serif;font-size:2.8rem;font-weight:800;color:{color};'>{val}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Stage breakdown
    stage_meta = {
        1:("⚡","Token Slicer"),2:("🔮","Prediction"),3:("🌡️","Temperature"),
        4:("📦","Context"),5:("🕵️","Hallucination"),6:("🤖","AI Concepts"),
        7:("💼","AI at Arqiva"),8:("🔒","AI Safety"),
    }
    st.markdown("<div style='font-size:0.8rem;color:#8891A8;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.8rem;'>Stage breakdown</div>", unsafe_allow_html=True)
    cols = st.columns(8)
    for i, col in enumerate(cols, 1):
        icon, name = stage_meta[i]
        pts = scores.get(i, 0)
        done = st.session_state.get("stage_complete", {}).get(i, False)
        with col:
            st.markdown(f"""
            <div style='background:{"#EAF5EF" if done else "white"};border:1.5px solid {"#A8D8BC" if done else "#E2E6EF"};
                        border-radius:10px;padding:0.8rem 0.4rem;text-align:center;'>
                <div style='font-size:1.2rem;'>{icon}</div>
                <div style='font-size:0.68rem;color:#8891A8;margin:3px 0;'>{name}</div>
                <div style='font-size:1rem;font-weight:800;font-family:monospace;color:{"#00857A" if done else "#8891A8"};'>{pts}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # What you learned
    st.markdown("""
    <div style='background:white;border:1.5px solid #E2E6EF;border-radius:14px;padding:1.5rem;margin-bottom:1.5rem;box-shadow:0 2px 8px rgba(26,47,94,0.04);'>
        <div style='font-family:"Syne",sans-serif;font-size:0.95rem;font-weight:800;color:#1a2f5e;margin-bottom:1rem;'>🎓 What you learned today</div>
        <div style='display:grid;grid-template-columns:1fr 1fr;gap:0.6rem;'>
            <div style='font-size:0.88rem;color:#4a5168;padding:0.5rem 0;border-bottom:1px solid #E2E6EF;'>⚡ <strong>Tokens</strong> — LLMs read chunks, not words</div>
            <div style='font-size:0.88rem;color:#4a5168;padding:0.5rem 0;border-bottom:1px solid #E2E6EF;'>🔮 <strong>Prediction</strong> — next-token probability engines</div>
            <div style='font-size:0.88rem;color:#4a5168;padding:0.5rem 0;border-bottom:1px solid #E2E6EF;'>🌡️ <strong>Temperature</strong> — dial between precise and creative</div>
            <div style='font-size:0.88rem;color:#4a5168;padding:0.5rem 0;border-bottom:1px solid #E2E6EF;'>📦 <strong>Context</strong> — AI only sees what you give it</div>
            <div style='font-size:0.88rem;color:#4a5168;padding:0.5rem 0;border-bottom:1px solid #E2E6EF;'>🕵️ <strong>Hallucination</strong> — confident but sometimes wrong</div>
            <div style='font-size:0.88rem;color:#4a5168;padding:0.5rem 0;border-bottom:1px solid #E2E6EF;'>🤖 <strong>AI Types</strong> — LLM vs chatbot vs agent</div>
            <div style='font-size:0.88rem;color:#4a5168;padding:0.5rem 0;'>💼 <strong>AI at Arqiva</strong> — where it creates real ROI</div>
            <div style='font-size:0.88rem;color:#4a5168;padding:0.5rem 0;'>🔒 <strong>AI Safety</strong> — protect data, check before you paste</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🏆 View Full Leaderboard", use_container_width=True):
            st.session_state["page"] = "leaderboard"; st.rerun()
    with c2:
        if st.button("🔄 Play Again", use_container_width=True):
            name = st.session_state.get("player_name","")
            team = st.session_state.get("player_team","")
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            from utils.state import init_state
            init_state()
            st.session_state.update({"player_name":name,"player_team":team,"page":"game","stage":1})
            import time as t; st.session_state["start_time"] = t.time(); st.session_state["stage_start_time"] = t.time()
            st.rerun()
