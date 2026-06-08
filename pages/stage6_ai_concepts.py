"""Stage 6 — AI Concepts: LLM vs Chatbot vs Agent vs Agentic Workflow"""
import streamlit as st, time
from utils.state import award_points, complete_stage, next_stage
from pages.shared import stage_header, next_btn

QS = [
    {
        "concept_card": {
            "title": "What is an LLM?",
            "body": "A <strong>Large Language Model (LLM)</strong> is an AI trained on billions of text examples. It learns statistical patterns in language — which words follow which. It has no memory between sessions, no live internet access (unless given tools), and no 'understanding' in the human sense. It predicts the most likely useful response. Examples: GPT-4, Claude, Gemini.",
            "analogy": "🧠 Think of it like a very well-read person who can only speak from memory — no notes, no phone, no checking facts live.",
        },
        "q": "An Arqiva engineer sends the same question to an LLM twice in separate sessions. What happens?",
        "opts": [
            "The LLM remembers the first answer and builds on it",
            "The LLM gives the same answer both times because it remembers",
            "The LLM treats each session independently — it has no memory between sessions",
            "The LLM searches the internet to give a fresh answer each time",
        ],
        "a": 2,
        "explain": "LLMs have no persistent memory between sessions. Each conversation starts completely fresh unless the application explicitly provides previous context in the prompt.",
    },
    {
        "concept_card": {
            "title": "What is a Chatbot vs an LLM?",
            "body": "A <strong>Chatbot</strong> is a conversational interface — it could be rule-based (if/else logic) or powered by an LLM. When backed by an LLM, it feels smart and flexible. When rule-based, it follows scripts. ChatGPT and Copilot are LLM-powered chatbots. The LLM is the brain; the chatbot is the interface that wraps it.",
            "analogy": "🏠 An LLM is the engine. A chatbot is the car. You interact with the car, not directly with the engine.",
        },
        "q": "An Arqiva customer service team wants to automate common billing queries. They build a tool that matches keywords and gives scripted responses. What is this?",
        "opts": [
            "An LLM — because it uses AI",
            "A rule-based chatbot — keyword matching without AI reasoning",
            "An agentic workflow — because it automates tasks",
            "A foundation model — because it handles many query types",
        ],
        "a": 1,
        "explain": "Keyword-matching scripted responses = rule-based chatbot. No LLM involved. It's fast and cheap, but can't handle anything outside its scripts.",
    },
    {
        "concept_card": {
            "title": "What is an AI Agent?",
            "body": "An <strong>AI Agent</strong> is an LLM given <em>tools</em> — the ability to search the web, call APIs, read files, or take actions. It can plan multi-step tasks and decide which tools to use. Agents can act autonomously: given a goal, they figure out the steps. Example: an agent that receives a fault report, queries the network database, drafts a ticket, and emails the team — without a human in the loop.",
            "analogy": "🤖 If an LLM is a brain, an agent is a brain with hands — it can actually do things, not just talk about them.",
        },
        "q": "Arqiva's data team wants to build a system that automatically checks for ServiceNow incidents, queries Databricks for affected devices, and sends a Slack summary — all triggered without human input. What type of AI system is this?",
        "opts": [
            "A simple chatbot — it handles multiple services",
            "A fine-tuned LLM — it's been trained on Arqiva data",
            "An AI Agent — it uses tools, takes actions, and completes a multi-step workflow autonomously",
            "A rule-based bot — it follows a fixed process",
        ],
        "a": 2,
        "explain": "Multi-step autonomous workflow using tools (ServiceNow, Databricks, Slack) = AI Agent. This is exactly the kind of use case Arqiva is exploring with LangGraph and AWS Bedrock.",
    },
    {
        "concept_card": {
            "title": "What is an Agentic Workflow?",
            "body": "An <strong>Agentic Workflow</strong> is a structured sequence of AI agent actions — plan → act → observe → decide → act again. Unlike a single LLM call, agentic workflows can loop, retry, branch, and adapt based on results. They're built with frameworks like LangGraph, AutoGen, or AWS Step Functions + Bedrock. They're powerful but need careful design to avoid runaway actions.",
            "analogy": "🔄 Like a smart project manager who breaks a task into steps, delegates to tools, checks results, and adjusts if something goes wrong.",
        },
        "q": "Which of these is an example of an AGENTIC workflow (not just a single AI call)?",
        "opts": [
            "Asking ChatGPT to rewrite an email",
            "Using Copilot to autocomplete a sentence in Word",
            "A system that receives a network alarm, diagnoses the cause by querying 3 databases, creates a ticket, and escalates if unresolved after 10 mins",
            "An LLM summarising a document when given its text",
        ],
        "a": 2,
        "explain": "An agentic workflow involves multiple steps, tool use, decision points, and loops. Summarising a document = single LLM call. The alarm → diagnose → ticket → escalate flow = agentic workflow.",
    },
    {
        "concept_card": {
            "title": "Foundation Models vs Fine-tuned Models",
            "body": "A <strong>Foundation Model</strong> (e.g. Claude, GPT-4) is a general-purpose LLM trained on broad data. A <strong>Fine-tuned Model</strong> is a foundation model further trained on specialist data — like Arqiva's incident logs, or legal documents — to improve performance on specific tasks. Fine-tuning costs money and requires data but gives more accurate domain-specific responses.",
            "analogy": "🎓 Foundation model = a university graduate. Fine-tuned = that graduate who then did a two-year specialist apprenticeship at Arqiva.",
        },
        "q": "Arqiva wants an AI that understands its specific network terminology and gives accurate answers about its infrastructure. What approach makes most sense?",
        "opts": [
            "Use a foundation model with no changes — it already knows everything",
            "Fine-tune a foundation model on Arqiva's internal documentation and incident data",
            "Build an LLM from scratch using Arqiva's data",
            "Use a rule-based chatbot — AI is too unpredictable for infrastructure queries",
        ],
        "a": 1,
        "explain": "Fine-tuning a foundation model on domain-specific data is the practical path. Building from scratch is prohibitively expensive. A general foundation model won't know Arqiva-specific terminology.",
    },
]

