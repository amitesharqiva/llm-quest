"""Stage 7 — AI at Arqiva: Real use cases, ROI, best fit problems"""
import streamlit as st
from utils.state import award_points, complete_stage, next_stage
from pages.shared import stage_header, next_btn

QS = [
    {
        "scenario": {
            "title": "🏭 Scenario: Network Fault Triage",
            "body": "Arqiva's NOC receives 400+ ServiceNow incidents per week. Engineers spend 2–3 hours daily reading, classifying, and routing these manually. Many are duplicates or low-priority noise.",
            "roi_hint": "If an AI agent handles 70% of triage, that's ~14 hours/week saved per engineer.",
        },
        "q": "Which AI approach gives the best ROI for this problem?",
        "opts": [
            "Ask ChatGPT to help — just paste incidents in manually each day",
            "Build a fine-tuned LLM that classifies incidents and routes them automatically via API",
            "Hire more engineers to read the incidents faster",
            "Create a simple Excel macro to filter keywords",
        ],
        "a": 1,
        "explain": "A fine-tuned classification model connected to ServiceNow via API can auto-triage at scale, 24/7, with no manual paste-in. This is exactly the type of agentic AI that delivers measurable ROI — hours saved, faster response times, reduced engineer toil.",
        "roi_box": "💰 Estimated ROI: 14 hrs/week × 52 weeks × £50/hr = ~£36,400/year per engineer saved",
    },
    {
        "scenario": {
            "title": "📡 Scenario: LoRaWAN IoT Data Quality",
            "body": "Arqiva's smart metering platform processes millions of meter readings. Data quality issues — missing readings, wrong UPRNs, duplicate device IDs — cost the team days of investigation per month.",
            "roi_hint": "Automated anomaly detection runs 24/7 and flags issues before they cascade.",
        },
        "q": "What AI capability is best suited to detecting data quality issues at scale?",
        "opts": [
            "A generative AI chatbot — ask it to review the data",
            "An anomaly detection ML model that learns normal patterns and flags outliers automatically",
            "A rule-based script — it's cheaper and simpler",
            "A large language model reading each row and deciding if it looks correct",
        ],
        "a": 1,
        "explain": "Anomaly detection ML (not generative AI) is the right tool here. It learns what 'normal' looks like for each meter and flags deviations automatically. Generative AI reading rows one by one is expensive and slow — wrong tool for the job.",
        "roi_box": "💰 Catching data issues early prevents costly SLA breaches and customer compensation claims",
    },
    {
        "scenario": {
            "title": "📋 Scenario: Document & Report Generation",
            "body": "Arqiva's commercial team produces 30+ customer proposals per quarter. Each proposal takes 4–6 hours to draft, pulling from previous documents, technical specs, and pricing templates.",
            "roi_hint": "AI-assisted drafting with RAG can reduce first-draft time from 4 hours to 45 minutes.",
        },
        "q": "Which combination of AI capabilities is most useful for accelerating proposal creation?",
        "opts": [
            "A rule-based chatbot with dropdown menus for each section",
            "RAG (Retrieval-Augmented Generation): an LLM connected to Arqiva's document library that drafts proposals using relevant past content",
            "Fine-tuning a model specifically on Arqiva proposals from scratch",
            "Using a high-temperature LLM to generate creative, novel proposals",
        ],
        "a": 1,
        "explain": "RAG is the sweet spot — it keeps the LLM grounded in real Arqiva content (previous proposals, specs, pricing) rather than hallucinating. Fine-tuning is expensive and slow to update. A rule-based dropdown misses the nuance of real proposals.",
        "roi_box": "💰 4 hrs → 45 mins per proposal × 30 proposals/quarter = 99 hrs saved = ~£4,950/quarter",
    },
    {
        "scenario": {
            "title": "🔍 Scenario: AI for a CEO briefing",
            "body": "Arqiva's leadership team wants a weekly AI-generated briefing: key incidents from the week, performance vs SLAs, commercial risks, and market news. Currently done manually by a senior analyst taking ~6 hours.",
            "roi_hint": "Automating this frees a senior analyst for higher-value strategic work.",
        },
        "q": "Which statement about using AI for this briefing is TRUE?",
        "opts": [
            "The AI can be fully trusted — just publish its output without human review",
            "AI can draft the briefing from structured data + news sources, but a human should review before it goes to leadership",
            "AI cannot help here — briefings require too much human judgement",
            "Only use AI if you have more than 100 incidents per week — otherwise it's not worth it",
        ],
        "a": 1,
        "explain": "AI can draft rapidly and handle structured data well, but executive-facing content needs human review for accuracy, tone, and context. The model: AI drafts → human reviews → publish. This is 'AI-assisted' not 'AI-replaced'.",
        "roi_box": "💰 6 hrs/week → 1 hr review = 5 hrs saved × 52 weeks = 260 hrs/year of senior analyst time",
    },
    {
        "scenario": {
            "title": "🚫 Scenario: When NOT to use AI",
            "body": "A junior engineer suggests using an LLM to make final decisions on whether to decommission a transmitter mast, based on maintenance logs. The decision affects 40,000 households.",
            "roi_hint": "High-stakes, irreversible decisions need a human in the loop.",
        },
        "q": "What is the correct approach for this high-stakes decision?",
        "opts": [
            "Use the LLM — it's faster and processes more data than a human",
            "Use the LLM but give it a high temperature so it considers more options",
            "AI can analyse the logs and surface insights, but a qualified engineer must make the final decommission decision",
            "Ignore AI entirely — maintenance decisions should never involve AI",
        ],
        "a": 2,
        "explain": "AI is excellent at surfacing patterns in maintenance logs and flagging risk factors. But irreversible decisions affecting tens of thousands of people must have a qualified human making the final call. 'AI-assisted human decision' is the right model here.",
        "roi_box": "⚠️ Rule of thumb: the higher the stakes and the harder to reverse, the more human oversight you need",
    },
]

