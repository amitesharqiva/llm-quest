import streamlit as st
from utils.state import load_leaderboard, get_total_score

STAGE_META = {
    1: ("⚡", "Token Slicer"),
    2: ("🔮", "Word Prediction"),
    3: ("🌡️", "Temperature"),
    4: ("📦", "Context Window"),
    5: ("🕵️", "Hallucinations"),
    6: ("🤖", "AI Concepts"),
    7: ("💼", "AI at Arqiva"),
    8: ("🔒", "AI Safety"),
}

def render_sidebar():
    with st.sidebar:
        # Arqiva header
        st.markdown("""
        <div style='background:#1a2f5e; border-radius:12px; padding:1.2rem 1rem; margin-bottom:1rem; text-align:center;'>
            <div style='font-family:"Syne",sans-serif; font-size:1.4rem; font-weight:800; color:white; letter-spacing:0.04em;'>ARQIVA</div>
            <div style='font-size:0.68rem; color:#8BA3CC; letter-spacing:0.12em; text-transform:uppercase; margin-top:2px;'>AI Literacy Quest</div>
            <div style='background:#00857A; height:2px; border-radius:2px; margin:0.8rem 0 0;'></div>
        </div>
        """, unsafe_allow_html=True)

        # Player score card
        player = st.session_state.get("player_name", "")
        team   = st.session_state.get("player_team", "")
        score  = get_total_score()
        stage  = st.session_state.get("stage", 1)
        rank   = None
        board  = load_leaderboard()
        for i, e in enumerate(board):
            if e["name"] == player:
                rank = i + 1

        st.markdown(f"""
        <div style='background:white; border:1.5px solid #E2E6EF; border-radius:12px;
                    padding:1rem; margin-bottom:1rem; box-shadow:0 2px 8px rgba(26,47,94,0.06);'>
            <div style='font-size:0.7rem; color:#8891A8; text-transform:uppercase;
                        letter-spacing:0.1em; margin-bottom:3px;'>Playing as</div>
            <div style='font-size:1rem; font-weight:700; color:#1a1f2e; font-family:"Syne",sans-serif;'>{player}</div>
            {f'<div style="font-size:0.8rem; color:#4a5168;">{team}</div>' if team else ''}
            <div style='display:flex; justify-content:space-between; align-items:flex-end; margin-top:0.8rem;'>
                <div>
                    <div style='font-size:0.68rem; color:#8891A8; text-transform:uppercase; letter-spacing:0.08em;'>Score</div>
                    <div style='font-size:2rem; font-weight:800; color:#00857A; font-family:"Syne",sans-serif; line-height:1.1;'>{score}</div>
                </div>
                <div style='text-align:right;'>
                    <div style='font-size:0.68rem; color:#8891A8; text-transform:uppercase; letter-spacing:0.08em;'>Rank</div>
                    <div style='font-size:2rem; font-weight:800; color:#1a2f5e; font-family:"Syne",sans-serif; line-height:1.1;'>
                        {"#"+str(rank) if rank else "—"}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Stage progress
        st.markdown("<div style='font-size:0.7rem; color:#8891A8; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.5rem;'>Progress</div>", unsafe_allow_html=True)
        scores = st.session_state.get("scores", {})
        done   = st.session_state.get("stage_complete", {})

        for s in range(1, 9):
            icon, name = STAGE_META[s]
            pts       = scores.get(s, 0)
            is_done   = done.get(s, False)
            is_active = (s == stage)
            is_locked = s > stage

            if is_done:
                bg, border, txt_color = "#EAF5EF", "#A8D8BC", "#1A7A4A"
                dot = "✓"
            elif is_active:
                bg, border, txt_color = "#EEF1F8", "#C5CCE0", "#1a2f5e"
                dot = "▶"
            else:
                bg, border, txt_color = "transparent", "transparent", "#8891A8"
                dot = "○"

            st.markdown(f"""
            <div style='display:flex; justify-content:space-between; align-items:center;
                        background:{bg}; border:1px solid {border}; border-radius:8px;
                        padding:5px 8px; margin-bottom:3px;'>
                <span style='font-size:0.82rem; color:{txt_color}; font-weight:{"600" if is_active or is_done else "400"};'>
                    {dot} {icon} {name}
                </span>
                <span style='font-size:0.78rem; font-family:monospace; color:{txt_color}; font-weight:600;'>
                    {pts if pts > 0 else ""}
                </span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<hr style='border:none; border-top:1.5px solid #E2E6EF; margin:0.8rem 0;'>", unsafe_allow_html=True)

        # Mini leaderboard
        st.markdown("<div style='font-size:0.7rem; color:#8891A8; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.5rem;'>Leaderboard</div>", unsafe_allow_html=True)

        if not board:
            st.markdown("<div style='font-size:0.82rem; color:#8891A8; padding:0.5rem;'>No scores yet</div>", unsafe_allow_html=True)
        else:
            medals = ["🥇", "🥈", "🥉"]
            for i, entry in enumerate(board[:6]):
                is_you = entry["name"] == player
                rank_icon = medals[i] if i < 3 else f"{i+1}."
                st.markdown(f"""
                <div style='display:flex; justify-content:space-between; align-items:center;
                            background:{"#E6F4F3" if is_you else "transparent"};
                            border-radius:6px; padding:4px 8px; margin-bottom:2px;'>
                    <span style='font-size:0.8rem; color:{"#00857A" if is_you else "#4a5168"};
                                font-weight:{"600" if is_you else "400"};'>
                        {rank_icon} {entry["name"]}{" ← you" if is_you else ""}
                    </span>
                    <span style='font-size:0.8rem; font-family:monospace; font-weight:700;
                                color:{"#00857A" if is_you else "#1a1f2e"};'>{entry["score"]}</span>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🏆 Full Leaderboard", use_container_width=True):
            st.session_state["page"] = "leaderboard"
            st.rerun()
