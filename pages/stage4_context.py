import streamlit as st
import time
from utils.state import award_points, complete_stage, next_stage, speed_bonus

PUZZLES = [
    {
        "window": 10,
        "question": "An LLM has a 10-token context window. Which chunks of this conversation should you keep to answer 'What is my name?'",
        "chunks": [
            {"text": "User: Hi, my name is Ami", "tokens": 6, "relevant": True, "reason": "Contains the name"},
            {"text": "User: I love pizza", "tokens": 5, "relevant": False, "reason": "Irrelevant to name question"},
            {"text": "User: What is the weather?", "tokens": 6, "relevant": False, "reason": "Different topic"},
            {"text": "Assistant: The weather is nice today", "tokens": 7, "relevant": False, "reason": "Weather response, not needed"},
            {"text": "User: What is my name?", "tokens": 6, "relevant": True, "reason": "The question itself"},
        ],
        "answer_ids": [0, 4],
    },
    {
        "window": 15,
        "question": "Context window: 15 tokens. You need to answer a Python coding question. Which context fits?",
        "chunks": [
            {"text": "System: You are a Python expert", "tokens": 6, "relevant": True, "reason": "Essential system instruction"},
            {"text": "User: I had cereal for breakfast", "tokens": 7, "relevant": False, "reason": "Irrelevant personal info"},
            {"text": "User: How do I write a for loop?", "tokens": 8, "relevant": True, "reason": "The actual question"},
            {"text": "Assistant: Yesterday I discussed Java", "tokens": 6, "relevant": False, "reason": "Different language, irrelevant"},
            {"text": "User: The sky is blue", "tokens": 5, "relevant": False, "reason": "Completely unrelated"},
        ],
        "answer_ids": [0, 2],
    },
]

