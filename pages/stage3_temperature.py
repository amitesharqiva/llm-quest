import streamlit as st
import random
import time
from utils.state import award_points, complete_stage, next_stage

# Simulated outputs at different temperatures
SCENARIOS = [
    {
        "prompt": "The weather today is",
        "outputs": {
            0.0: ["sunny and clear", "sunny and clear", "sunny and clear"],
            0.5: ["sunny with light clouds", "warm and breezy", "partly cloudy"],
            1.0: ["a confusing mix of hail and butterflies", "absolutely volcanic", "purple with determination"],
            2.0: ["GLORP! The sun ate my umbrella", "weather is a conspiracy by spoons", "43 degrees of chaos penguin"],
        },
        "question": "Which temperature setting would make an AI weather assistant most useful?",
        "answer": 0.5,
        "explanation": "Temperature 0.5 gives sensible but slightly varied responses. 0.0 is robotic/repetitive, 1.0+ gets unreliable, 2.0 is nonsense."
    },
    {
        "prompt": "Write me a poem about the sea",
        "outputs": {
            0.0: ["The sea is blue. The waves are there. The water is wet. The sea is fair.", "The sea is blue. The waves are there. The water is wet. The sea is fair.", "The sea is blue. The waves are there. The water is wet. The sea is fair."],
            0.5: ["Waves crash upon the ancient shore, each tide a story, evermore.", "The ocean breathes in salt and foam, a restless wanderer, always home.", "Blue depths hold secrets, cold and deep, where ancient creatures slowly sleep."],
            1.0: ["Brine-kissed horizons swallow the moon's ambitions whole.", "The sea devours time like a patient philosopher.", "Salt remembers everything the rivers forgot."],
            2.0: ["Squid astronaut! Waves of purple Thursday. Fish remember Tuesday backwards.", "Ocean: the original Wi-Fi. Sharks download dreams at 4G speed.", "Blue wet thing goes whoosh. Crab says existential crisis. Salt."],
        },
        "question": "For creative writing, which temperature gives the best results?",
        "answer": 1.0,
        "explanation": "Temperature 1.0 is ideal for creative tasks — it produces vivid, original writing. 0.0 is boring, 2.0 becomes incoherent."
    },
    {
        "prompt": "2 + 2 =",
        "outputs": {
            0.0: ["4", "4", "4"],
            0.5: ["4", "4", "4 (as expected in standard arithmetic)"],
            1.0: ["4", "four", "well, it depends on the base..."],
            2.0: ["17", "eleventy-fish", "yes"],
        },
        "question": "For maths and factual answers, which temperature is best?",
        "answer": 0.0,
        "explanation": "For factual/deterministic tasks, temperature 0 is correct — there's only one right answer. Higher temperatures introduce errors."
    },
]

def simulate_output(prompt, temp, seed=42):
    """Return a sample output for the given temperature."""
    random.seed(seed + int(temp * 10))
    for scenario in SCENARIOS:
        if scenario["prompt"] == prompt:
            outputs = scenario["outputs"].get(temp, ["..."])
            return random.choice(outputs)
    return "..."

