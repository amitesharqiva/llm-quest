"""Stage 4 — Context Window"""
import streamlit as st, time
from utils.state import award_points, complete_stage, next_stage, speed_bonus
from game_pages.shared import stage_header

PUZZLES = [
    {
        "limit": 12,
        "question": "You have a 12-token window. An engineer asks: 'How do I reset my Arqiva VPN password?' Select ONLY what the AI needs to answer this.",
        "chunks": [
            {"text": "System: You are Arqiva IT helpdesk", "tokens": 6, "relevant": True, "reason": "Essential — defines the AI's role"},
            {"text": "User: My name is James", "tokens": 5, "relevant": False, "reason": "Name isn't needed to answer a password question"},
            {"text": "User: How do I reset my Arqiva VPN password?", "tokens": 9, "relevant": True, "reason": "This IS the question — must be included"},
            {"text": "Previous: We discussed broadband speeds", "tokens": 6, "relevant": False, "reason": "Different topic, wastes precious tokens"},
        ],
        "answer_ids": [0, 2],
    },
    {
        "limit": 15,
        "question": "Context limit: 15 tokens. A colleague wants to summarise a meeting. What goes in?",
        "chunks": [
            {"text": "Meeting notes: Q3 planning, 3 actions agreed", "tokens": 8, "relevant": True, "reason": "The actual content to summarise"},
            {"text": "User: Summarise the meeting notes above", "tokens": 7, "relevant": True, "reason": "The instruction to summarise"},
            {"text": "User: I had a sandwich for lunch", "tokens": 8, "relevant": False, "reason": "Personal chit-chat, irrelevant"},
            {"text": "System: Yesterday's weather was cloudy", "tokens": 6, "relevant": False, "reason": "Totally unrelated"},
            {"text": "User: Also tell me a joke", "tokens": 6, "relevant": False, "reason": "Different request, confuses the model"},
        ],
        "answer_ids": [0, 1],
    },
]

