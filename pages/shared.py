import streamlit as st
from utils.state import complete_stage, next_stage, award_points

STAGE_META = {
    1: ("⚡", "Token Slicer",          "teal",   "#00857A", "#E6F4F3", "#B3DDD9"),
    2: ("🔮", "Word Prediction",        "navy",   "#1a2f5e", "#EEF1F8", "#C5CCE0"),
    3: ("🌡️", "Temperature Lab",        "orange", "#E8580A", "#FEF0E9", "#F5C4A9"),
    4: ("📦", "Context Window",         "gold",   "#C49A2A", "#FDF5E1", "#E8D9A0"),
    5: ("🕵️", "Hallucination Hunter",   "purple", "#6B3FA0", "#F2EEF9", "#C9B8E8"),
    6: ("🤖", "AI Concepts",            "teal",   "#00857A", "#E6F4F3", "#B3DDD9"),
    7: ("💼", "AI at Arqiva",           "navy",   "#1a2f5e", "#EEF1F8", "#C5CCE0"),
    8: ("🔒", "AI Safety & Security",   "red",    "#C13535", "#FCEAEA", "#EFBCBC"),
}

CONCEPTS = {
    1: "Tokenisation — LLMs read text as chunks, not whole words",
    2: "Next-token prediction — LLMs guess what comes next based on patterns",
    3: "Temperature — controls how creative vs predictable the output is",
    4: "Context window — LLMs can only see a limited amount of text at once",
    5: "Hallucination — LLMs can sound confident but still be wrong",
    6: "AI Types — LLMs, chatbots, and agents are very different tools",
    7: "AI ROI — the right AI tool for the right problem saves real time and money",
    8: "AI Safety — good hygiene protects you and Arqiva from real risks",
}