def render():
    st.markdown("""
    <div style='display:flex; align-items:center; gap:12px; margin-bottom:1.5rem;'>
        <div style='background:rgba(106,247,196,0.15); color:#6af7c4; border:1px solid rgba(106,247,196,0.3);
                    padding:4px 14px; border-radius:20px; font-size:0.78rem; font-weight:700; letter-spacing:0.08em;'>
            STAGE 3 OF 5
        </div>
        <div style='font-size:1.6rem; font-weight:700; color:#e8e8f0;'>🌡️ Temperature Lab</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='background:#13131a; border:1px solid #2a2a3a; border-left:3px solid #6af7c4;
                border-radius:12px; padding:1.2rem; margin-bottom:1.5rem;'>
        <div style='font-size:0.7rem; color:#6af7c4; font-weight:700; letter-spacing:0.1em;
                    text-transform:uppercase; margin-bottom:0.5rem;'>💡 What is temperature?</div>
        <div style='color:#e8e8f0; font-size:0.92rem; line-height:1.6;'>
            Temperature controls <strong style='color:#6af7c4;'>how random</strong> the model's output is.
            <strong style='color:#f7c46a;'>Low temp (0)</strong> = always picks the most likely token (deterministic).
            <strong style='color:#f76a6a;'>High temp (2)</strong> = picks randomly, even unlikely tokens. 
            The right temperature depends on the task.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if "s3_scenario_idx" not in st.session_state:
        st.session_state["s3_scenario_idx"] = 0
        st.session_state["s3_score"] = 0

    scenario_idx = st.session_state["s3_scenario_idx"]

    if scenario_idx >= len(SCENARIOS):
        _show_complete()
        return

    scenario = SCENARIOS[scenario_idx]
    st.progress(scenario_idx / len(SCENARIOS))
    st.markdown(f"<div style='font-size:0.8rem; color:#9090a8; margin-bottom:1.5rem;'>Scenario {scenario_idx+1} of {len(SCENARIOS)}</div>", unsafe_allow_html=True)

    # Interactive temperature dial
    st.markdown(f"""
    <div style='background:#13131a; border:1px solid #2a2a3a; border-radius:14px; padding:1.2rem; margin-bottom:1rem;'>
        <div style='font-size:0.75rem; color:#9090a8; margin-bottom:0.5rem; text-transform:uppercase; letter-spacing:0.08em;'>Prompt</div>
        <div style='font-size:1.3rem; font-weight:600; font-family:"JetBrains Mono",monospace; color:#e8e8f0;'>"{scenario["prompt"]}"</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 3])

    with col1:
        temp_options = [0.0, 0.5, 1.0, 2.0]
        temp_labels = {0.0: "🧊 0.0 — Frozen", 0.5: "😊 0.5 — Balanced", 1.0: "🔥 1.0 — Creative", 2.0: "💥 2.0 — Chaos"}

        selected_temp = st.radio(
            "Set temperature:",
            temp_options,
            format_func=lambda x: temp_labels[x],
            key=f"s3_temp_{scenario_idx}"
        )

        # Temp visual indicator
        colors = {0.0: "#6ab4f7", 0.5: "#6af7c4", 1.0: "#f7c46a", 2.0: "#f76a6a"}
        color = colors[selected_temp]
        st.markdown(f"""
        <div style='background:rgba(0,0,0,0.2); border:1px solid {color}33; border-radius:10px;
                    padding:1rem; margin-top:0.5rem; text-align:center;'>
            <div style='font-size:2.5rem; font-family:monospace; font-weight:700; color:{color};'>{selected_temp}</div>
            <div style='font-size:0.75rem; color:#9090a8; margin-top:4px;'>temperature</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='font-size:0.78rem; color:#9090a8; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:0.8rem;'>
            Sample outputs at this temperature
        </div>
        """, unsafe_allow_html=True)

        outputs = scenario["outputs"][selected_temp]
        for i, out in enumerate(outputs):
            st.markdown(f"""
            <div style='background:#1c1c26; border:1px solid #2a2a3a; border-left:3px solid {colors[selected_temp]};
                        border-radius:8px; padding:0.8rem 1rem; margin-bottom:6px; font-size:0.9rem; color:#e8e8f0;'>
                <span style='color:#9090a8; font-size:0.75rem; font-family:monospace;'>run {i+1}:</span><br>
                {out}
            </div>
            """, unsafe_allow_html=True)

    # Question
    st.markdown(f"""
    <div style='background:#13131a; border:1px solid #2a2a3a; border-radius:12px;
                padding:1.2rem; margin:1rem 0;'>
        <div style='font-size:1rem; font-weight:600; color:#e8e8f0; margin-bottom:1rem;'>
            🎯 {scenario["question"]}
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    submitted_key = f"s3_submitted_{scenario_idx}"

    answer_options = {0.0: "Temperature 0.0", 0.5: "Temperature 0.5", 1.0: "Temperature 1.0", 2.0: "Temperature 2.0"}
    chosen = st.radio(
        "Your answer:",
        [0.0, 0.5, 1.0, 2.0],
        format_func=lambda x: answer_options[x],
        key=f"s3_answer_{scenario_idx}",
        label_visibility="collapsed"
    )

    if not st.session_state.get(submitted_key):
        if st.button("✅ Submit", key=f"s3_submit_{scenario_idx}"):
            st.session_state[submitted_key] = chosen
            st.rerun()
    else:
        user_answer = st.session_state[submitted_key]
        correct = scenario["answer"]
        processed_key = f"s3_processed_{scenario_idx}"

        if not st.session_state.get(processed_key):
            st.session_state[processed_key] = True
            if user_answer == correct:
                award_points(3, 120)
                st.session_state[f"s3_pts_{scenario_idx}"] = 120
            else:
                st.session_state[f"s3_pts_{scenario_idx}"] = 0

        pts = st.session_state.get(f"s3_pts_{scenario_idx}", 0)

        if user_answer == correct:
            st.markdown(f"""
            <div class='alert-success' style='margin-top:1rem;'>
                <strong>✅ Correct! +{pts} pts</strong><br>
                <span style='font-size:0.88rem; opacity:0.85;'>{scenario["explanation"]}</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='alert-error' style='margin-top:1rem;'>
                <strong>❌ Not quite — the best answer was temperature {correct}</strong><br>
                <span style='font-size:0.88rem; opacity:0.85;'>{scenario["explanation"]}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if scenario_idx + 1 < len(SCENARIOS):
            if st.button("→ Next Scenario", key=f"s3_next_{scenario_idx}"):
                st.session_state["s3_scenario_idx"] += 1
                st.rerun()
        else:
            if st.button("→ Complete Stage", key="s3_done"):
                complete_stage(3)
                next_stage()
                st.rerun()


def _show_complete():
    score = st.session_state["scores"].get(3, 0)
    st.markdown(f"""
    <div style='text-align:center; padding:3rem;'>
        <div style='font-size:3rem; margin-bottom:1rem;'>🌡️</div>
        <h2 style='color:#6af7c4;'>Stage 3 Complete!</h2>
        <div style='font-size:2.5rem; font-family:monospace; color:#f7c46a; margin:1rem 0;'>{score} pts</div>
        <p style='color:#9090a8;'>You can now tune an LLM like a pro</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("→ Next Stage: Context Window"):
        complete_stage(3)
        next_stage()
        st.rerun()
