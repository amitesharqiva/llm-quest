"""Stage 2 — Next Word Prediction"""
import streamlit as st, time
from utils.state import award_points, complete_stage, next_stage, speed_bonus
from game_pages.shared import stage_header, mcq_question, next_btn

QS = [
    ("The capital of France is ___",
     ["London","Paris","Berlin","Madrid"], 1,
     "Paris is overwhelmingly the most likely next token in every text corpus. The model has seen this millions of times.",
     {"Paris":94,"London":3,"Berlin":2,"Madrid":1}),
    ("Machine learning models are trained on large amounts of ___",
     ["code","data","hardware","electricity"], 1,
     "'Data' completes this phrase in 80%+ of technical texts. The model has learned this as near-certain.",
     {"data":82,"code":11,"hardware":5,"electricity":2}),
    ("To be or not to ___",
     ["die","live","be","fight"], 2,
     "Shakespeare's line appears in almost every English text corpus. 'be' is 99% likely.",
     {"be":99,"die":0,"live":0,"fight":1}),
    ("Neural networks are inspired by the human ___",
     ["body","brain","hand","eye"], 1,
     "This exact phrase appears thousands of times in AI papers always followed by 'brain'.",
     {"brain":88,"body":7,"hand":3,"eye":2}),
    ("Once upon a ___",
     ["day","year","time","night"], 2,
     "The classic fairy tale opener — 'time' is the dominant completion across all story corpora.",
     {"time":91,"day":5,"year":3,"night":1}),
]

def render():
    stage_header(2, "Think like the model — what word comes next?")

    if "s2_idx" not in st.session_state: st.session_state["s2_idx"] = 0
    if "s2_streak" not in st.session_state: st.session_state["s2_streak"] = 0

    idx = st.session_state.get("s2_idx", 0)
    if idx >= len(QS): _complete(); return

    q = QS[idx]
    st.progress(idx / len(QS))
    st.markdown(f"<div style='font-size:0.8rem;color:#8891A8;margin-bottom:1rem;'>Question {idx+1} of {len(QS)} &nbsp;·&nbsp; 🔥 Streak: {st.session_state['s2_streak']}</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])
    sub_key = f"s2_sub_{idx}"

    with col1:
        st.markdown(f"""
        <div style='background:white;border:1.5px solid #E2E6EF;border-radius:12px;
                    padding:1.5rem;margin-bottom:1rem;box-shadow:0 2px 8px rgba(26,47,94,0.05);'>
            <div style='font-size:0.72rem;color:#8891A8;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.6rem;'>Model sees this</div>
            <div style='font-size:1.3rem;font-weight:600;color:#1a2f5e;line-height:1.5;'>
                "{q[0].replace("___", '<span style="background:#EEF1F8;border:1.5px dashed #C5CCE0;padding:2px 16px;border-radius:6px;color:#8891A8;">?</span>')}"
            </div>
        </div>
        """, unsafe_allow_html=True)

        submitted = st.session_state.get(sub_key)
        options = q[1]
        correct_idx = q[2]

        for i, opt in enumerate(options):
            btn_key = f"s2_opt_{idx}_{i}"
            if submitted is None:
                if st.button(f"  {opt}", key=btn_key, use_container_width=True):
                    st.session_state[sub_key] = i
                    proc_key = f"s2_proc_{idx}"
                    if not st.session_state.get(proc_key):
                        st.session_state[proc_key] = True
                        correct = (i == correct_idx)
                        if correct:
                            st.session_state["s2_streak"] += 1
                            streak_b = min((st.session_state["s2_streak"]-1)*15, 60)
                            bonus = speed_bonus(st.session_state.get("stage_start_time", time.time()), 30)
                            pts = 80 + streak_b + bonus
                        else:
                            st.session_state["s2_streak"] = 0
                            pts = 0
                        award_points(2, pts)
                        st.session_state[f"s2_pts_{idx}"] = pts
                        st.session_state[f"s2_correct_{idx}"] = correct
                    st.rerun()
            else:
                if i == correct_idx:
                    st.markdown(f"<div class='aq-alert-success' style='margin-bottom:4px;'>✓ {opt}</div>", unsafe_allow_html=True)
                elif i == submitted and i != correct_idx:
                    st.markdown(f"<div class='aq-alert-error' style='margin-bottom:4px;'>✗ {opt} — your pick</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='background:#F7F9FC;border:1.5px solid #E2E6EF;border-radius:8px;padding:0.7rem 1rem;margin-bottom:4px;font-size:0.9rem;color:#8891A8;'>{opt}</div>", unsafe_allow_html=True)

    with col2:
        if st.session_state.get(sub_key) is not None:
            probs = q[4]
            st.markdown("""
            <div style='background:white;border:1.5px solid #E2E6EF;border-radius:12px;padding:1.2rem;'>
                <div style='font-size:0.72rem;color:#8891A8;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.8rem;'>Model probabilities</div>
            """, unsafe_allow_html=True)
            for word, pct in sorted(probs.items(), key=lambda x: -x[1]):
                is_correct = (word == options[correct_idx])
                fill = "#00857A" if is_correct else "#C5CCE0"
                st.markdown(f"""
                <div style='margin-bottom:8px;'>
                    <div style='display:flex;justify-content:space-between;margin-bottom:3px;'>
                        <span style='font-size:0.82rem;color:#1a2f5e;font-weight:{"600" if is_correct else "400"};'>{word}</span>
                        <span style='font-size:0.78rem;font-family:monospace;color:#8891A8;'>{pct}%</span>
                    </div>
                    <div style='background:#EEF1F8;border-radius:4px;height:6px;'>
                        <div style='background:{fill};width:{pct}%;height:6px;border-radius:4px;'></div>
                    </div>
                </div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='background:#EEF1F8;border:1.5px solid #C5CCE0;border-radius:12px;
                        padding:2rem;text-align:center;'>
                <div style='font-size:2rem;margin-bottom:0.5rem;'>🔮</div>
                <div style='font-size:0.85rem;color:#4a5168;'>Probability bars appear after you answer</div>
            </div>""", unsafe_allow_html=True)

    if st.session_state.get(sub_key) is not None:
        pts  = st.session_state.get(f"s2_pts_{idx}", 0)
        corr = st.session_state.get(f"s2_correct_{idx}", False)
        if corr:
            st.markdown(f"<div class='aq-alert-success' style='margin-top:1rem;'><strong>✅ +{pts} pts</strong> — {q[3]}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='aq-alert-error' style='margin-top:1rem;'><strong>❌ The answer was '{options[correct_idx]}'</strong> — {q[3]}</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        final = (idx + 1 >= len(QS))
        next_btn(2, final=final, final_label="✅ Complete Stage 2")

def _complete():
    pts = st.session_state["scores"].get(2,0)
    st.markdown(f"""<div style='text-align:center;padding:3rem;'>
        <div style='font-size:3rem;'>🔮</div>
        <div style='font-family:"Syne",sans-serif;font-size:2rem;font-weight:800;color:#1a2f5e;'>Stage 2 Complete!</div>
        <div style='font-size:2.5rem;font-family:monospace;font-weight:800;color:#00857A;'>{pts} pts</div>
        <p style='color:#4a5168;'>You think like a language model</p></div>""", unsafe_allow_html=True)
    if st.button("→ Stage 3: Temperature Lab"):
        complete_stage(2); next_stage(); st.rerun()