def render():
    stage_header(4, "Pack the right information — fit within the limit")

    if "s4_idx" not in st.session_state: st.session_state["s4_idx"] = 0
    idx = st.session_state.get("s4_idx", 0)
    if idx >= len(PUZZLES): _complete(); return

    pz = PUZZLES[idx]
    st.progress(idx / len(PUZZLES))
    st.markdown(f"<div style='font-size:0.8rem;color:#8891A8;margin-bottom:1rem;'>Puzzle {idx+1} of {len(PUZZLES)}</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='background:#EEF1F8;border:1.5px solid #C5CCE0;border-left:4px solid #1a2f5e;
                border-radius:8px;padding:1rem;margin-bottom:1rem;'>
        <div style='font-size:0.95rem;font-weight:600;color:#1a2f5e;'>{pz["question"]}</div>
        <div style='font-size:0.85rem;color:#C13535;margin-top:4px;font-weight:600;'>
            ⚠️ Window limit: {pz["limit"]} tokens
        </div>
    </div>""", unsafe_allow_html=True)

    sel_key = f"s4_sel_{idx}"
    if sel_key not in st.session_state: st.session_state[sel_key] = []

    selected = st.session_state[sel_key]
    total_tokens = sum(pz["chunks"][i]["tokens"] for i in selected)
    sub_key = f"s4_sub_{idx}"
    submitted = st.session_state.get(sub_key)

    # Token meter
    pct = min(total_tokens / pz["limit"] * 100, 100)
    bar_color = "#00857A" if total_tokens <= pz["limit"] else "#C13535"
    over = total_tokens > pz["limit"]
    st.markdown(f"""
    <div style='background:white;border:1.5px solid #E2E6EF;border-radius:10px;padding:1rem;margin-bottom:1rem;'>
        <div style='display:flex;justify-content:space-between;margin-bottom:6px;'>
            <span style='font-size:0.82rem;font-weight:600;color:#1a2f5e;'>Context used</span>
            <span style='font-size:0.82rem;font-family:monospace;color:{bar_color};font-weight:700;'>{total_tokens} / {pz["limit"]} tokens</span>
        </div>
        <div style='background:#EEF1F8;border-radius:6px;height:10px;'>
            <div style='background:{bar_color};width:{pct}%;height:10px;border-radius:6px;transition:width 0.3s;'></div>
        </div>
        {"<div style='color:#C13535;font-size:0.78rem;margin-top:4px;font-weight:600;'>⚠️ Over limit! Remove some chunks before submitting.</div>" if over else ""}
    </div>""", unsafe_allow_html=True)

    for i, chunk in enumerate(pz["chunks"]):
        is_sel = (i in selected)
        if submitted:
            is_correct_chunk = (i in pz["answer_ids"])
            is_wrong_pick = (is_sel and not is_correct_chunk)
            if is_correct_chunk:
                bg, border, txt = "#EAF5EF","#A8D8BC","#1A7A4A"; icon = "✓ Include"
            elif is_wrong_pick:
                bg, border, txt = "#FCEAEA","#EFBCBC","#C13535"; icon = "✗ Not needed"
            else:
                bg, border, txt = "#F7F9FC","#E2E6EF","#8891A8"; icon = "○"
        else:
            bg = "#E6F4F3" if is_sel else "white"
            border = "#00857A" if is_sel else "#E2E6EF"
            txt = "#1a2f5e"
            icon = "◉ Selected" if is_sel else "○ Select"

        col1, col2 = st.columns([6, 1])
        with col1:
            reason_html = f'<span style="font-size:0.76rem;color:{txt};opacity:0.8;margin-left:6px;"> — {chunk["reason"]}</span>' if submitted else ""
            st.markdown(f"""
            <div style='background:{bg};border:1.5px solid {border};border-radius:8px;
                        padding:0.8rem 1rem;margin-bottom:5px;display:flex;justify-content:space-between;align-items:center;'>
                <div style='flex:1;'>
                    <span style='font-size:0.88rem;color:{txt};font-family:"DM Mono",monospace;'>{chunk["text"]}</span>
                    {reason_html}
                </div>
                <div style='display:flex;align-items:center;gap:10px;flex-shrink:0;margin-left:12px;'>
                    <span style='font-size:0.75rem;color:#8891A8;font-family:monospace;'>{chunk["tokens"]} tok</span>
                    <span style='font-size:0.72rem;color:{txt};font-weight:600;'>{icon}</span>
                </div>
            </div>""", unsafe_allow_html=True)
        with col2:
            if not submitted:
                lbl = "Remove" if is_sel else "Add"
                if st.button(lbl, key=f"s4_tog_{idx}_{i}", use_container_width=True):
                    if is_sel: st.session_state[sel_key].remove(i)
                    else: st.session_state[sel_key].append(i)
                    st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if not submitted:
        can = total_tokens <= pz["limit"] and len(selected) > 0
        if st.button("✅ Lock in my selection", disabled=not can, key=f"s4_submit_{idx}"):
            st.session_state[sub_key] = True
            proc_key = f"s4_proc_{idx}"
            if not st.session_state.get(proc_key):
                st.session_state[proc_key] = True
                correct = set(selected) == set(pz["answer_ids"])
                if correct:
                    bonus = speed_bonus(st.session_state.get("stage_start_time", time.time()))
                    pts = 150 + bonus
                else:
                    pts = 0
                award_points(4, pts)
                st.session_state[f"s4_pts_{idx}"] = pts
                st.session_state[f"s4_correct_{idx}"] = correct
            st.rerun()
    else:
        pts = st.session_state.get(f"s4_pts_{idx}", 0)
        corr = st.session_state.get(f"s4_correct_{idx}", False)
        correct_texts = [pz["chunks"][i]["text"] for i in pz["answer_ids"]]
        if corr:
            st.markdown(f"<div class='aq-alert-success'><strong>✅ Perfect selection! +{pts} pts</strong><br>You packed exactly the right context — the model would have everything it needs.</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='aq-alert-error'><strong>❌ Not quite.</strong> The optimal chunks were: {' + '.join([f'\"{t}\"' for t in correct_texts])}</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        final = (idx+1 >= len(PUZZLES))
        if final:
            if st.button("✅ Complete Stage 4"):
                complete_stage(4); next_stage(); st.rerun()
        else:
            if st.button("→ Next Puzzle", key=f"s4_nxt_{idx}"):
                st.session_state["s4_idx"] += 1
                st.session_state["stage_start_time"] = time.time()
                st.rerun()

def _complete():
    pts = st.session_state["scores"].get(4,0)
    st.markdown(f"""<div style='text-align:center;padding:3rem;'>
        <div style='font-size:3rem;'>📦</div>
        <div style='font-family:"Syne",sans-serif;font-size:2rem;font-weight:800;color:#1a2f5e;'>Stage 4 Complete!</div>
        <div style='font-size:2.5rem;font-family:monospace;font-weight:800;color:#00857A;'>{pts} pts</div>
        <p style='color:#4a5168;'>Context window mastered</p></div>""", unsafe_allow_html=True)
    if st.button("→ Stage 5: Hallucination Hunter"):
        complete_stage(4); next_stage(); st.rerun()
