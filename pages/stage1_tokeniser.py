import streamlit as st
import time
from utils.state import award_points, complete_stage, next_stage, speed_bonus

# Token colour palette cycling
TOKEN_COLORS = [
    ("#7c6af7", "#2a1f5a"),
    ("#f7c46a", "#5a3f1f"),
    ("#6af7c4", "#1f5a42"),
    ("#f76a6a", "#5a1f1f"),
    ("#f7a86a", "#5a3520"),
    ("#a86af7", "#3a1f5a"),
    ("#6ab4f7", "#1f3a5a"),
]

# Simplified tokenisation rules (approximating GPT-style BPE)
def simple_tokenise(text):
    """Approximate BPE tokenisation for demonstration."""
    import re
    tokens = []
    # Split on spaces but keep them attached to following word (GPT-style)
    words = re.findall(r'\s*\S+', text)
    for word in words:
        # Common subword splits
        subwords = []
        w = word.strip()
        space_prefix = "·" if word.startswith(" ") else ""

        # Numbers become individual tokens
        if w.isdigit():
            subwords = [space_prefix + w]
        # Common suffixes
        elif w.endswith("ing") and len(w) > 5:
            subwords = [space_prefix + w[:-3], "ing"]
        elif w.endswith("tion") and len(w) > 6:
            subwords = [space_prefix + w[:-4], "tion"]
        elif w.endswith("ed") and len(w) > 4:
            subwords = [space_prefix + w[:-2], "ed"]
        elif w.endswith("er") and len(w) > 4:
            subwords = [space_prefix + w[:-2], "er"]
        elif w.endswith("ly") and len(w) > 4:
            subwords = [space_prefix + w[:-2], "ly"]
        elif w.endswith("'s"):
            subwords = [space_prefix + w[:-2], "'s"]
        elif len(w) > 10:
            # Long words get split roughly in half
            mid = len(w) // 2
            subwords = [space_prefix + w[:mid], w[mid:]]
        else:
            subwords = [space_prefix + w]

        tokens.extend(subwords)
    return tokens

PUZZLES = [
    {
        "text": "Transformers are amazing!",
        "answer_count": 5,
        "hint": "Punctuation is usually its own token. 'Transformers' stays whole.",
    },
    {
        "text": "I am running quickly",
        "answer_count": 5,
        "hint": "'running' splits into 'run' + 'ning' and 'quickly' splits into 'quick' + 'ly'",
    },
    {
        "text": "ChatGPT learned from text",
        "answer_count": 6,
        "hint": "'ChatGPT' often splits at the capital G. 'learned' → 'learn' + 'ed'",
    },
]

