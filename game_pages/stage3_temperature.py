"""Stage 3 — Temperature Lab"""
import streamlit as st, time
from utils.state import award_points, complete_stage, next_stage
from game_pages.shared import stage_header, next_btn

SCENARIOS = [
    {
        "prompt": "The 2+2 equals",
        "q": "For a maths or factual question, what temperature should you use?",
        "answer": 0.0,
        "outputs": {
            0.0: ["4","4","4"],
            0.5: ["4","4 (the standard answer)","4, always"],
            1.0: ["4","four","well it depends..."],
            2.0: ["17","eleventy","yes"],
        },
        "explain": "Factual questions have one correct answer. Temperature 0 ensures the model always picks the most likely (correct) token.",
    },
    {
        "prompt": "Write a tagline for Arqiva's new AI platform",
        "q": "For creative marketing copy, which temperature gives the best output?",
        "answer": 1.0,
        "outputs": {
            0.0: ["Arqiva: AI for broadcast.","Arqiva: AI for broadcast.","Arqiva: AI for broadcast."],
            0.5: ["Connecting intelligence. Powering tomorrow.","Where networks meet AI.","Smarter signals, smarter world."],
            1.0: ["Broadcast reimagined. Intelligence amplified.","Where every signal tells a story.","Arqiva: the infrastructure of intelligent Britain."],
            2.0: ["SIGNAL WIZARD POTATO","Broadcast: now with feelings!","Arqiva!! (beep boop revolution)"],
        },
        "explain": "Temperature 1.0 is the sweet spot for creative tasks — imaginative but still coherent. 0 is repetitive, 2 is gibberish.",
    },
    {
        "prompt": "Summarise this safety policy for our engineers",
        "q": "For summarising an important document, what temperature is safest?",
        "answer": 0.5,
        "outputs": {
            0.0: ["The policy requires all engineers to follow safety protocol 7.","The policy requires all engineers to follow safety protocol 7.","The policy requires all engineers to follow safety protocol 7."],
            0.5: ["Engineers must follow safety protocol 7, complete annual training, and report incidents within 24 hours.","Safety protocol 7 outlines required training, incident reporting, and PPE standards for all engineering staff.","The policy mandates protocol 7 compliance, annual refresher training, and prompt incident reporting."],
            1.0: ["Engineers should probably read this and follow the gist of it.","Safety is important, and this document says so clearly.","The policy is quite firm about protocol matters."],
            2.0: ["Safety = good vibes only, wear hats!","Engineers must interpret the document's soul.","Protocol 7 demands your emotional attention."],
        },
        "explain": "Temperature 0.5 gives accurate, varied-but-reliable summaries. Too low = robotic repetition. Too high = imprecise and risky for important content.",
    },
]

