import streamlit as st
import json, os, time

LEADERBOARD_FILE = "/tmp/llm_quest_leaderboard.json"

def init_state():
    defaults = {
        "page": "home",
        "player_name": "",
        "stage": 1,
        "scores": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
        "stage_complete": {1: False, 2: False, 3: False, 4: False, 5: False},
        "start_time": None,
        "stage_start_time": None,
        "hints_used": 0,
        "total_score": 0,
        "s1_attempts": 0,
        "s2_streak": 0,
        "s2_current_q": 0,
        "s2_answers": [],
        "s3_submitted": False,
        "s4_selected": [],
        "s5_answers": {},
        "s5_current": 0,
        "submitted": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def get_total_score():
    return sum(st.session_state["scores"].values())

def award_points(stage, points, reason=""):
    current = st.session_state["scores"].get(stage, 0)
    st.session_state["scores"][stage] = current + points
    st.session_state["total_score"] = get_total_score()

def speed_bonus(stage_start_time, max_bonus=50):
    elapsed = time.time() - stage_start_time
    if elapsed < 15:
        return max_bonus
    elif elapsed < 30:
        return int(max_bonus * 0.75)
    elif elapsed < 60:
        return int(max_bonus * 0.5)
    elif elapsed < 120:
        return int(max_bonus * 0.25)
    return 0

def complete_stage(stage):
    st.session_state["stage_complete"][stage] = True

def next_stage():
    st.session_state["stage"] += 1
    st.session_state["stage_start_time"] = time.time()
    st.session_state["submitted"] = False

def save_to_leaderboard():
    name = st.session_state["player_name"]
    score = get_total_score()
    elapsed = int(time.time() - st.session_state["start_time"]) if st.session_state["start_time"] else 0

    try:
        if os.path.exists(LEADERBOARD_FILE):
            with open(LEADERBOARD_FILE, "r") as f:
                board = json.load(f)
        else:
            board = []
    except Exception:
        board = []

    # Update or add
    existing = next((e for e in board if e["name"] == name), None)
    if existing:
        if score > existing["score"]:
            existing["score"] = score
            existing["time"] = elapsed
    else:
        board.append({"name": name, "score": score, "time": elapsed})

    board.sort(key=lambda x: (-x["score"], x["time"]))

    try:
        with open(LEADERBOARD_FILE, "w") as f:
            json.dump(board[:20], f)
    except Exception:
        pass

    return board

def load_leaderboard():
    try:
        if os.path.exists(LEADERBOARD_FILE):
            with open(LEADERBOARD_FILE, "r") as f:
                return json.load(f)
    except Exception:
        pass
    return []

def get_rank(name):
    board = load_leaderboard()
    for i, entry in enumerate(board):
        if entry["name"] == name:
            return i + 1
    return None
