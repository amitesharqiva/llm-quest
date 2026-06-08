import streamlit as st
import time
from utils.state import award_points, complete_stage, next_stage, speed_bonus, save_to_leaderboard

QUESTIONS = [
    {
        "intro": "An AI assistant was asked about famous inventors. One fact is hallucinated.",
        "facts": [
            {"text": "Alexander Graham Bell is credited with inventing the telephone in 1876.", "correct": True},
            {"text": "Thomas Edison invented the phonograph and held over 1,000 patents.", "correct": True},
            {"text": "Nikola Tesla invented the radio before Marconi, but lost the patent dispute.", "correct": True},
            {"text": "James Watt invented the steam engine from scratch in 1765.", "correct": False, "why": "Watt improved an existing steam engine (Newcomen's). He didn't invent it from scratch."},
            {"text": "The Wright brothers made their first powered flight at Kitty Hawk in 1903.", "correct": True},
        ],
        "hallucination_idx": 3,
    },
    {
        "intro": "An AI summarised key AI milestones. Spot the hallucination.",
        "facts": [
            {"text": "The term 'Artificial Intelligence' was coined by John McCarthy in 1956.", "correct": True},
            {"text": "Deep Blue defeated world chess champion Garry Kasparov in 1997.", "correct": True},
            {"text": "GPT-3 was released by OpenAI in 2020 with 175 billion parameters.", "correct": True},
            {"text": "AlphaGo was developed by Microsoft and beat the world Go champion in 2016.", "correct": False, "why": "AlphaGo was developed by DeepMind (part of Google/Alphabet), not Microsoft."},
            {"text": "The ImageNet competition sparked the modern deep learning era starting in 2012.", "correct": True},
        ],
        "hallucination_idx": 3,
    },
    {
        "intro": "The AI described programming languages. One fact is wrong.",
        "facts": [
            {"text": "Python was created by Guido van Rossum and first released in 1991.", "correct": True},
            {"text": "JavaScript was originally created in just 10 days by Brendan Eich in 1995.", "correct": True},
            {"text": "Java's motto is 'Write Once, Run Anywhere' due to the JVM.", "correct": True},
            {"text": "SQL was invented by IBM researchers and first appeared in 1974.", "correct": True},
            {"text": "C++ was created by Bjarne Stroustrup as an extension of Java in 1979.", "correct": False, "why": "C++ is an extension of C, not Java. Java didn't even exist in 1979."},
        ],
        "hallucination_idx": 4,
    },
    {
        "intro": "The AI described cloud computing facts. Find the lie.",
        "facts": [
            {"text": "AWS (Amazon Web Services) launched in 2006 with S3 and EC2.", "correct": True},
            {"text": "Microsoft Azure was originally announced as 'Windows Azure' in 2008.", "correct": True},
            {"text": "Databricks was founded by the creators of Apache Spark.", "correct": True},
            {"text": "Google Cloud Platform launched before AWS, making it the oldest hyperscaler.", "correct": False, "why": "AWS launched in 2006. Google App Engine launched in 2008. AWS is the oldest major cloud platform."},
            {"text": "Serverless computing allows code to run without managing server infrastructure.", "correct": True},
        ],
        "hallucination_idx": 3,
    },
]

