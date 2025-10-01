# The Notebook – AI Word Game

An AI-powered word association game built with Ollama + Qwen3 (0.6B) as the reasoning model.

The backend handles scoring, prompt generation, and player word evaluation, while the frontend (React + Vite) will provide the UI/UX layer.


~~~ bash
project-root/
│
├── AI/                     # Backend (Python, Ollama, LangChain)
│   ├── Word_Assesment.py   # Core game logic & word scoring
│   ├── main.py             # CLI entry point for testing / playing in terminal
│   ├── requirements.txt    # Python dependencies
│   ├── .idea/              # IDE configs (ignore)
│   └── __pycache__/        # Python cache (ignore)
│
├── frontend/               # React + Vite frontend (UI/UX)
│   ├── src/                # React app source (empty for now)
│   └── package.json        # Frontend dependencies
│
└── README.md               # Documentation
~~~

---

## AI Python

*Dependencies*

Install required Python packages:

~~~bash
cd AI
pip install -r requirements.txt
~~~

Your requirements.txt should contain at least:

~~~bash
langchain
ollama
~~~

---

## Running the AI in CLI

You can test the AI game loop directly in the terminal:

~~~bash
cd AI
python main.py
~~~

This will start the game where:

- This will start the game where:
- Players input words.
- Words are evaluated on:
   - Commonality - how common the word is among 7–11-year-olds
   - Spelling Complexity - difficulty of spelling
   - Prompt Compatibility - how well the word matches the prompt

Scores are calculated, and the winner is displayed.

---

## Code Overview
*`main.py`*

- Entry point for running the game.
- Initializes the *LLM* with Ollama (qwen3:0.6b).

*`Word_Assesment.py`*

- Core logic for evaluating words.

---
---
---

## Frontend (React + Vite)

*Not yet implemented – placeholder for future development.*

The frontend will:
- Provide a web UI for multiple players.
- Fetch AI results from the backend (via API).
- Display game prompts, scores, and winners.

Planned Workflow
1. Players input words through React UI.
2. Frontend sends words + prompt → backend API (to be created).
3. Backend returns scores + winner(s).
4. UI updates with live results.

Tech Stack
- React + Vite (frontend framework + fast bundler).
- Express / FastAPI (planned backend API layer).
- Ollama + LangChain (AI reasoning).

---
---
---

## Quick Start for Devs

1. Run Ollama with Qwen3:
   ~~~bash
   ollama run qwen3:0.6b
   ~~~
2. Start backend test:
   ~~~bash
   cd AI
   python main.py
   ~~~
3. Prepare frontend:
   ~~~bash
   cd frontend
   npm install
   npm run dev
   ~~~