def render():
    stage_header(3, "Dial the temperature — see how AI output changes")

    if "s3_idx" not in st.session_state: st.session_state["s3_idx"] = 0
    idx = st.session_state.get("s3_idx", 0)
    if idx >= len(SCENARIOS): _complete(); return

    sc = SCENARIOS[idx]
    st.progress(idx / len(SCENARIOS))
    st.markdown(f"<div style='font-size:0.8rem;color:#8891A8;margin-bottom:1rem;'>Scenario {idx+1} of {len(SCENARIOS)}</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='background:white;border:1.5px solid #E2E6EF;border-radius:12px;padding:1.2rem;margin-bottom:1rem;'>
        <span style='font-size:0.72rem;color:#8891A8;text-transform:uppercase;letter-spacing:0.1em;'>Prompt: </span>
        <span style='font-size:1rem;font-weight:600;color:#1a2f5e;font-family:"DM Mono",monospace;'>"{sc["prompt"]}"</span>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 3])
    with col1:
        temp_map = {0.0:"🧊 0.0 — Deterministic", 0.5:"😊 0.5 — Balanced", 1.0:"🔥 1.0 — Creative", 2.0:"💥 2.0 — Chaotic"}
        sel = st.radio("Temperature:", [0.0,0.5,1.0,2.0], format_func=lambda x: temp_map[x], key=f"s3_temp_{idx}")
        colors = {0.0:"#0070CC",0.5:"#00857A",1.0:"#E8580A",2.0:"#C13535"}
        c = colors[sel]
        st.markdown(f"""
        <div style='background:white;border:2px solid {c};border-radius:10px;
                    padding:1rem;text-align:center;margin-top:0.5rem;'>
            <div style='font-family:"DM Mono",monospace;font-size:2.5rem;font-weight:700;color:{c};'>{sel}</div>
            <div style='font-size:0.72rem;color:#8891A8;margin-top:2px;'>temperature setting</div>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("<div style='font-size:0.72rem;color:#8891A8;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.6rem;'>Sample outputs at this temperature</div>", unsafe_allow_html=True)
        colors2 = {0.0:"#0070CC",0.5:"#00857A",1.0:"#E8580A",2.0:"#C13535"}
        for i, out in enumerate(sc["outputs"][sel]):
            st.markdown(f"""
            <div style='background:white;border:1.5px solid #E2E6EF;border-left:3px solid {colors2[sel]};
                        border-radius:8px;padding:0.8rem 1rem;margin-bottom:6px;
                        font-size:0.9rem;color:#1a2f5e;'>
                <span style='font-size:0.72rem;font-family:monospace;color:#8891A8;'>run {i+1}:</span><br>{out}
            </div>""", unsafe_allow_html=True)

    # Answer
    sub_key = f"s3_sub_{idx}"
    st.markdown(f"<div style='font-size:0.95rem;font-weight:600;color:#1a2f5e;margin:1rem 0 0.5rem;'>{sc['q']}</div>", unsafe_allow_html=True)
    choice = st.radio("Your answer:", [0.0,0.5,1.0,2.0], format_func=lambda x: temp_map[x], key=f"s3_ans_{idx}", label_visibility="collapsed")

    if not st.session_state.get(sub_key):
        if st.button("✅ Submit Answer", key=f"s3_submit_{idx}"):
            st.session_state[sub_key] = choice
            proc_key = f"s3_proc_{idx}"
            if not st.session_state.get(proc_key):
                st.session_state[proc_key] = True
                correct = (choice == sc["answer"])
                pts = 120 if correct else 0
                award_points(3, pts)
                st.session_state[f"s3_pts_{idx}"] = pts
                st.session_state[f"s3_correct_{idx}"] = correct
            st.rerun()
    else:
        pts = st.session_state.get(f"s3_pts_{idx}", 0)
        corr = st.session_state.get(f"s3_correct_{idx}", False)
        if corr:
            st.markdown(f"<div class='aq-alert-success' style='margin-top:1rem;'><strong>✅ Correct! +{pts} pts</strong><br><span style='font-weight:400;font-size:0.88rem;'>{sc['explain']}</span></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='aq-alert-error' style='margin-top:1rem;'><strong>❌ Best answer: Temperature {sc['answer']}</strong><br><span style='font-weight:400;font-size:0.88rem;'>{sc['explain']}</span></div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        next_btn(3, final=(idx+1>=len(SCENARIOS)), final_label="✅ Complete Stage 3")

def _complete():
    pts = st.session_state["scores"].get(3,0)
    st.markdown(f"""<div style='text-align:center;padding:3rem;'>
        <div style='font-size:3rem;'>🌡️</div>
        <div style='font-family:"Syne",sans-serif;font-size:2rem;font-weight:800;color:#1a2f5e;'>Stage 3 Complete!</div>
        <div style='font-size:2.5rem;font-family:monospace;font-weight:800;color:#00857A;'>{pts} pts</div>
        <p style='color:#4a5168;'>You can now tune AI like an engineer</p></div>""", unsafe_allow_html=True)
    if st.button("→ Stage 4: Context Window"):
        complete_stage(3); next_stage(); st.rerun()
