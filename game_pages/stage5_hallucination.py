"""Stage 5 — Hallucination Hunter"""
import streamlit as st, time
from utils.state import award_points, complete_stage, next_stage, speed_bonus
from game_pages.shared import stage_header

QS = [
    {
        "intro": "An AI assistant wrote these facts about Arqiva and UK broadcasting. One is hallucinated.",
        "facts": [
            {"t": "Arqiva operates the UK's main terrestrial TV transmitter network, reaching 98.5% of households.", "ok": True},
            {"t": "DAB digital radio in the UK is largely distributed via Arqiva's transmitter infrastructure.", "ok": True},
            {"t": "Arqiva was founded in 2005 following the merger of Crown Castle UK and the BBC's transmission business.", "ok": True},
            {"t": "Arqiva is headquartered in Silicon Roundabout, London, near the tech startup cluster.", "ok": False,
             "why": "Arqiva is headquartered in Winchester, Hampshire — not London. The model plausibly invented a tech-sounding location."},
            {"t": "Smart metering infrastructure (SMIP) is one of Arqiva's key IoT services.", "ok": True},
        ],
        "hi": 3,
    },
    {
        "intro": "An AI wrote a summary of large language models. Find the hallucination.",
        "facts": [
            {"t": "GPT stands for Generative Pre-trained Transformer.", "ok": True},
            {"t": "LLMs are trained on large datasets of text from the internet, books, and code.", "ok": True},
            {"t": "Claude was created by Anthropic, a company co-founded by former OpenAI researchers.", "ok": True},
            {"t": "ChatGPT reached 100 million users in 2 months — faster than any app in history at the time.", "ok": True},
            {"t": "BERT, developed by Microsoft, was the first transformer model to achieve human-level reading comprehension.", "ok": False,
             "why": "BERT was developed by Google, not Microsoft. Also it wasn't strictly the first — the model invented two false details at once."},
        ],
        "hi": 4,
    },
    {
        "intro": "An AI described AI safety and data risks. Which statement is wrong?",
        "facts": [
            {"t": "Sending personal or commercially sensitive data to a public AI tool may breach GDPR.", "ok": True},
            {"t": "Prompt injection is an attack where malicious instructions are hidden in content the AI reads.", "ok": True},
            {"t": "AI models with no internet access cannot access or leak your company's live systems.", "ok": True},
            {"t": "Microsoft Copilot, when used with a corporate M365 account, automatically prevents all data from leaving the organisation.", "ok": False,
             "why": "This is a common misconception. Copilot has data governance controls but does not automatically prevent all data flows — configuration and policy still matter. Always check with your IT team."},
            {"t": "Training an AI model on private customer data without consent can create legal liability.", "ok": True},
        ],
        "hi": 3,
    },
]