def render():
    st.markdown("""
    <div style='display:flex; align-items:center; gap:12px; margin-bottom:1.5rem;'>
        <div style='background:rgba(247,168,106,0.15); color:#f7a86a; border:1px solid rgba(247,168,106,0.3);
                    padding:4px 14px; border-radius:20px; font-size:0.78rem; font-weight:700; letter-spacing:0.08em;'>
            STAGE 5 OF 5 — FINAL
        </div>
        <div style='font-size:1.6rem; font-weight:700; color:#e8e8f0;'>🕵️ Hallucination Hunter</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='background:#13131a; border:1px solid #2a2a3a; border-left:3px solid #f7a86a;
                border-radius:12px; padding:1.2rem; margin-bottom:1.5rem;'>
        <div style='font-size:0.7rem; color:#f7a86a; font-weight:700; letter-spacing:0.1em;
                    text-transform:uppercase; margin-bottom:0.5rem;'>💡 What is hallucination?</div>
        <div style='color:#e8e8f0; font-size:0.92rem; line-height:1.6;'>
            LLMs sometimes generate <strong style='color:#f7a86a;'>confident-sounding facts that are simply wrong</strong>.
            This is called hallucination. The model isn't lying — it's predicting the most statistically likely text,
            which can sometimes be plausible-but-false. Always verify AI output on critical facts.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if "s5_q_idx" not in st.session_state:
        st.session_state["s5_q_idx"] = 0
        st.session_state["s5_correct"] = 0

    idx = st.session_state["s5_q_idx"]

    if idx >= len(QUESTIONS):
        _show_complete()
        return

    q = QUESTIONS[idx]
    st.progress(idx / len(QUESTIONS))
    st.markdown(f"<div style='font-size:0.8rem; color:#9090a8; margin-bottom:1.5rem;'>Round {idx+1} of {len(QUESTIONS)}</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='background:#1c1c26; border:1px solid #2a2a3a; border-radius:12px; padding:1rem 1.2rem; margin-bottom:1rem;'>
        <span style='font-size:0.85rem; color:#f7a86a;'>🤖 AI Output:</span>
        <span style='font-size:0.88rem; color:#9090a8; margin-left:8px;'>{q["intro"]}</span>
    </div>
    """, unsafe_allow_html=True)

    submitted_key = f"s5_submitted_{idx}"

    for i, fact in enumerate(q["facts"]):
        is_submitted = st.session_state.get(submitted_key) is not None
        user_pick = st.session_state.get(submitted_key)

        if is_submitted:
            is_hallucination = not fact["correct"]
            is_user_pick = (user_pick == i)
            if is_hallucination:
                bg = "rgba(247,168,106,0.12)"
                border = "#f7a86a"
                icon = "🎯 HALLUCINATION"
                reason = fact.get("why", "")
            elif is_user_pick and not is_hallucination:
                bg = "rgba(247,106,106,0.08)"
                border = "#f76a6a33"
                icon = "✗ your pick"
                reason = ""
            else:
                bg = "#13131a"
                border = "#2a2a3a"
                icon = "✓"
                reason = ""

            st.markdown(f"""
            <div style='background:{bg}; border:1px solid {border}; border-radius:10px;
                        padding:0.9rem 1.1rem; margin-bottom:6px;'>
                <div style='display:flex; justify-content:space-between; align-items:flex-start;'>
                    <div style='font-size:0.88rem; color:#e8e8f0; flex:1; line-height:1.5;'>
                        <strong style='font-family:monospace; color:#9090a8; margin-right:8px;'>{chr(65+i)}.</strong>
                        {fact["text"]}
                    </div>
                    <span style='font-size:0.72rem; color:{"#f7a86a" if is_hallucination else "#6af7c4" if not is_user_pick else "#f76a6a"};
                                font-weight:700; margin-left:12px; white-space:nowrap;'>{icon}</span>
                </div>
                {f'<div style="font-size:0.8rem; color:#f7a86a; margin-top:6px; font-style:italic;">Why: {reason}</div>' if reason else ''}
            </div>
            """, unsafe_allow_html=True)
        else:
            if st.button(
                f"{chr(65+i)}. {fact['text'][:90]}{'...' if len(fact['text'])>90 else ''}",
                use_container_width=True,
                key=f"s5_pick_{idx}_{i}"
            ):
                st.session_state[submitted_key] = i
                processed_key = f"s5_processed_{idx}"
                if not st.session_state.get(processed_key):
                    st.session_state[processed_key] = True
                    if i == q["hallucination_idx"]:
                        bonus = speed_bonus(st.session_state.get("stage_start_time", time.time()), 60)
                        pts = 150 + bonus
                        award_points(5, pts)
                        st.session_state[f"s5_pts_{idx}"] = pts
                        st.session_state[f"s5_correct_{idx}"] = True
                        st.session_state["s5_correct"] += 1
                    else:
                        st.session_state[f"s5_pts_{idx}"] = 0
                        st.session_state[f"s5_correct_{idx}"] = False
                st.rerun()

    if st.session_state.get(submitted_key) is not None:
        pts = st.session_state.get(f"s5_pts_{idx}", 0)
        correct = st.session_state.get(f"s5_correct_{idx}", False)
        hallucination_text = q["facts"][q["hallucination_idx"]]["text"]
        why = q["facts"][q["hallucination_idx"]].get("why", "")

        if correct:
            st.markdown(f"""
            <div class='alert-success' style='margin-top:1rem;'>
                <strong>🎯 Found it! +{pts} pts</strong><br>
                <span style='font-size:0.88rem; opacity:0.85;'>{why}</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='alert-error' style='margin-top:1rem;'>
                <strong>❌ Missed it.</strong> The hallucination was:<br>
                <span style='font-size:0.88rem; font-style:italic; opacity:0.85;'>"{hallucination_text}"</span><br>
                <span style='font-size:0.85rem; opacity:0.85; margin-top:4px; display:block;'>{why}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if idx + 1 < len(QUESTIONS):
            if st.button("→ Next Round", key=f"s5_next_{idx}"):
                st.session_state["s5_q_idx"] += 1
                st.rerun()
        else:
            if st.button("🏁 Finish Quest & See Final Score", key="s5_done"):
                complete_stage(5)
                save_to_leaderboard()
                st.session_state["stage"] = 6
                st.rerun()


def _show_complete():
    score = st.session_state["scores"].get(5, 0)
    st.markdown(f"""
    <div style='text-align:center; padding:3rem;'>
        <div style='font-size:3rem; margin-bottom:1rem;'>🕵️</div>
        <h2 style='color:#f7a86a;'>Stage 5 Complete!</h2>
        <div style='font-size:2.5rem; font-family:monospace; color:#f7c46a; margin:1rem 0;'>{score} pts</div>
    </div>
    """, unsafe_allow_html=True)
