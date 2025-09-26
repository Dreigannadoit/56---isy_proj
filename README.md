# Word Association Game 🎯

A creative word association game where two players compete to find the best word matching a given prompt. The game uses AI to evaluate words based on multiple criteria including commonality, spelling complexity, and prompt compatibility.

## Features

- **AI-Powered Scoring**: Uses language models to evaluate word quality
- **Multi-Criteria Evaluation**: Scores words based on:
  -- **Commonality**: How rare/uncommon the word is
  -- **Spelling Complexity**: Difficulty of spelling
  -- **Prompt Compatibility**: How well the word matches the prompt
  -- **Spelling Accuracy**: Penalty for misspelled words
- **Tie-Breaker System**: AI-powered tie-breaking when scores are equal
- **Interactive Gameplay**: Simple terminal-based interface
- **Detailed Results**: Comprehensive scoring breakdown after each round

## Prerequisites

Before running the game, make sure you have:

1. **Python 3.8+** installed
2. **Ollama** installed and running
3. **Qwen3:8b model** available in Ollama

### Installing Ollama and Qwen Model

```bash
# Install Ollama (visit https://ollama.ai for specific instructions for your OS)
# On macOS/Linux:
curl -fsSL https://ollama.ai/install.sh | sh

# Pull the required model
ollama pull qwen2.5:7b
```

## Installation

1. Clone or download the game files
2. Install required Python packages:
   ```bash
   pip install langchain-community python-dotenv
   ```
3. Set up environment (optional - create a .env file for custom configurations):
   ```bash
   pip install -r requirements.txt
   ```

