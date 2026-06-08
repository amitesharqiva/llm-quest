import streamlit as st
import time
import random
from utils.state import award_points, complete_stage, next_stage, speed_bonus

QUESTIONS = [
    {
        "context": "The capital of France is",
        "options": ["London", "Paris", "Berlin", "Madrid"],
        "answer": "Paris",
        "explanation": "This is highly predictable — 'Paris' follows this phrase in millions of training texts.",
        "probability": {"Paris": 94, "London": 3, "Berlin": 2, "Madrid": 1},
    },
    {
        "context": "To be or not to",
        "options": ["die", "be", "live", "fight"],
        "answer": "be",
        "explanation": "Shakespeare's famous line — extremely high probability of 'be' completing this.",
        "probability": {"be": 99, "die": 0, "live": 0, "fight": 0},
    },
    {
        "context": "Machine learning models are trained on large amounts of",
        "options": ["code", "data", "hardware", "money"],
        "answer": "data",
        "explanation": "'data' is the overwhelmingly common completion in technical texts.",
        "probability": {"data": 82, "code": 10, "hardware": 5, "money": 3},
    },
    {
        "context": "The quick brown fox jumps over the lazy",
        "options": ["cat", "fence", "dog", "hill"],
        "answer": "dog",
        "explanation": "This classic typing exercise is in almost every text corpus — 'dog' is near-certain.",
        "probability": {"dog": 97, "cat": 1, "fence": 1, "hill": 1},
    },
    {
        "context": "Neural networks are inspired by the human",
        "options": ["body", "brain", "hand", "eye"],
        "answer": "brain",
        "explanation": "This phrase appears thousands of times in AI literature with 'brain' completing it.",
        "probability": {"brain": 88, "body": 6, "hand": 3, "eye": 3},
    },
    {
        "context": "Once upon a",
        "options": ["day", "year", "time", "night"],
        "answer": "time",
        "explanation": "The classic fairy tale opener — 'time' is the statistically dominant completion.",
        "probability": {"time": 91, "day": 5, "year": 3, "night": 1},
    },
]