def render():
    st.markdown("""
    <div style='display:flex; align-items:center; gap:12px; margin-bottom:1.5rem;'>
        <div style='background:rgba(247,106,106,0.15); color:#f76a6a; border:1px solid rgba(247,106,106,0.3);
                    padding:4px 14px; border-radius:20px; font-size:0.78rem; font-weight:700; letter-spacing:0.08em;'>
            STAGE 4 OF 5
        </div>
        <div style='font-size:1.6rem; font-weight:700; color:#e8e8f0;'>📦 Context Window</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='background:#13131a; border:1px solid #2a2a3a; border-left:3px solid #f76a6a;
                border-radius:12px; padding:1.2rem; margin-bottom:1.5rem;'>
        <div style='font-size:0.7rem; color:#f76a6a; font-weight:700; letter-spacing:0.1em;
                    text-transform:uppercase; margin-bottom:0.5rem;'>💡 What is a context window?</div>
        <div style='color:#e8e8f0; font-size:0.92rem; line-height:1.6;'>
            An LLM can only "see" a limited number of tokens at once — its <strong style='color:#f76a6a;'>context window</strong>.
            GPT-4 has ~128,000 tokens. Claude has ~200,000. But what goes inside matters.
            Too much irrelevant text leaves no room for what actually matters.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if "s4_puzzle_idx" not in st.session_state:
        st.session_state["s4_puzzle_idx"] = 0

    idx = st.session_state["s4_puzzle_idx"]

    if idx >= len(PUZZLES):
        _show_complete()
        return

    puzzle = PUZZLES[idx]
    window_size = puzzle["window"]
    chunks = puzzle["chunks"]

    st.progress(idx / len(PUZZLES))
    st.markdown(f"<div style='font-size:0.8rem; color:#9090a8; margin-bottom:1.5rem;'>Puzzle {idx+1} of {len(PUZZLES)}</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='background:#13131a; border:1px solid #f76a6a33; border-radius:12px; padding:1.2rem; margin-bottom:1rem;'>
        <div style='font-size:0.95rem; color:#e8e8f0; margin-bottom:0.5rem;'>{puzzle["question"]}</div>
        <div style='font-size:0.85rem; color:#f76a6a;'>Context window limit: <strong>{window_size} tokens</strong></div>
    </div>
    """, unsafe_allow_html=True)

    selected_key = f"s4_selected_{idx}"
    if selected_key not in st.session_state:
        st.session_state[selected_key] = []

    selected = st.session_state[selected_key]
    total_tokens = sum(chunks[i]["tokens"] for i in selected)
    submitted_key = f"s4_submitted_{idx}"

    # Token meter
    pct = min(total_tokens / window_size * 100, 100)
    bar_color = "#6af7c4" if total_tokens <= window_size else "#f76a6a"
    st.markdown(f"""
    <div style='margin-bottom:1rem;'>
        <div style='display:flex; justify-content:space-between; margin-bottom:4px;'>
            <span style='font-size:0.8rem; color:#9090a8;'>Context used</span>
            <span style='font-size:0.8rem; font-family:monospace; color:{bar_color};'>{total_tokens} / {window_size} tokens</span>
        </div>
        <div style='background:#2a2a3a; border-radius:6px; height:10px;'>
            <div style='background:{bar_color}; width:{pct}%; height:10px; border-radius:6px; transition:width 0.3s;'></div>
        </div>
        {"<div style='color:#f76a6a; font-size:0.78rem; margin-top:4px;'>⚠️ Over limit! Deselect some chunks.</div>" if total_tokens > window_size else ""}
    </div>
    """, unsafe_allow_html=True)

    # Chunk selector
    st.markdown("<div style='font-size:0.82rem; color:#9090a8; margin-bottom:0.5rem;'>Select which chunks to include (toggle on/off):</div>", unsafe_allow_html=True)

    for i, chunk in enumerate(chunks):
        is_selected = i in selected
        is_submitted = st.session_state.get(submitted_key)

        if is_submitted:
            correct_ids = puzzle["answer_ids"]
            if i in correct_ids:
                bg = "rgba(106,247,196,0.1)"
                border = "#6af7c4"
                icon = "✓"
                label_color = "#6af7c4"
            elif is_selected and i not in correct_ids:
                bg = "rgba(247,106,106,0.1)"
                border = "#f76a6a"
                icon = "✗"
                label_color = "#f76a6a"
            else:
                bg = "#1c1c26"
                border = "#2a2a3a"
                icon = "○"
                label_color = "#9090a8"
        else:
            bg = "rgba(124,106,247,0.1)" if is_selected else "#1c1c26"
            border = "#7c6af7" if is_selected else "#2a2a3a"
            icon = "◉" if is_selected else "○"
            label_color = "#7c6af7" if is_selected else "#9090a8"

        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"""
            <div style='background:{bg}; border:1px solid {border}; border-radius:8px;
                        padding:0.8rem 1rem; margin-bottom:6px; display:flex; justify-content:space-between; align-items:center;'>
                <div>
                    <span style='color:{label_color}; font-size:1rem; margin-right:8px;'>{icon}</span>
                    <span style='font-size:0.88rem; color:#e8e8f0; font-family:monospace;'>{chunk["text"]}</span>
                    {f'<span style="font-size:0.78rem; color:#9090a8; margin-left:8px;">({chunk["reason"]})</span>' if is_submitted else ''}
                </div>
                <span style='font-size:0.78rem; color:#9090a8; font-family:monospace; flex-shrink:0; margin-left:8px;'>
                    {chunk["tokens"]}tok
                </span>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if not is_submitted:
                if st.button("Select" if not is_selected else "Remove", key=f"s4_toggle_{idx}_{i}", use_container_width=True):
                    if is_selected:
                        st.session_state[selected_key].remove(i)
                    else:
                        st.session_state[selected_key].append(i)
                    st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    if not st.session_state.get(submitted_key):
        can_submit = total_tokens <= window_size and len(selected) > 0
        if st.button("✅ Lock in Selection", disabled=not can_submit, key=f"s4_submit_{idx}"):
            st.session_state[submitted_key] = True
            correct_ids = set(puzzle["answer_ids"])
            user_ids = set(selected)
            if user_ids == correct_ids:
                pts = 150
                bonus = speed_bonus(st.session_state.get("stage_start_time", time.time()))
                pts += bonus
                award_points(4, pts)
                st.session_state[f"s4_pts_{idx}"] = pts
                st.session_state[f"s4_correct_{idx}"] = True
            else:
                st.session_state[f"s4_pts_{idx}"] = 0
                st.session_state[f"s4_correct_{idx}"] = False
            st.rerun()
    else:
        pts = st.session_state.get(f"s4_pts_{idx}", 0)
        correct = st.session_state.get(f"s4_correct_{idx}", False)
        correct_ids = puzzle["answer_ids"]
        correct_texts = [chunks[i]["text"] for i in correct_ids]

        if correct:
            st.markdown(f"""
            <div class='alert-success'>
                <strong>✅ Perfect selection! +{pts} pts</strong><br>
                You packed exactly the right context.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='alert-error'>
                <strong>❌ Not quite.</strong> Optimal chunks were: {" + ".join([f'"{t}"' for t in correct_texts])}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if idx + 1 < len(PUZZLES):
            if st.button("→ Next Puzzle", key=f"s4_next_{idx}"):
                st.session_state["s4_puzzle_idx"] += 1
                st.session_state["stage_start_time"] = time.time()
                st.rerun()
        else:
            if st.button("→ Complete Stage", key="s4_done"):
                complete_stage(4)
                next_stage()
                st.rerun()


def _show_complete():
    score = st.session_state["scores"].get(4, 0)
    st.markdown(f"""
    <div style='text-align:center; padding:3rem;'>
        <div style='font-size:3rem; margin-bottom:1rem;'>📦</div>
        <h2 style='color:#f76a6a;'>Stage 4 Complete!</h2>
        <div style='font-size:2.5rem; font-family:monospace; color:#f7c46a; margin:1rem 0;'>{score} pts</div>
        <p style='color:#9090a8;'>Context window management: unlocked</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("→ Final Stage: Hallucination Hunter"):
        complete_stage(4)
        next_stage()
        st.rerun()
