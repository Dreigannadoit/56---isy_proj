# LLM-Powered Word Association Game

A terminal-based multiplayer **word association game** powered by Large Language Models (LLMs).  
Players compete by entering words that best fit a generated prompt. The LLM scores each word based on:

- **Commonality**: How common the word is among elementary students (ages 7–11).  
- **Spelling Complexity**: How difficult the word is to spell.  
- **Prompt Compatibility**: How well the word matches the given prompt.  

The player with the **highest total score** wins!

---

## Features
- 🎮 Multiplayer support (2–5 players).  
- 🤖 LLM-powered evaluation using [LangChain](https://www.langchain.com/) and [Ollama](https://ollama.ai/).  
- 📝 Scoring based on **word commonality, spelling difficulty, and prompt fit**.  
- 🔄 Tie-breaking logic (customizable).  
- 🧑‍🏫 Fun and educational for kids and learners.  

---

## Requirements

- Python **3.10+**
- [Ollama](https://ollama.ai/) (must be installed and running)
- Dependencies listed in `requirements.txt` (see installation below)

---

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/LLM-powered_word_association_game.git
   cd LLM-powered_word_association_game
   ```
2. Create a virtual environment (recommended)
  ```bash
  python -m venv .venv
  source .venv/bin/activate   # On Linux/Mac
  .venv\Scripts\activate      # On Windows
  ```
3. Install dependencies
  ```bash
  pip install -r requirements.txt
  ```

## Running the Game
* Make sure Ollama is running and that the model you want (default: qwen3:0.6b) is available. *

Then run:

```bash
python main.py
```

You’ll see a menu:

```vbnet
Copy code
Welcome to The Notebook

Options:
1. Start a new game
2. Quit
Choose 1 to start a new game, pick the number of players (2–5), and enter your words!
```

## Project Structure
```bash
Copy code
.
├── main.py              # Entry point for the game
├── Word_Assesment.py    # Core game logic and scoring
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

---

## Example Gameplay
```yaml
Welcome to The Notebook

Options:
1. Start a new game
2. Quit

Enter your choice: 1
How many players? (2-5): 2

Prompt: "Something that shines in the sky at night."

Player 1, enter a word: moon
Player 2, enter a word: galaxy

Evaluating words...
...

GAME RESULTS
Prompt: Something that shines in the sky at night.

Scores:
Player 1 ('moon'): 13.0 points
 - Commonality: 2.0/10
 - Spelling Complexity: 2.0/7
 - Prompt Compatibility: 9.0/15

Player 2 ('galaxy'): 25.0 points
 - Commonality: 8.0/10
 - Spelling Complexity: 3.0/7
 - Prompt Compatibility: 14.0/15

Winner(s): Player 2!
'galaxy' (score: 25.0) is the least common word!
```

## Customization
- Model: Change the model in main.py:

```python
CHAT_MODEL = "qwen3:0.6b"
```

- Themes: Change the theme passed to start_new_game:
```python
Word_Assesment(llm).start_new_game(llm, theme="space")
```

- Scoring: Adjust logic in Word_Assesment.py.

---

### License
MIT License – feel free to use and modify.

### Future Ideas
- Web or GUI version
- Persistent leaderboard
- Advanced tie-breaking
- More scoring dimensions (e.g., creativity)











ChatGPT can make mistakes.