def render():
    stage_header(6, "LLMs, chatbots, agents — what's actually the difference?")

    if "s6_idx" not in st.session_state: st.session_state["s6_idx"] = 0
    if "s6_streak" not in st.session_state: st.session_state["s6_streak"] = 0

    idx = st.session_state.get("s6_idx", 0)
    if idx >= len(QS): _complete(); return

    q = QS[idx]
    st.progress(idx / len(QS))
    st.markdown(f"<div style='font-size:0.8rem;color:#8891A8;margin-bottom:1rem;'>Question {idx+1} of {len(QS)} · Streak 🔥{st.session_state['s6_streak']}</div>", unsafe_allow_html=True)

    # Concept card
    cc = q["concept_card"]
    st.markdown(f"""
    <div style='background:white;border:1.5px solid #B3DDD9;border-left:4px solid #00857A;
                border-radius:12px;padding:1.3rem;margin-bottom:1.2rem;
                box-shadow:0 2px 8px rgba(0,133,122,0.08);'>
        <div style='font-family:"Syne",sans-serif;font-size:1rem;font-weight:800;
                    color:#00857A;margin-bottom:0.6rem;'>📖 {cc["title"]}</div>
        <div style='font-size:0.9rem;color:#4a5168;line-height:1.7;'>{cc["body"]}</div>
        <div style='background:#E6F4F3;border-radius:8px;padding:0.7rem 1rem;margin-top:0.8rem;
                    font-size:0.88rem;color:#005c55;'>{cc["analogy"]}</div>
    </div>""", unsafe_allow_html=True)

    # Question
    sub_key = f"s6_sub_{idx}"
    submitted = st.session_state.get(sub_key)

    st.markdown(f"""
    <div style='background:#EEF1F8;border:1.5px solid #C5CCE0;border-radius:10px;
                padding:1.1rem;margin-bottom:1rem;'>
        <div style='font-size:0.95rem;font-weight:600;color:#1a2f5e;'>❓ {q["q"]}</div>
    </div>""", unsafe_allow_html=True)

    for i, opt in enumerate(q["opts"]):
        btn_key = f"s6_opt_{idx}_{i}"
        if submitted is None:
            if st.button(f"  {opt}", key=btn_key, use_container_width=True):
                st.session_state[sub_key] = i
                proc_key = f"s6_proc_{idx}"
                if not st.session_state.get(proc_key):
                    st.session_state[proc_key] = True
                    correct = (i == q["a"])
                    if correct:
                        st.session_state["s6_streak"] += 1
                        streak_b = min((st.session_state["s6_streak"]-1)*10, 40)
                        pts = 100 + streak_b
                    else:
                        st.session_state["s6_streak"] = 0
                        pts = 0
                    award_points(6, pts)
                    st.session_state[f"s6_pts_{idx}"] = pts
                    st.session_state[f"s6_correct_{idx}"] = correct
                st.rerun()
        else:
            if i == q["a"]:
                st.markdown(f"<div class='aq-alert-success' style='margin-bottom:4px;'>✓ {opt}</div>", unsafe_allow_html=True)
            elif i == submitted and i != q["a"]:
                st.markdown(f"<div class='aq-alert-error' style='margin-bottom:4px;'>✗ {opt}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='background:#F7F9FC;border:1.5px solid #E2E6EF;border-radius:8px;padding:0.7rem 1rem;margin-bottom:4px;font-size:0.9rem;color:#8891A8;'>{opt}</div>", unsafe_allow_html=True)

    if submitted is not None:
        pts = st.session_state.get(f"s6_pts_{idx}", 0)
        corr = st.session_state.get(f"s6_correct_{idx}", False)
        if corr:
            st.markdown(f"<div class='aq-alert-success' style='margin-top:0.8rem;'><strong>✅ Correct! +{pts} pts</strong><br><span style='font-weight:400;font-size:0.88rem;'>{q['explain']}</span></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='aq-alert-error' style='margin-top:0.8rem;'><strong>❌ Not quite.</strong><br><span style='font-weight:400;font-size:0.88rem;'>{q['explain']}</span></div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        next_btn(6, final=(idx+1>=len(QS)), final_label="✅ Complete Stage 6")

def _complete():
    pts = st.session_state["scores"].get(6,0)
    st.markdown(f"""<div style='text-align:center;padding:3rem;'>
        <div style='font-size:3rem;'>🤖</div>
        <div style='font-family:"Syne",sans-serif;font-size:2rem;font-weight:800;color:#1a2f5e;'>Stage 6 Complete!</div>
        <div style='font-size:2.5rem;font-family:monospace;font-weight:800;color:#00857A;'>{pts} pts</div>
        <p style='color:#4a5168;'>You now know your LLMs from your agents</p></div>""", unsafe_allow_html=True)
    if st.button("→ Stage 7: AI at Arqiva"):
        complete_stage(6); next_stage(); st.rerun()