def stage_header(stage_num, subtitle=""):
    icon, name, _, accent, bg, border = STAGE_META[stage_num]
    concept = CONCEPTS.get(stage_num, "")

    # Progress dots
    dots_html = "<div style='display:flex; gap:5px; align-items:center; margin-bottom:0.6rem;'>"
    for i in range(1, 9):
        done = st.session_state.get("stage_complete", {}).get(i, False)
        active = (i == stage_num)
        if done:
            dots_html += f"<div style='width:8px;height:8px;border-radius:50%;background:#00857A;'></div>"
        elif active:
            dots_html += f"<div style='width:10px;height:10px;border-radius:50%;background:{accent};box-shadow:0 0 0 3px {border};'></div>"
        else:
            dots_html += f"<div style='width:8px;height:8px;border-radius:50%;background:#E2E6EF;'></div>"
    dots_html += f"<span style='font-size:0.72rem;color:#8891A8;margin-left:6px;'>{stage_num}/8</span></div>"

    st.markdown(f"""
    <div style='background:{bg}; border:1.5px solid {border}; border-radius:14px;
                padding:1.2rem 1.5rem; margin-bottom:1.5rem;'>
        {dots_html}
        <div style='display:flex; align-items:center; gap:10px;'>
            <span style='font-size:1.8rem;'>{icon}</span>
            <div>
                <div style='font-size:0.68rem; font-weight:700; color:{accent};
                            text-transform:uppercase; letter-spacing:0.1em;'>Stage {stage_num} of 8</div>
                <div style='font-family:"Syne",sans-serif; font-size:1.5rem;
                            font-weight:800; color:#1a2f5e; line-height:1.1;'>{name}</div>
                {f'<div style="font-size:0.88rem; color:#4a5168; margin-top:2px;">{subtitle}</div>' if subtitle else ''}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Concept explainer (collapsible feel via info box)
    if concept:
        st.markdown(f"""
        <div style='background:white; border:1.5px solid {border}; border-left:4px solid {accent};
                    border-radius:8px; padding:0.9rem 1.1rem; margin-bottom:1.2rem;
                    font-size:0.88rem; color:#4a5168; line-height:1.6;'>
            <span style='font-weight:700; color:{accent};'>💡 Key concept: </span>{concept}
        </div>
        """, unsafe_allow_html=True)

def mcq_question(stage, q_idx, question_text, options, correct_idx, explanation,
                 points=100, streak_key=None, bonus_key=None):
    """
    Renders a multiple-choice question with instant feedback.
    Returns True if submitted (answered), False if still pending.
    """
    submitted_key = f"s{stage}_q{q_idx}_submitted"
    processed_key = f"s{stage}_q{q_idx}_processed"
    pts_key       = f"s{stage}_q{q_idx}_pts"
    correct_key   = f"s{stage}_q{q_idx}_correct"

    st.markdown(f"""
    <div style='background:white; border:1.5px solid #E2E6EF; border-radius:12px;
                padding:1.4rem; margin-bottom:1rem; box-shadow:0 2px 8px rgba(26,47,94,0.05);'>
        <div style='font-size:1rem; font-weight:600; color:#1a2f5e; line-height:1.5; margin-bottom:1rem;'>
            {question_text}
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    submitted = st.session_state.get(submitted_key)

    for i, opt in enumerate(options):
        btn_key = f"s{stage}_q{q_idx}_opt{i}"
        if submitted is None:
            if st.button(f"  {opt}", key=btn_key, use_container_width=True):
                st.session_state[submitted_key] = i
                st.rerun()
        else:
            if i == correct_idx:
                st.markdown(f"""<div class='aq-alert-success' style='margin-bottom:4px;'>
                    ✓ {opt}</div>""", unsafe_allow_html=True)
            elif i == submitted and i != correct_idx:
                st.markdown(f"""<div class='aq-alert-error' style='margin-bottom:4px;'>
                    ✗ {opt} — your answer</div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""<div style='background:#F7F9FC; border:1.5px solid #E2E6EF;
                    border-radius:8px; padding:0.7rem 1rem; margin-bottom:4px;
                    font-size:0.9rem; color:#8891A8;'>{opt}</div>""", unsafe_allow_html=True)

    if submitted is not None:
        if not st.session_state.get(processed_key):
            st.session_state[processed_key] = True
            correct = (submitted == correct_idx)
            st.session_state[correct_key] = correct
            if correct:
                import time
                from utils.state import speed_bonus
                bonus = speed_bonus(st.session_state.get("stage_start_time", time.time()), 30)
                if streak_key:
                    st.session_state[streak_key] = st.session_state.get(streak_key, 0) + 1
                    streak_bonus = min((st.session_state[streak_key] - 1) * 10, 40)
                else:
                    streak_bonus = 0
                total_pts = points + bonus + streak_bonus
                award_points(stage, total_pts)
                st.session_state[pts_key] = total_pts
            else:
                if streak_key:
                    st.session_state[streak_key] = 0
                st.session_state[pts_key] = 0

        pts = st.session_state.get(pts_key, 0)
        correct = st.session_state.get(correct_key, False)

        if correct:
            st.markdown(f"""
            <div class='aq-alert-success' style='margin-top:0.8rem;'>
                <strong>✅ Correct! +{pts} pts</strong><br>
                <span style='font-size:0.88rem; font-weight:400;'>{explanation}</span>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='aq-alert-error' style='margin-top:0.8rem;'>
                <strong>❌ Not quite.</strong><br>
                <span style='font-size:0.88rem; font-weight:400;'>{explanation}</span>
            </div>""", unsafe_allow_html=True)

        return True
    return False

def next_btn(stage, label="→ Next Question", final=False, final_label="✅ Complete Stage"):
    txt = final_label if final else label
    if st.button(txt, key=f"s{stage}_next_btn_{final}"):
        if final:
            complete_stage(stage)
            next_stage()
        else:
            st.session_state[f"s{stage}_q_idx"] = st.session_state.get(f"s{stage}_q_idx", 0) + 1
        st.rerun()