def render():
    stage_header(7, "Real Arqiva scenarios — pick the right AI approach")

    if "s7_idx" not in st.session_state: st.session_state["s7_idx"] = 0
    if "s7_streak" not in st.session_state: st.session_state["s7_streak"] = 0

    idx = st.session_state.get("s7_idx", 0)
    if idx >= len(QS): _complete(); return

    q = QS[idx]
    st.progress(idx / len(QS))
    st.markdown(f"<div style='font-size:0.8rem;color:#8891A8;margin-bottom:1rem;'>Scenario {idx+1} of {len(QS)} · Streak 🔥{st.session_state['s7_streak']}</div>", unsafe_allow_html=True)

    # Scenario card
    sc = q["scenario"]
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"""
        <div style='background:white;border:1.5px solid #E2E6EF;border-left:4px solid #1a2f5e;
                    border-radius:12px;padding:1.3rem;margin-bottom:1rem;
                    box-shadow:0 2px 8px rgba(26,47,94,0.06);'>
            <div style='font-family:"Syne",sans-serif;font-size:1rem;font-weight:800;
                        color:#1a2f5e;margin-bottom:0.6rem;'>{sc["title"]}</div>
            <div style='font-size:0.9rem;color:#4a5168;line-height:1.6;'>{sc["body"]}</div>
            <div style='background:#EEF1F8;border-radius:8px;padding:0.6rem 0.9rem;margin-top:0.8rem;
                        font-size:0.82rem;color:#4a5168;'><strong>💡 Hint:</strong> {sc["roi_hint"]}</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style='background:#1a2f5e;border-radius:12px;padding:1.2rem;text-align:center;'>
            <div style='font-size:0.68rem;color:#8BA3CC;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:6px;'>Stage</div>
            <div style='font-size:1.8rem;font-weight:800;color:white;font-family:"Syne",sans-serif;'>{idx+1}</div>
            <div style='font-size:0.72rem;color:#8BA3CC;'>of {len(QS)}</div>
        </div>""", unsafe_allow_html=True)

    sub_key = f"s7_sub_{idx}"
    submitted = st.session_state.get(sub_key)

    st.markdown(f"""
    <div style='background:#EEF1F8;border:1.5px solid #C5CCE0;border-radius:10px;
                padding:1rem;margin-bottom:0.8rem;'>
        <div style='font-size:0.95rem;font-weight:600;color:#1a2f5e;'>❓ {q["q"]}</div>
    </div>""", unsafe_allow_html=True)

    for i, opt in enumerate(q["opts"]):
        btn_key = f"s7_opt_{idx}_{i}"
        if submitted is None:
            if st.button(f"  {opt}", key=btn_key, use_container_width=True):
                st.session_state[sub_key] = i
                proc_key = f"s7_proc_{idx}"
                if not st.session_state.get(proc_key):
                    st.session_state[proc_key] = True
                    correct = (i == q["a"])
                    if correct:
                        st.session_state["s7_streak"] += 1
                        streak_b = min((st.session_state["s7_streak"]-1)*10, 40)
                        pts = 120 + streak_b
                    else:
                        st.session_state["s7_streak"] = 0
                        pts = 0
                    award_points(7, pts)
                    st.session_state[f"s7_pts_{idx}"] = pts
                    st.session_state[f"s7_correct_{idx}"] = correct
                st.rerun()
        else:
            if i == q["a"]:
                st.markdown(f"<div class='aq-alert-success' style='margin-bottom:4px;'>✓ {opt}</div>", unsafe_allow_html=True)
            elif i == submitted and i != q["a"]:
                st.markdown(f"<div class='aq-alert-error' style='margin-bottom:4px;'>✗ {opt}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='background:#F7F9FC;border:1.5px solid #E2E6EF;border-radius:8px;padding:0.7rem 1rem;margin-bottom:4px;font-size:0.9rem;color:#8891A8;'>{opt}</div>", unsafe_allow_html=True)

    if submitted is not None:
        pts = st.session_state.get(f"s7_pts_{idx}", 0)
        corr = st.session_state.get(f"s7_correct_{idx}", False)
        if corr:
            st.markdown(f"<div class='aq-alert-success' style='margin-top:0.8rem;'><strong>✅ Correct! +{pts} pts</strong><br><span style='font-weight:400;font-size:0.88rem;'>{q['explain']}</span></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='aq-alert-error' style='margin-top:0.8rem;'><strong>❌ Not quite.</strong><br><span style='font-weight:400;font-size:0.88rem;'>{q['explain']}</span></div>", unsafe_allow_html=True)

        # ROI box always shows after submission
        st.markdown(f"""
        <div style='background:#FDF5E1;border:1.5px solid #E8D9A0;border-radius:10px;
                    padding:0.9rem 1.1rem;margin-top:0.8rem;font-size:0.88rem;color:#7A5A10;
                    font-weight:500;'>{q["roi_box"]}</div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        next_btn(7, final=(idx+1>=len(QS)), final_label="✅ Complete Stage 7")

def _complete():
    pts = st.session_state["scores"].get(7,0)
    st.markdown(f"""<div style='text-align:center;padding:3rem;'>
        <div style='font-size:3rem;'>💼</div>
        <div style='font-family:"Syne",sans-serif;font-size:2rem;font-weight:800;color:#1a2f5e;'>Stage 7 Complete!</div>
        <div style='font-size:2.5rem;font-family:monospace;font-weight:800;color:#00857A;'>{pts} pts</div>
        <p style='color:#4a5168;'>You can now make the case for AI at Arqiva</p></div>""", unsafe_allow_html=True)
    if st.button("→ Stage 8: AI Safety & Security"):
        complete_stage(7); next_stage(); st.rerun()
