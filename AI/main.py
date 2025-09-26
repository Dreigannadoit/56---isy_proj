import os
import json
from typing import Dict, Any
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

CHAT_MODEL = "qwen3:8b"


class WordScorer:
    """Handles scoring for words based on various criteria"""

    def __init__(self, llm):
        self.llm = llm

    def score_word_commonality(self, word: str) -> float:
        """Score based on how common the word is (less common = higher score)"""
        prompt = f"""
        Rate how common the word "{word}" is on a scale of 1-10, where 1 is extremely common 
        (used daily by most people) and 10 is extremely rare (specialized or obscure).
        Return ONLY a number between 1 and 10 with no additional text.
        """
        response = self.llm.invoke(prompt).content.strip()
        try:
            return float(response)
        except:
            return 5.0  # Default score

    def score_word_length(self, word: str) -> float:
        """Score based on word length (longer = higher score)"""
        length = len(word)
        if length <= 3:
            return 1.0
        elif length <= 5:
            return 2.0
        elif length <= 7:
            return 3.0
        elif length <= 9:
            return 4.0
        else:
            return 5.0

    def score_spelling_complexity(self, word: str) -> float:
        """Score based on spelling difficulty"""
        prompt = f"""
        Rate the spelling complexity of the word "{word}" on a scale of 1-7, where 1 is very simple 
        (easy to spell) and 7 is very complex (difficult to spell consistently correctly).
        Consider factors like unusual letter combinations, silent letters, etc.
        Return ONLY a number between 1 and 7 with no additional text.
        """
        response = self.llm.invoke(prompt).content.strip()
        try:
            return float(response)
        except:
            return 3.5  # Default score

    def score_prompt_compatibility(self, word: str, prompt: str) -> float:
        """Score based on how well the word matches the prompt"""
        scoring_prompt = f"""
        Prompt: "{prompt}"
        Word: "{word}"

        Rate how well this word matches the prompt on a scale of 1-15, where:
        1-5: Poor match (tangentially related at best)
        6-10: Reasonable match (fits the general idea)
        11-15: Excellent match (perfectly captures the prompt's meaning)

        Return ONLY a number between 1 and 15 with no additional text.
        """
        response = self.llm.invoke(scoring_prompt).content.strip()
        try:
            return float(response)
        except:
            return 7.5  # Default score

    def check_spelling(self, word: str) -> bool:
        """Check if word is spelled correctly and deduct points if not"""
        prompt = f"""
        Is the word "{word}" spelled correctly? 
        Return ONLY "yes" if it's correctly spelled, or "no" if it's misspelled.
        """
        response = self.llm.invoke(prompt).content.strip().lower()
        return "yes" in response

    def calculate_total_score(self, word: str, prompt: str) -> Dict[str, Any]:
        """Calculate all scores for a word"""
        spelling_correct = self.check_spelling(word)

        scores = {
            'commonality': self.score_word_commonality(word),
            # 'length': self.score_word_length(word),
            'spelling_complexity': self.score_spelling_complexity(word),
            'prompt_compatibility': self.score_prompt_compatibility(word, prompt),
            'spelling_correct': spelling_correct
        }

        # Apply spelling penalty
        spelling_penalty = 0 if spelling_correct else -5
        scores['spelling_penalty'] = spelling_penalty

        scores['total'] = (
                scores['commonality'] +
                # scores['length'] +
                scores['spelling_complexity'] +
                scores['prompt_compatibility'] +
                spelling_penalty
        )

        return scores


def generate_prompt(llm):
    """Generate a creative prompt for the word game"""
    print("Generating prompt...")

    prompt_request = """
    Generate a creative, open-ended prompt for a word association game. 
    The prompt should describe a concept, feeling, object, or scenario that can be represented by many different words.
    Make it interesting but not too obscure. Return ONLY the prompt text.

    Examples:
    - "We use this term when something is pretty"
    - "What you feel when you accomplish something difficult"
    - "A word for when technology doesn't work as expected"

    Your prompt:
    """

    response = llm.invoke(prompt_request).content.strip()
    return response


