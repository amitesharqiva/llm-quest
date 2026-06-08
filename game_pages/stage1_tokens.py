import streamlit as st, time
from utils.state import award_points, complete_stage, next_stage, speed_bonus
from game_pages.shared import stage_header

TOKEN_COLORS = ["#00857A","#1a2f5e","#E8580A","#C49A2A","#6B3FA0","#C13535","#0070CC","#1A7A4A"]
TOKEN_BG     = ["#E6F4F3","#EEF1F8","#FEF0E9","#FDF5E1","#F2EEF9","#FCEAEA","#E8F4FE","#EAF5EF"]

def approx_tokenise(text):
    import re
    tokens = []
    words = re.findall(r"\s*\S+", text)
    for word in words:
        w = word.strip()
        sp = "·" if word.startswith(" ") else ""
        if w.isdigit():
            tokens.append(sp + w)
        elif w.endswith("ing") and len(w) > 5:
            tokens += [sp + w[:-3], "ing"]
        elif w.endswith("tion") and len(w) > 6:
            tokens += [sp + w[:-4], "tion"]
        elif w.endswith("'s"):
            tokens += [sp + w[:-2], "'s"]
        elif w.endswith("ed") and len(w) > 4:
            tokens += [sp + w[:-2], "ed"]
        elif w.endswith("ly") and len(w) > 4:
            tokens += [sp + w[:-2], "ly"]
        elif len(w) > 11:
            mid = len(w) // 2
            tokens += [sp + w[:mid], w[mid:]]
        else:
            tokens.append(sp + w)
    return tokens

PUZZLES = [
    {"text": "AI is amazing!", "hint": "Punctuation is its own token. 'AI' = 1 token."},
    {"text": "I am learning quickly", "hint": "'quickly' → 'quick' + 'ly'. Count spaces too."},
    {"text": "ChatGPT was trained on text", "hint": "'ChatGPT' often splits. 'trained' → 'train'+'ed'."},
    {"text": "The transformer architecture changed everything", "hint": "'transformer' = 1 word but 'everything' may split."},
]

