from flask import Flask, request, jsonify
from flask_cors import CORS  # To handle Cross-Origin Resource Sharing
from langchain.chat_models import init_chat_model
from Word_Assesment import Word_Assesment
import os  # Import os for environment variables or similar needs

CHAT_MODEL = "qwen3:0.6b"  # Or load from an environment variable

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes, adjust as needed for production

# Initialize LLM once
try:
    llm = init_chat_model(CHAT_MODEL, model_provider='ollama')
    print(f"Successfully connected to LLM: {CHAT_MODEL}")
except Exception as e:
    print(f"Error connecting LLM on startup: {e}")
    llm = None  # Handle case where LLM fails to initialize


@app.route('/')
def home():
    return "Welcome to The Notebook API!"


@app.route('/start_game', methods=['POST'])
def start_game():
    if llm is None:
        return jsonify({"error": "LLM not initialized. Please check backend logs."}), 500

    data = request.get_json()
    player_count = data.get('player_count')
    theme = data.get('theme', '')  # Allow theme to be optional

    if not player_count or not (2 <= player_count <= 5):
        return jsonify({"error": "Invalid player count. Must be between 2 and 5."}), 400

    word_assessment = Word_Assesment(llm)

    try:
        # Generate prompt
        prompt = word_assessment.generate_prompt(llm, theme)

        # Prepare response for the frontend
        return jsonify({
            "prompt": prompt,
            "player_count": player_count,
            "message": "Game started, prompt generated. Awaiting player words."
        })
    except Exception as e:
        print(f"Error generating prompt: {e}")
        return jsonify({"error": f"Failed to generate game prompt: {str(e)}"}), 500


@app.route('/submit_words', methods=['POST'])
def submit_words():
    if llm is None:
        return jsonify({"error": "LLM not initialized. Please check backend logs."}), 500

    data = request.get_json()
    prompt = data.get('prompt')
    player_words = data.get('player_words')  # Expecting a dictionary like {1: "word1", 2: "word2"}

    if not prompt or not player_words or not isinstance(player_words, dict):
        return jsonify({"error": "Invalid input. 'prompt' and 'player_words' (as a dictionary) are required."}), 400

    word_assessment = Word_Assesment(llm)
    try:
        # Evaluate words
        evaluation_result = word_assessment.evaluate_words(llm, prompt, player_words)

        # Return the evaluation result
        return jsonify(evaluation_result)
    except Exception as e:
        print(f"Error evaluating words: {e}")
        return jsonify({"error": f"Failed to evaluate words: {str(e)}"}), 500


if __name__ == '__main__':
    # You might want to get the port from an environment variable in production
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)  # debug=True for development