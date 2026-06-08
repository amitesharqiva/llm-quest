# 🧠 LLM Quest

**An interactive puzzle game that teaches how Large Language Models actually work — no AI APIs, no cloud costs, pure Python.**

Built for [Arqiva Live 2026](https://www.arqiva.com) as a live competitive learning experience. Players race through 5 stages, each revealing a core concept behind modern AI, while competing on a shared real-time leaderboard.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-red?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## What is this?

Most AI demos show you *outputs*. This game teaches you *how* — through puzzles you have to solve yourself.

Each stage is a short interactive challenge. Get it right and you score points. The leaderboard updates live across all players. Designed to run in a browser, on any laptop or phone, with no setup required from participants.

---

## The 5 Stages

| # | Stage | Mechanic | Concept |
|---|-------|----------|---------|
| 1 | ⚡ **Token Slicer** | Guess how many tokens a phrase splits into, then see the coloured breakdown | Tokenisation — LLMs don't read words, they read chunks |
| 2 | 🔮 **Next Word Prophet** | Pick what the model predicts next; probability bars reveal after you answer | Next-token prediction — the core of how LLMs generate text |
| 3 | 🌡️ **Temperature Lab** | Dial temperature from 0 → 2 and watch outputs shift from frozen to chaotic | Temperature — how randomness is controlled |
| 4 | 📦 **Context Window** | Pack the right chunks into a token budget using a live fill meter | Context limits — LLMs can only see so much at once |
| 5 | 🕵️ **Hallucination Hunter** | One of five AI-generated facts is wrong — find it before the timer runs out | Hallucination — why you should never blindly trust AI output |

---

## Scoring

| Stage | Points |
|-------|--------|
| Exact token count | 100 pts |
| Token count ±1 | 50 pts |
| No hint used | +20 pts |
| Speed bonus (any stage) | up to +50 pts |
| Correct next-word prediction | 80 pts |
| Streak bonus (per consecutive correct) | +15 pts |
| Correct temperature scenario | 120 pts |
| Correct context selection | 150 pts |
| Hallucination spotted | 150 pts |

**Max theoretical score: ~2,400 pts**

---

## Quickstart

### Run locally

```bash
git clone https://github.com/YOUR_USERNAME/llm-quest.git
cd llm-quest
pip install -r requirements.txt
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

### Run for a live event (multiple players on same network)

```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

Participants open `http://<your-machine-ip>:8501` on any device. The leaderboard syncs automatically across all sessions via a shared local file.

---

## Deploy to Streamlit Community Cloud (free, recommended)

The easiest way to run this for a group event — no server to manage, works on any device with a browser.

**1. Fork or push this repo to GitHub** (must be a public repo for the free tier)

**2. Go to [share.streamlit.io](https://share.streamlit.io)** and sign in with GitHub

**3. Click "New app"** and fill in:

| Field | Value |
|-------|-------|
| Repository | `your-username/llm-quest` |
| Branch | `main` |
| Main file path | `app.py` |

**4. Click "Deploy"** — takes about 60–90 seconds

**5. Share the URL** — it looks like `https://your-username-llm-quest-xxxx.streamlit.app`

Players open that URL on their laptops or phones, enter their name, and start playing immediately.

> **Note on the leaderboard:** Streamlit Community Cloud runs all sessions on the same server instance, so the shared leaderboard works correctly for a single event. The leaderboard data persists in `/tmp` for the duration of the session but resets if the app goes idle for ~20 minutes. For a multi-hour event, keep a browser tab open to prevent the app sleeping, or see the persistence note below.

---

## Project structure

```
llm-quest/
├── app.py                      # Entry point — routing and global CSS
├── requirements.txt
├── README.md
├── pages/
│   ├── home.py                 # Landing page and name entry
│   ├── stage1_tokeniser.py     # Token Slicer
│   ├── stage2_prediction.py    # Next Word Prophet
│   ├── stage3_temperature.py   # Temperature Lab
│   ├── stage4_context.py       # Context Window
│   ├── stage5_hallucination.py # Hallucination Hunter
│   ├── finish.py               # Results and grade screen
│   └── leaderboard.py          # Full leaderboard view
└── utils/
    ├── state.py                # Session state, scoring, leaderboard I/O
    └── leaderboard.py          # Sidebar leaderboard component
```

---

## Requirements

```
streamlit>=1.35.0
```

No other dependencies. No API keys. No database setup.

---

## Customising for your event

**Change the branding:** Search for `Arqiva Live 2025` across the files and replace with your event name.

**Add questions:** Each stage has a `QUESTIONS` or `PUZZLES` list at the top of its file — add new entries following the same dict structure.

**Adjust scoring:** All point values are defined as plain integers at the top of each stage file.

**Persistent leaderboard:** If you want scores to survive an app restart, swap the JSON file logic in `utils/state.py` for [Streamlit's `st.experimental_memo`](https://docs.streamlit.io/library/api-reference/performance) or a free [Supabase](https://supabase.com) table — the `save_to_leaderboard` and `load_leaderboard` functions are the only two places to change.

---

## Running as a facilitated event

Suggested format for 10–30 participants:

1. **Pre-brief (5 min):** Show the URL on screen, let everyone open it and enter their name
2. **Stages 1–3 (15 min):** Participants play at their own pace; leaderboard visible on the main screen
3. **Mid-point pause (5 min):** Call out the top 3 scores, explain any concepts that came up
4. **Stages 4–5 (15 min):** Final push; tension builds as scores shift
5. **Results (5 min):** Project the full leaderboard, announce winner, hand out prize

Total: ~40 minutes. Works in-person, hybrid, or fully remote.

---

## License

MIT — use it, fork it, brand it, run it at your own events.