def get_player_input(player_number: int):
    """Get word input from a player via terminal"""
    word = input(f"Player {player_number}, enter your word: ").strip()
    return word


def evaluate_words(llm, prompt: str, word1: str, word2: str):
    """Evaluate both words and determine the winner"""
    print("Evaluating words...")

    scorer = WordScorer(llm)

    # Score both words
    scores1 = scorer.calculate_total_score(word1, prompt)
    scores2 = scorer.calculate_total_score(word2, prompt)

    # Determine winner
    if scores1['total'] > scores2['total']:
        winner = "Player 1"
    elif scores2['total'] > scores1['total']:
        winner = "Player 2"
    else:
        winner = "It's a tie!"

    return {
        'player1_scores': scores1,
        'player2_scores': scores2,
        'winner': winner
    }


def display_results(evaluation_result: dict):
    """Display the game results in a formatted way"""
    result = evaluation_result
    word1_scores = result['player1_scores']
    word2_scores = result['player2_scores']

    print("\n" + "=" * 50)
    print("GAME RESULTS")
    print("=" * 50)

    # Player 1 results
    print(f"\nPlayer 1's Word:")
    print(f"How common is the word: {word1_scores['commonality']:.1f} points")
    # print(f"Length of the word: {word1_scores['length']:.1f} points")
    print(f"Spelling Complexity: {word1_scores['spelling_complexity']:.1f} points")
    print(f"Prompt Compatibility: {word1_scores['prompt_compatibility']:.1f} points")
    if not word1_scores['spelling_correct']:
        print(f"Spelling Penalty: {word1_scores['spelling_penalty']:.1f} points")
    print(f"Total: {word1_scores['total']:.1f} points")

    # Player 2 results
    print(f"\nPlayer 2's Word:")
    print(f"How common is the word: {word2_scores['commonality']:.1f} points")
    # print(f"Length of the word: {word2_scores['length']:.1f} points")
    print(f"Spelling Complexity: {word2_scores['spelling_complexity']:.1f} points")
    print(f"Prompt Compatibility: {word2_scores['prompt_compatibility']:.1f} points")
    if not word2_scores['spelling_correct']:
        print(f"Spelling Penalty: {word2_scores['spelling_penalty']:.1f} points")
    print(f"Total: {word2_scores['total']:.1f} points")

    print(f"\n{result['winner']} wins!")
    print("=" * 50)


def start_new_game(llm):
    """Start a new game round"""
    print("Starting new game...")

    # Generate prompt
    prompt = generate_prompt(llm)
    print(f"\nPrompt: {prompt}")

    # Get player inputs
    word1 = get_player_input(1)
    word2 = get_player_input(2)

    # Evaluate words
    evaluation = evaluate_words(llm, prompt, word1, word2)

    # Display results
    display_results(evaluation)

    return {
        'prompt': prompt,
        'player1_word': word1,
        'player2_word': word2,
        'evaluation': evaluation
    }


def play_game():
    """Main game loop"""
    print("Welcome to the Word Association Game!")
    print("=" * 50)

    # Initialize LLM
    try:
        llm = init_chat_model(CHAT_MODEL, model_provider='ollama')
        print(f"Connected to {CHAT_MODEL} successfully!")
    except Exception as e:
        print(f"Error connecting to LLM: {e}")
        print("Please make sure Ollama is running with the qwen3:8b model available.")
        return

    while True:
        print("\nOptions:")
        print("1. Start new game")
        print("2. Quit")

        choice = input("\nEnter your choice (1 or 2): ").strip()

        if choice == "2":
            print("Thanks for playing!")
            break
        elif choice == "1":
            try:
                start_new_game(llm)
            except Exception as e:
                print(f"An error occurred during the game: {e}")
                print("Please try again.")
        else:
            print("Invalid choice. Please enter 1 or 2.")


if __name__ == '__main__':
    play_game()