def render():
    st.markdown("""
    <div style='display:flex; align-items:center; gap:12px; margin-bottom:1.5rem;'>
        <div style='background:rgba(247,196,106,0.15); color:#f7c46a; border:1px solid rgba(247,196,106,0.3);
                    padding:4px 14px; border-radius:20px; font-size:0.78rem; font-weight:700; letter-spacing:0.08em;'>
            STAGE 2 OF 5
        </div>
        <div style='font-size:1.6rem; font-weight:700; color:#e8e8f0;'>🔮 Next Word Prophet</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='background:#13131a; border:1px solid #2a2a3a; border-left:3px solid #f7c46a;
                border-radius:12px; padding:1.2rem; margin-bottom:1.5rem;'>
        <div style='font-size:0.7rem; color:#f7c46a; font-weight:700; letter-spacing:0.1em;
                    text-transform:uppercase; margin-bottom:0.5rem;'>💡 How LLMs predict text</div>
        <div style='color:#e8e8f0; font-size:0.92rem; line-height:1.6;'>
            At its core, an LLM is a <strong style='color:#f7c46a;'>next-token predictor</strong>.
            Given everything it has seen, it assigns a probability to every possible next token.
            The most likely token wins — but not always (that's temperature, coming next!).
        </div>
    </div>
    """, unsafe_allow_html=True)

    if "s2_q_idx" not in st.session_state:
        st.session_state["s2_q_idx"] = 0
        st.session_state["s2_correct"] = 0
        st.session_state["s2_streak"] = 0

    idx = st.session_state["s2_q_idx"]

    if idx >= len(QUESTIONS):
        _show_complete()
        return

    q = QUESTIONS[idx]
    st.progress(idx / len(QUESTIONS))
    st.markdown(f"<div style='font-size:0.8rem; color:#9090a8; margin-bottom:1rem;'>Question {idx+1} of {len(QUESTIONS)} &nbsp;|&nbsp; 🔥 Streak: {st.session_state['s2_streak']}</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown(f"""
        <div style='background:#13131a; border:1px solid #2a2a3a; border-radius:14px;
                    padding:1.5rem; margin-bottom:1.2rem;'>
            <div style='font-size:0.75rem; color:#9090a8; margin-bottom:0.8rem;
                        text-transform:uppercase; letter-spacing:0.08em;'>Context given to the model</div>
            <div style='font-size:1.4rem; font-weight:600; color:#e8e8f0;'>
                "{q["context"]} <span style='color:#f7c46a; background:rgba(247,196,106,0.1);
                padding:2px 12px; border-radius:6px; border:1px dashed rgba(247,196,106,0.4);'>___</span>"
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='font-size:0.88rem; color:#9090a8; margin-bottom:0.75rem;'>Think like the model — what word comes next?</div>", unsafe_allow_html=True)

        for opt in q["options"]:
            key = f"s2_opt_{idx}_{opt}"
            submitted_key = f"s2_submitted_{idx}"
            if not st.session_state.get(submitted_key):
                if st.button(f"  {opt}", use_container_width=True, key=key):
                    st.session_state[submitted_key] = opt
                    st.session_state["stage_start_time_q"] = st.session_state.get("stage_start_time", time.time())
                    st.rerun()
            else:
                chosen = st.session_state[submitted_key]
                correct = q["answer"]
                if opt == correct:
                    st.markdown(f"""
                    <div style='background:rgba(106,247,196,0.1); border:1px solid #6af7c4;
                                border-radius:8px; padding:10px 16px; margin-bottom:4px;
                                color:#6af7c4; font-weight:600;'>✓ {opt}</div>
                    """, unsafe_allow_html=True)
                elif opt == chosen and opt != correct:
                    st.markdown(f"""
                    <div style='background:rgba(247,106,106,0.1); border:1px solid #f76a6a;
                                border-radius:8px; padding:10px 16px; margin-bottom:4px;
                                color:#f76a6a;'>✗ {opt} (your pick)</div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style='background:#1c1c26; border:1px solid #2a2a3a;
                                border-radius:8px; padding:10px 16px; margin-bottom:4px;
                                color:#9090a8;'>{opt}</div>
                    """, unsafe_allow_html=True)

    with col2:
        submitted_key = f"s2_submitted_{idx}"
        if st.session_state.get(submitted_key):
            probs = q["probability"]
            st.markdown("""
            <div style='background:#13131a; border:1px solid #2a2a3a; border-radius:14px; padding:1.2rem;'>
                <div style='font-size:0.75rem; color:#9090a8; margin-bottom:1rem;
                            text-transform:uppercase; letter-spacing:0.08em;'>Model probabilities</div>
            """, unsafe_allow_html=True)
            for word, pct in sorted(probs.items(), key=lambda x: -x[1]):
                bar_color = "#6af7c4" if word == q["answer"] else "#2a2a3a"
                fill_color = "#6af7c4" if word == q["answer"] else "#7c6af7"
                st.markdown(f"""
                <div style='margin-bottom:8px;'>
                    <div style='display:flex; justify-content:space-between; margin-bottom:3px;'>
                        <span style='font-size:0.82rem; color:#e8e8f0;'>{word}</span>
                        <span style='font-size:0.82rem; font-family:monospace; color:#9090a8;'>{pct}%</span>
                    </div>
                    <div style='background:#2a2a3a; border-radius:4px; height:6px;'>
                        <div style='background:{fill_color}; width:{pct}%; height:6px; border-radius:4px;
                                    transition:width 0.5s;'></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='background:#13131a; border:1px solid #2a2a3a; border-radius:14px;
                        padding:1.5rem; text-align:center;'>
                <div style='font-size:2rem; margin-bottom:0.5rem;'>🔮</div>
                <div style='color:#9090a8; font-size:0.85rem;'>Probability bars reveal after you answer</div>
            </div>
            """, unsafe_allow_html=True)

    # Result & explanation
    submitted_key = f"s2_submitted_{idx}"
    if st.session_state.get(submitted_key):
        chosen = st.session_state[submitted_key]
        correct = q["answer"]
        processed_key = f"s2_processed_{idx}"

        if not st.session_state.get(processed_key):
            st.session_state[processed_key] = True
            if chosen == correct:
                st.session_state["s2_correct"] += 1
                st.session_state["s2_streak"] += 1
                streak = st.session_state["s2_streak"]
                streak_bonus = min((streak - 1) * 15, 60)
                pts = 80 + streak_bonus
                award_points(2, pts)
                st.session_state[f"s2_pts_{idx}"] = pts
                st.session_state[f"s2_streak_bonus_{idx}"] = streak_bonus
            else:
                st.session_state["s2_streak"] = 0
                st.session_state[f"s2_pts_{idx}"] = 0

        pts = st.session_state.get(f"s2_pts_{idx}", 0)
        streak_bonus = st.session_state.get(f"s2_streak_bonus_{idx}", 0)

        if chosen == correct:
            st.markdown(f"""
            <div class='alert-success' style='margin-top:1rem;'>
                <strong>✅ Correct!</strong> +{pts} pts {f"(+{streak_bonus} streak bonus 🔥)" if streak_bonus > 0 else ""}<br>
                <span style='font-size:0.88rem; opacity:0.85;'>{q["explanation"]}</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='alert-error' style='margin-top:1rem;'>
                <strong>❌ The model would say "{correct}"</strong><br>
                <span style='font-size:0.88rem; opacity:0.85;'>{q["explanation"]}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if idx + 1 < len(QUESTIONS):
            if st.button("→ Next Question", key=f"s2_next_{idx}"):
                st.session_state["s2_q_idx"] += 1
                st.rerun()
        else:
            if st.button("→ Complete Stage", key="s2_done"):
                complete_stage(2)
                next_stage()
                st.rerun()


def _show_complete():
    score = st.session_state["scores"].get(2, 0)
    correct = st.session_state.get("s2_correct", 0)
    st.markdown(f"""
    <div style='text-align:center; padding:3rem;'>
        <div style='font-size:3rem; margin-bottom:1rem;'>🔮</div>
        <h2 style='color:#f7c46a;'>Stage 2 Complete!</h2>
        <div style='font-size:2.5rem; font-family:monospace; color:#f7c46a; margin:1rem 0;'>{score} pts</div>
        <p style='color:#9090a8;'>{correct}/{len(QUESTIONS)} correct — you think like a language model</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("→ Next Stage: Temperature Lab"):
        complete_stage(2)
        next_stage()
        st.rerun()