def render():
    stage_header(5, "One AI-generated fact is wrong — spot it before time runs out")

    if "s5_idx" not in st.session_state: st.session_state["s5_idx"] = 0
    idx = st.session_state.get("s5_idx", 0)
    if idx >= len(QS): _complete(); return

    q = QS[idx]
    st.progress(idx / len(QS))
    st.markdown(f"<div style='font-size:0.8rem;color:#8891A8;margin-bottom:1rem;'>Round {idx+1} of {len(QS)}</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='background:#FDF5E1;border:1.5px solid #E8D9A0;border-left:4px solid #C49A2A;
                border-radius:8px;padding:1rem;margin-bottom:1rem;'>
        <span style='font-size:0.72rem;color:#C49A2A;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;'>🤖 AI Output</span>
        <div style='font-size:0.9rem;color:#4a5168;margin-top:4px;'>{q["intro"]}</div>
    </div>""", unsafe_allow_html=True)

    sub_key = f"s5_sub_{idx}"
    submitted = st.session_state.get(sub_key)

    for i, fact in enumerate(q["facts"]):
        is_sub = submitted is not None
        is_pick = (submitted == i)
        is_lie = not fact["ok"]

        if is_sub:
            if is_lie:
                bg, border, color = "#FCEAEA","#C13535","#C13535"; label = "🎯 HALLUCINATION"
            elif is_pick and not is_lie:
                bg, border, color = "#FCEAEA","#EFBCBC","#C13535"; label = "✗ your pick"
            else:
                bg, border, color = "#EAF5EF","#A8D8BC","#1A7A4A"; label = "✓ Correct"
        else:
            bg, border, color = "white","#E2E6EF","#1a2f5e"; label = ""

        reason_html = f'<div style="font-size:0.8rem;color:#C13535;margin-top:6px;font-style:italic;">Why this is wrong: {fact["why"]}</div>' if (is_sub and is_lie and "why" in fact) else ""

        col1, col2 = st.columns([8, 1])
        with col1:
            st.markdown(f"""
            <div style='background:{bg};border:1.5px solid {border};border-radius:10px;
                        padding:0.9rem 1.1rem;margin-bottom:6px;'>
                <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
                    <div style='flex:1;font-size:0.9rem;color:{color};line-height:1.5;'>
                        <strong style='font-family:monospace;color:#8891A8;margin-right:8px;'>{chr(65+i)}.</strong>
                        {fact["t"]}
                    </div>
                    <span style='font-size:0.72rem;font-weight:700;color:{color};margin-left:12px;white-space:nowrap;'>{label}</span>
                </div>
                {reason_html}
            </div>""", unsafe_allow_html=True)
        with col2:
            if not submitted:
                if st.button("Pick", key=f"s5_pick_{idx}_{i}", use_container_width=True):
                    st.session_state[sub_key] = i
                    proc_key = f"s5_proc_{idx}"
                    if not st.session_state.get(proc_key):
                        st.session_state[proc_key] = True
                        correct = (i == q["hi"])
                        if correct:
                            bonus = speed_bonus(st.session_state.get("stage_start_time", time.time()), 50)
                            pts = 150 + bonus
                        else:
                            pts = 0
                        award_points(5, pts)
                        st.session_state[f"s5_pts_{idx}"] = pts
                        st.session_state[f"s5_correct_{idx}"] = correct
                    st.rerun()

    if submitted is not None:
        pts = st.session_state.get(f"s5_pts_{idx}", 0)
        corr = st.session_state.get(f"s5_correct_{idx}", False)
        if corr:
            st.markdown(f"<div class='aq-alert-success' style='margin-top:1rem;'><strong>🎯 You found it! +{pts} pts</strong><br>Always verify AI output against trusted sources, especially for facts about specific organisations.</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='aq-alert-error' style='margin-top:1rem;'><strong>❌ Missed it.</strong> Check option {chr(65+q['hi'])} — {q['facts'][q['hi']].get('why', 'that was the hallucination.')} </div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        final = (idx+1 >= len(QS))
        if final:
            if st.button("✅ Complete Stage 5"):
                complete_stage(5); next_stage(); st.rerun()
        else:
            if st.button("→ Next Round", key=f"s5_nxt_{idx}"):
                st.session_state["s5_idx"] += 1
                st.rerun()

def _complete():
    pts = st.session_state["scores"].get(5,0)
    st.markdown(f"""<div style='text-align:center;padding:3rem;'>
        <div style='font-size:3rem;'>🕵️</div>
        <div style='font-family:"Syne",sans-serif;font-size:2rem;font-weight:800;color:#1a2f5e;'>Stage 5 Complete!</div>
        <div style='font-size:2.5rem;font-family:monospace;font-weight:800;color:#00857A;'>{pts} pts</div>
        <p style='color:#4a5168;'>Hallucination hunter: certified</p></div>""", unsafe_allow_html=True)
    if st.button("→ Stage 6: AI Concepts"):
        complete_stage(5); next_stage(); st.rerun()