def render():
    st.markdown("""
    <div style='display:flex; align-items:center; gap:12px; margin-bottom:1.5rem;'>
        <div style='background:rgba(124,106,247,0.15); color:#7c6af7; border:1px solid rgba(124,106,247,0.3);
                    padding:4px 14px; border-radius:20px; font-size:0.78rem; font-weight:700; letter-spacing:0.08em;'>
            STAGE 1 OF 5
        </div>
        <div style='font-size:1.6rem; font-weight:700; color:#e8e8f0;'>⚡ Token Slicer</div>
    </div>
    """, unsafe_allow_html=True)

    # Concept explainer
    st.markdown("""
    <div style='background:#13131a; border:1px solid #2a2a3a; border-left:3px solid #7c6af7;
                border-radius:12px; padding:1.2rem; margin-bottom:1.5rem;'>
        <div style='font-size:0.7rem; color:#7c6af7; font-weight:700; letter-spacing:0.1em;
                    text-transform:uppercase; margin-bottom:0.5rem;'>💡 What is a token?</div>
        <div style='color:#e8e8f0; font-size:0.92rem; line-height:1.6;'>
            LLMs don't read words — they read <strong style='color:#f7c46a;'>tokens</strong>.
            A token is a chunk of text: sometimes a whole word, sometimes part of a word, sometimes punctuation.
            <br><br>
            <code style='background:#1c1c26; padding:2px 6px; border-radius:4px; color:#6af7c4;'>
            "Transformers" → ["Transform", "ers"]
            </code>
            &nbsp;&nbsp;
            <code style='background:#1c1c26; padding:2px 6px; border-radius:4px; color:#f7c46a;'>
            "running" → ["run", "ning"]
            </code>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if "s1_puzzle_idx" not in st.session_state:
        st.session_state["s1_puzzle_idx"] = 0
        st.session_state["s1_correct"] = 0
        st.session_state["s1_revealed"] = False

    idx = st.session_state["s1_puzzle_idx"]

    if idx >= len(PUZZLES):
        _show_complete()
        return

    puzzle = PUZZLES[idx]
    text = puzzle["text"]
    correct_tokens = simple_tokenise(text)
    correct_count = len(correct_tokens)

    # Progress
    prog = idx / len(PUZZLES)
    st.progress(prog)
    st.markdown(f"<div style='font-size:0.8rem; color:#9090a8; margin-bottom:1rem;'>Puzzle {idx+1} of {len(PUZZLES)}</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown(f"""
        <div style='background:#13131a; border:1px solid #2a2a3a; border-radius:14px; padding:1.5rem; margin-bottom:1rem;'>
            <div style='font-size:0.75rem; color:#9090a8; margin-bottom:0.8rem; text-transform:uppercase; letter-spacing:0.08em;'>
                Text to tokenise
            </div>
            <div style='font-size:1.6rem; font-weight:600; font-family:"JetBrains Mono",monospace;
                        color:#e8e8f0; letter-spacing:0.02em;'>
                "{text}"
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style='font-size:0.88rem; color:#9090a8; margin-bottom:0.5rem;'>
            How many tokens does this text split into?
        </div>
        """, unsafe_allow_html=True)

        guess = st.number_input(
            "Token count",
            min_value=1, max_value=20, value=4, step=1,
            label_visibility="collapsed",
            key=f"s1_guess_{idx}"
        )

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("✅ Submit Answer", use_container_width=True, key=f"s1_submit_{idx}"):
                st.session_state[f"s1_submitted_{idx}"] = True
                st.session_state[f"s1_user_guess_{idx}"] = guess

        with col_b:
            if st.button("💡 Reveal Split", use_container_width=True, key=f"s1_reveal_{idx}"):
                st.session_state[f"s1_revealed_{idx}"] = True

    with col2:
        st.markdown("""
        <div style='background:#13131a; border:1px solid #2a2a3a; border-radius:14px; padding:1.2rem;'>
            <div style='font-size:0.75rem; color:#9090a8; margin-bottom:1rem; text-transform:uppercase; letter-spacing:0.08em;'>
                Scoring
            </div>
        """, unsafe_allow_html=True)
        scoring_html = """
            <div style='font-size:0.85rem; line-height:2;'>
                <div>🎯 Exact answer: <strong style='color:#6af7c4;'>+100 pts</strong></div>
                <div>±1 off: <strong style='color:#f7c46a;'>+50 pts</strong></div>
                <div>No hint used: <strong style='color:#7c6af7;'>+20 pts</strong></div>
                <div>Speed bonus: <strong style='color:#f7a86a;'>up to +50 pts</strong></div>
            </div>
        </div>
        """
        st.markdown(scoring_html, unsafe_allow_html=True)

    # Feedback
    if st.session_state.get(f"s1_submitted_{idx}"):
        user_guess = st.session_state.get(f"s1_user_guess_{idx}", guess)
        diff = abs(user_guess - correct_count)
        hint_used = st.session_state.get(f"s1_revealed_{idx}", False)

        if diff == 0:
            pts = 100
            if not hint_used:
                pts += 20
            bonus = speed_bonus(st.session_state.get("stage_start_time", time.time()))
            pts += bonus
            st.markdown(f"""
            <div class='alert-success' style='margin-top:1rem;'>
                <strong>✅ Exact match!</strong> The text has exactly <strong>{correct_count} tokens</strong>.<br>
                +{pts} points {f"(+{bonus} speed bonus)" if bonus > 0 else ""}
            </div>
            """, unsafe_allow_html=True)
            award_points(1, pts)
            st.session_state["s1_correct"] += 1
        elif diff == 1:
            pts = 50
            st.markdown(f"""
            <div style='background:rgba(247,196,106,0.1); border:1px solid rgba(247,196,106,0.3);
                        border-radius:10px; padding:1rem; margin-top:1rem; color:#f7c46a;'>
                <strong>⚡ Close!</strong> You guessed {user_guess}, actual is <strong>{correct_count}</strong>. +{pts} points
            </div>
            """, unsafe_allow_html=True)
            award_points(1, pts)
        else:
            st.markdown(f"""
            <div class='alert-error' style='margin-top:1rem;'>
                <strong>❌ Not quite.</strong> You guessed {user_guess}, actual is <strong>{correct_count} tokens</strong>.
            </div>
            """, unsafe_allow_html=True)

        # Auto-reveal after submit
        st.session_state[f"s1_revealed_{idx}"] = True

    # Token reveal
    if st.session_state.get(f"s1_revealed_{idx}"):
        st.markdown("<div style='margin-top:1.5rem;'>", unsafe_allow_html=True)
        st.markdown("""
        <div style='font-size:0.78rem; color:#9090a8; text-transform:uppercase;
                    letter-spacing:0.1em; margin-bottom:0.8rem;'>Token breakdown</div>
        """, unsafe_allow_html=True)

        chips_html = "<div style='display:flex; flex-wrap:wrap; gap:6px; align-items:center;'>"
        for i, tok in enumerate(correct_tokens):
            bg, border = TOKEN_COLORS[i % len(TOKEN_COLORS)]
            display = tok.replace("·", "▸")
            chips_html += f"""
            <div style='background:{border}; color:{bg}; border:1px solid {bg};
                        padding:5px 12px; border-radius:8px; font-family:monospace;
                        font-size:0.9rem; font-weight:600;'>{display}</div>
            """
        chips_html += f"<div style='color:#9090a8; font-size:0.85rem; margin-left:8px;'>= {len(correct_tokens)} tokens</div>"
        chips_html += "</div>"
        st.markdown(chips_html, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.session_state.get(f"s1_submitted_{idx}"):
            if idx + 1 < len(PUZZLES):
                if st.button("→ Next Puzzle", use_container_width=False, key=f"s1_next_{idx}"):
                    st.session_state["s1_puzzle_idx"] += 1
                    st.session_state["stage_start_time"] = time.time()
                    st.rerun()
            else:
                if st.button("→ Complete Stage", use_container_width=False, key="s1_done"):
                    complete_stage(1)
                    next_stage()
                    st.rerun()


def _show_complete():
    score = st.session_state["scores"].get(1, 0)
    st.markdown(f"""
    <div style='text-align:center; padding:3rem;'>
        <div style='font-size:3rem; margin-bottom:1rem;'>⚡</div>
        <h2 style='color:#6af7c4;'>Stage 1 Complete!</h2>
        <div style='font-size:2.5rem; font-family:monospace; color:#f7c46a; margin:1rem 0;'>{score} pts</div>
        <p style='color:#9090a8;'>You now know how LLMs see text as tokens</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("→ Next Stage: Next Word Prophet", use_container_width=False):
        complete_stage(1)
        next_stage()
        st.rerun()
