import streamlit as st
import time
from utils.state import init_state

def render():
    st.markdown("""
    <div style='text-align:center; padding: 3rem 0 2rem;'>
        <div style='font-size:4rem; margin-bottom:0.5rem;'>🧠</div>
        <h1 style='font-size:3.5rem; font-weight:700; color:#e8e8f0; margin:0; line-height:1.1;'>LLM Quest</h1>
        <div style='font-size:1.1rem; color:#9090a8; margin-top:0.75rem; margin-bottom:0.25rem;'>
            5 puzzles · learn how AI really works · compete live
        </div>
        <div style='display:inline-block; background:rgba(124,106,247,0.15); color:#7c6af7;
                    border:1px solid rgba(124,106,247,0.3); padding:3px 14px; border-radius:20px;
                    font-size:0.78rem; font-weight:700; letter-spacing:0.08em; text-transform:uppercase;'>
            Arqiva Live 2025
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Stage overview cards
    stages = [
        ("⚡", "Token Slicer", "Slice text like an LLM does", "#7c6af7"),
        ("🔮", "Next Word Prophet", "Predict what the model thinks comes next", "#f7c46a"),
        ("🌡️", "Temperature Lab", "Control AI randomness with a dial", "#6af7c4"),
        ("📦", "Context Window", "Pack tokens into a limited window", "#f76a6a"),
        ("🕵️", "Hallucination Hunter", "Spot the AI lie hidden in the facts", "#f7a86a"),
    ]

    cols = st.columns(5)
    for i, (icon, name, desc, color) in enumerate(stages):
        with cols[i]:
            st.markdown(f"""
            <div style='background:#13131a; border:1px solid #2a2a3a; border-radius:14px;
                        padding:1.2rem 0.8rem; text-align:center; height:160px;
                        display:flex; flex-direction:column; justify-content:center;'>
                <div style='font-size:2rem; margin-bottom:0.5rem;'>{icon}</div>
                <div style='font-weight:700; font-size:0.9rem; color:#e8e8f0; margin-bottom:0.3rem;'>{name}</div>
                <div style='font-size:0.75rem; color:#9090a8; line-height:1.4;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Name entry
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='background:#13131a; border:1px solid #2a2a3a; border-radius:16px; padding:2rem; text-align:center;'>
            <div style='font-size:1.2rem; font-weight:600; margin-bottom:1.5rem; color:#e8e8f0;'>
                Enter your name to start
            </div>
        """, unsafe_allow_html=True)

        name = st.text_input(
            "Your name",
            placeholder="e.g. Ami Hassan",
            label_visibility="collapsed",
            key="name_input"
        )

        if name and len(name.strip()) >= 2:
            if st.button("🚀  Start the Quest", use_container_width=True):
                st.session_state["player_name"] = name.strip()
                st.session_state["page"] = "game"
                st.session_state["stage"] = 1
                st.session_state["start_time"] = time.time()
                st.session_state["stage_start_time"] = time.time()
                st.rerun()
        else:
            st.markdown("""
            <div style='color:#9090a8; font-size:0.85rem; text-align:center; margin-top:0.5rem;'>
                Type at least 2 characters to begin
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # How scoring works
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    scoring_items = [
        ("⚡ Speed bonus", "Answer fast, earn extra points"),
        ("🎯 Accuracy", "Right answers unlock bonus points"),
        ("💡 No hints", "Skip hints to maximise your score"),
    ]
    for col, (title, desc) in zip([col1, col2, col3], scoring_items):
        with col:
            st.markdown(f"""
            <div style='text-align:center; padding:1rem; background:#13131a;
                        border:1px solid #2a2a3a; border-radius:12px;'>
                <div style='font-weight:600; margin-bottom:0.3rem;'>{title}</div>
                <div style='font-size:0.82rem; color:#9090a8;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)
