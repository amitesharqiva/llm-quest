import streamlit as st
import json, os, time

LEADERBOARD_FILE = "/tmp/llm_quest_lb_v2.json"
TOTAL_STAGES = 8

def init_state():
    defaults = {
        "page": "home",
        "player_name": "",
        "player_team": "",
        "stage": 1,
        "scores": {i: 0 for i in range(1, TOTAL_STAGES + 1)},
        "stage_complete": {i: False for i in range(1, TOTAL_STAGES + 1)},
        "start_time": None,
        "stage_start_time": None,
        "total_score": 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def get_total_score():
    return sum(st.session_state.get("scores", {}).values())

def award_points(stage, points):
    current = st.session_state["scores"].get(stage, 0)
    st.session_state["scores"][stage] = current + points
    st.session_state["total_score"] = get_total_score()

def speed_bonus(stage_start_time, max_bonus=40):
    elapsed = time.time() - stage_start_time
    if elapsed < 10:   return max_bonus
    if elapsed < 20:   return int(max_bonus * 0.75)
    if elapsed < 40:   return int(max_bonus * 0.5)
    if elapsed < 90:   return int(max_bonus * 0.25)
    return 0

def complete_stage(stage):
    st.session_state["stage_complete"][stage] = True

def next_stage():
    st.session_state["stage"] += 1
    st.session_state["stage_start_time"] = time.time()
    # Reset per-stage submission flags
    for key in list(st.session_state.keys()):
        if key.startswith(f"s{st.session_state['stage'] - 1}_"):
            pass  # keep history, just move forward

def save_to_leaderboard():
    name  = st.session_state.get("player_name", "Unknown")
    team  = st.session_state.get("player_team", "")
    score = get_total_score()
    elapsed = int(time.time() - st.session_state["start_time"]) if st.session_state.get("start_time") else 0
    stages_done = sum(1 for v in st.session_state.get("stage_complete", {}).values() if v)

    try:
        board = json.loads(open(LEADERBOARD_FILE).read()) if os.path.exists(LEADERBOARD_FILE) else []
    except Exception:
        board = []

    existing = next((e for e in board if e["name"] == name), None)
    if existing:
        if score > existing["score"]:
            existing.update({"score": score, "time": elapsed, "stages": stages_done, "team": team})
    else:
        board.append({"name": name, "team": team, "score": score, "time": elapsed, "stages": stages_done})

    board.sort(key=lambda x: (-x["score"], x["time"]))
    try:
        with open(LEADERBOARD_FILE, "w") as f:
            json.dump(board[:30], f)
    except Exception:
        pass
    return board

def load_leaderboard():
    try:
        if os.path.exists(LEADERBOARD_FILE):
            return json.loads(open(LEADERBOARD_FILE).read())
    except Exception:
        pass
    return []

def get_rank(name):
    for i, e in enumerate(load_leaderboard()):
        if e["name"] == name:
            return i + 1
    return None
