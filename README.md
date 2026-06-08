# LLM Quest 🧠
### Arqiva Live 2025 — Interactive AI Learning Game

A 5-stage puzzle game that teaches core LLM concepts through play. No API keys, no cloud costs, pure Python.

## Concepts covered

| Stage | Name | Concept taught |
|-------|------|----------------|
| 1 | ⚡ Token Slicer | Tokenisation — how LLMs see text |
| 2 | 🔮 Next Word Prophet | Next-token prediction |
| 3 | 🌡️ Temperature Lab | Temperature & randomness |
| 4 | 📦 Context Window | Context limits & relevance |
| 5 | 🕵️ Hallucination Hunter | AI hallucination |

## Run locally

```bash
pip install streamlit
streamlit run app.py
```

## Run for an event (multiple players)

Start on any machine accessible on your network:

```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

Players open `http://<your-ip>:8501` on their laptops/phones.
Leaderboard is shared via `/tmp/llm_quest_leaderboard.json`.

## Deploy to Streamlit Community Cloud (free)

1. Push this folder to a GitHub repo
2. Go to share.streamlit.io
3. Connect repo → set `app.py` as entry point
4. Share the URL with participants

## Scoring

- **Stage 1**: 100pts exact / 50pts ±1 / +20pts no hint / +50pts speed
- **Stage 2**: 80pts correct / +15pts per streak level
- **Stage 3**: 120pts per correct scenario
- **Stage 4**: 150pts + speed bonus
- **Stage 5**: 150pts + speed bonus

**Max theoretical score: ~2,400 pts**