def render():
    stage_header(1, "How many pieces does AI chop this text into?")

    if "s1_idx" not in st.session_state:
        st.session_state["s1_idx"] = 0

    idx = st.session_state.get("s1_idx", 0)
    if idx >= len(PUZZLES):
        _complete(); return

    puzzle = PUZZLES[idx]
    tokens = approx_tokenise(puzzle["text"])
    correct = len(tokens)

    st.progress(idx / len(PUZZLES))
    st.markdown(f"<div style='font-size:0.8rem;color:#8891A8;margin-bottom:1rem;'>Puzzle {idx+1} of {len(PUZZLES)}</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown(f"""
        <div style='background:white; border:1.5px solid #E2E6EF; border-radius:12px;
                    padding:1.5rem; margin-bottom:1rem; box-shadow:0 2px 8px rgba(26,47,94,0.05);'>
            <div style='font-size:0.72rem; color:#8891A8; text-transform:uppercase;
                        letter-spacing:0.1em; margin-bottom:0.6rem;'>Text to tokenise</div>
            <div style='font-family:"DM Mono",monospace; font-size:1.5rem; font-weight:600;
                        color:#1a2f5e; padding:0.8rem; background:#F7F9FC;
                        border-radius:8px; border:1.5px solid #E2E6EF;'>
                "{puzzle["text"]}"
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='font-size:0.9rem; font-weight:600; color:#1a2f5e; margin-bottom:0.5rem;'>How many tokens is this?</div>", unsafe_allow_html=True)

        guess = st.number_input("tokens", min_value=1, max_value=25, value=4, step=1, label_visibility="collapsed", key=f"s1_guess_{idx}")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Submit", use_container_width=True, key=f"s1_sub_{idx}"):
                st.session_state[f"s1_submitted_{idx}"] = guess
                st.session_state[f"s1_revealed_{idx}"] = True
        with c2:
            if st.button("💡 Show split", use_container_width=True, key=f"s1_hint_{idx}"):
                st.session_state[f"s1_revealed_{idx}"] = True

    with col2:
        st.markdown(f"""
        <div style='background:#EEF1F8; border:1.5px solid #C5CCE0; border-radius:12px; padding:1.2rem;'>
            <div style='font-size:0.72rem; color:#1a2f5e; font-weight:700; text-transform:uppercase;
                        letter-spacing:0.1em; margin-bottom:0.8rem;'>Scoring</div>
            <div style='font-size:0.85rem; color:#4a5168; line-height:2;'>
                🎯 Exact: <strong style='color:#1A7A4A;'>+100 pts</strong><br>
                ±1 off: <strong style='color:#C49A2A;'>+50 pts</strong><br>
                ⚡ Speed: <strong style='color:#E8580A;'>up to +40 pts</strong><br>
                💡 Hint used: <strong style='color:#8891A8;'>no penalty</strong>
            </div>
            <div style='margin-top:0.8rem; background:white; border-radius:8px;
                        padding:0.7rem; font-size:0.8rem; color:#4a5168; border:1px solid #E2E6EF;'>
                <strong>Hint:</strong> {puzzle["hint"]}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Feedback
    if st.session_state.get(f"s1_submitted_{idx}") is not None:
        user = st.session_state[f"s1_submitted_{idx}"]
        diff = abs(user - correct)
        processed_key = f"s1_proc_{idx}"
        if not st.session_state.get(processed_key):
            st.session_state[processed_key] = True
            if diff == 0:
                bonus = speed_bonus(st.session_state.get("stage_start_time", time.time()))
                pts = 100 + bonus
            elif diff == 1:
                pts = 50
            else:
                pts = 0
            award_points(1, pts)
            st.session_state[f"s1_pts_{idx}"] = pts

        pts = st.session_state.get(f"s1_pts_{idx}", 0)
        if diff == 0:
            st.markdown(f"<div class='aq-alert-success' style='margin-top:1rem;'>✅ Exact! The answer is <strong>{correct} tokens</strong>. +{pts} pts</div>", unsafe_allow_html=True)
        elif diff == 1:
            st.markdown(f"<div style='background:#FDF5E1;border:1.5px solid #E8D9A0;border-left:4px solid #C49A2A;border-radius:8px;padding:1rem;margin-top:1rem;color:#7A5A10;'>⚡ Close! You said {user}, answer is <strong>{correct}</strong>. +{pts} pts</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='aq-alert-error' style='margin-top:1rem;'>❌ The answer is <strong>{correct} tokens</strong>. +0 pts — keep going!</div>", unsafe_allow_html=True)

    # Token reveal
    if st.session_state.get(f"s1_revealed_{idx}"):
        st.markdown("<div style='font-size:0.78rem;color:#8891A8;text-transform:uppercase;letter-spacing:0.1em;margin:1.2rem 0 0.5rem;'>Token breakdown</div>", unsafe_allow_html=True)
        chips = ""
        for i, tok in enumerate(tokens):
            c = TOKEN_COLORS[i % len(TOKEN_COLORS)]
            bg = TOKEN_BG[i % len(TOKEN_BG)]
            display = tok.replace("·", "▸ ")
            chips += f"<span style='background:{bg};color:{c};border:1.5px solid {c}33;padding:4px 11px;border-radius:6px;font-family:monospace;font-size:0.88rem;font-weight:600;margin:2px;display:inline-block;'>{display}</span> "
        chips += f"<span style='font-size:0.82rem;color:#8891A8;margin-left:6px;font-weight:600;'>= {len(tokens)} tokens</span>"
        st.markdown(f"<div style='background:white;border:1.5px solid #E2E6EF;border-radius:10px;padding:1rem;'>{chips}</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        if st.session_state.get(f"s1_submitted_{idx}") is not None:
            if idx + 1 < len(PUZZLES):
                if st.button("→ Next Puzzle", key=f"s1_nxt_{idx}"):
                    st.session_state["s1_idx"] += 1
                    st.session_state["stage_start_time"] = time.time()
                    st.rerun()
            else:
                if st.button("✅ Complete Stage 1", key="s1_done"):
                    complete_stage(1); next_stage(); st.rerun()

def _complete():
    pts = st.session_state["scores"].get(1, 0)
    st.markdown(f"""
    <div style='text-align:center;padding:3rem;'>
        <div style='font-size:3rem;'>⚡</div>
        <div style='font-family:"Syne",sans-serif;font-size:2rem;font-weight:800;color:#1a2f5e;margin:0.5rem 0;'>Stage 1 Complete!</div>
        <div style='font-size:2.5rem;font-family:monospace;font-weight:800;color:#00857A;'>{pts} pts</div>
        <p style='color:#4a5168;margin-top:0.5rem;'>You now understand how LLMs chop text into tokens</p>
    </div>""", unsafe_allow_html=True)
    if st.button("→ Stage 2: Word Prediction"):
        complete_stage(1); next_stage(); st.rerun()
