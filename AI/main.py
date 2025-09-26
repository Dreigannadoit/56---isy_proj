import os
import json
from typing import Dict, Any, Tuple
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
        Analyze the word "{word}" and rate its commonality in everyday English usage.
        Consider how frequently an average educated adult would encounter or use this word.

        Scoring scale:
        1-2: Extremely common (the, and, is, cat, run)
        3-4: Very common (happy, computer, quickly)
        5-6: Moderately common (significant, accomplish, various)
        7-8: Uncommon (serendipity, ephemeral, quintessential)
        9-10: Very rare/obscure (defenestration, sesquipedalian)

        Return ONLY the numeric score between 1-10. No explanations.
        """
        response = self.llm.invoke(prompt).content.strip()
        try:
            score = float(response)
            return min(max(score, 1), 10)  # Ensure score is between 1-10
        except:
            return 5.0

    def score_spelling_complexity(self, word: str) -> float:
        """Score based on spelling difficulty"""
        prompt = f"""
        Analyze the spelling complexity of the word "{word}". Consider:
        - Unusual letter combinations
        - Silent letters
        - Double letters
        - Exceptions to common spelling rules
        - Overall predictability of spelling

        Scoring scale:
        1-2: Very simple (cat, dog, run)
        3-4: Simple (happy, water, table)
        5-6: Moderate (receive, necessary, rhythm)
        7: Complex (conscience, questionnaire, bureaucracy)

        Return ONLY the numeric score between 1-7. No explanations.
        """
        response = self.llm.invoke(prompt).content.strip()
        try:
            score = float(response)
            return min(max(score, 1), 7)
        except:
            return 3.5

    def score_prompt_compatibility(self, word: str, prompt: str) -> float:
        """Score based on how well the word matches the prompt"""
        scoring_prompt = f"""
        PROMPT: "{prompt}"
        WORD TO EVALUATE: "{word}"

        How perfectly does this word capture the essence of the prompt?

        Specific scoring guidelines:
        1-3: Poor match (tangentially related at best)
        4-7: Fair match (somewhat related but not ideal)
        8-11: Good match (clearly related and appropriate)
        12-15: Excellent match (perfectly captures the prompt's meaning)

        Consider: specificity, relevance, and how well it embodies the concept.

        Return ONLY the numeric score between 1-15. No explanations.
        """
        response = self.llm.invoke(scoring_prompt).content.strip()
        try:
            score = float(response)
            return min(max(score, 1), 15)
        except:
            return 7.5

    def check_spelling(self, word: str) -> bool:
        """Check if word is spelled correctly"""
        # First, check if it's a proper noun (like "Eureka")
        if word.istitle() and len(word) > 1:
            # Could be a proper noun, which is valid
            return True

        prompt = f"""
        Is the word "{word}" spelled correctly in standard English? 
        Consider common variations and proper nouns.
        Return ONLY "correct" or "incorrect".
        """
        response = self.llm.invoke(prompt).content.strip().lower()
        return "correct" in response

    def break_tie(self, prompt: str, word1: str, word2: str) -> Tuple[str, str]:
        """Break a tie by having AI determine which word better matches the prompt"""
        tie_breaker_prompt = f"""
        PROMPT: "{prompt}"
        WORD 1: "{word1}"
        WORD 2: "{word2}"

        You are a judge in a word association game. Both words have the same total score, 
        but you must choose which one is the BETTER match for the prompt.

        Consider:
        - Which word more precisely captures the essence of the prompt?
        - Which word is more specific and appropriate for the context?
        - Which word would be more commonly used in this specific situation?
        - Choose the word that is HARDER to spell in English (Unusual letter combinations, Silent letters, Double letters, Exceptions to common spelling rules, Overall predictability of spelling).
        - Choose the word that is LESS commonly used or encountered by an average educated adult.

        DO NOT CONSIDER THE LENGTH OF THE WORD, BECAUSE THAT DOES NOT MATTER. 

        First, choose the winner by returning either "WORD1" or "WORD2".
        Then, provide a brief one-sentence explanation of why that word is a better match.

        Format your response exactly like this:
        WINNER: WORD1
        EXPLANATION: Your brief explanation here.

        Or:
        WINNER: WORD2  
        EXPLANATION: Your brief explanation here.
        """

        response = self.llm.invoke(tie_breaker_prompt).content.strip()

        # Parse the response
        lines = response.split('\n')
        winner = None
        explanation = ""

        for line in lines:
            if line.startswith('WINNER:'):
                if 'WORD1' in line.upper() or word1.upper() in line.upper():
                    winner = "Player 1"
                elif 'WORD2' in line.upper() or word2.upper() in line.upper():
                    winner = "Player 2"
            elif line.startswith('EXPLANATION:'):
                explanation = line.replace('EXPLANATION:', '').strip()

        if winner:
            return winner, explanation
        else:
            # Fallback if parsing fails
            fallback_winner = self._fallback_tie_break(prompt, word1, word2)
            explanation = f"{fallback_winner}'s word was chosen as it better captures the prompt's essence."
            return fallback_winner, explanation

    def _fallback_tie_break(self, prompt: str, word1: str, word2: str) -> str:
        """Fallback tie-breaking using spelling complexity and commonality"""
        # Prefer words that are harder to spell
        complexity1 = self.score_spelling_complexity(word1)
        complexity2 = self.score_spelling_complexity(word2)

        if complexity1 > complexity2:
            return "Player 1"
        elif complexity2 > complexity1:
            return "Player 2"

        # If same complexity, prefer less common words
        commonality1 = self.score_word_commonality(word1)
        commonality2 = self.score_word_commonality(word2)

        if commonality1 > commonality2:  # Higher score = less common
            return "Player 1"
        elif commonality2 > commonality1:
            return "Player 2"
        else:
            return "Player 1"  # Final fallback

    def calculate_total_score(self, word: str, prompt: str) -> Dict[str, Any]:
        """Calculate all scores for a word"""
        spelling_correct = self.check_spelling(word)

        scores = {
            'commonality': self.score_word_commonality(word),
            'spelling_complexity': self.score_spelling_complexity(word),
            'prompt_compatibility': self.score_prompt_compatibility(word, prompt),
            'spelling_correct': spelling_correct
        }

        # Apply spelling penalty
        spelling_penalty = 0 if spelling_correct else -5
        scores['spelling_penalty'] = spelling_penalty

        scores['total'] = (
                scores['commonality'] +
                scores['spelling_complexity'] +
                scores['prompt_compatibility'] +
                spelling_penalty
        )

        return scores


def generate_prompt(llm):
    """Generate a creative prompt for the word game"""
    print("Generating prompt...")

    prompt_request = """
    Create a single, clear prompt for a word association game. The prompt should describe a concept that can be represented by multiple words.
    Return ONLY the prompt text, nothing else.

    Example formats:
    "A word for when you finally understand something"
    "What we call something that brings people together"
    "A term for unexpected good fortune"

    Your prompt:
    """

    response = llm.invoke(prompt_request).content.strip()
    # Clean up any thinking text or markdown
    if "```" in response:
        response = response.split("```")[-1].strip()
    if response.startswith('"') and response.endswith('"'):
        response = response[1:-1]

    return response


def get_player_input(player_number: int):
    """Get word input from a player via terminal"""
    word = input(f"Player {player_number}, enter your word: ").strip()
    return word


def evaluate_words(llm, prompt: str, word1: str, word2: str):
    """Evaluate both words and determine the winner"""
    print("Evaluating words...")
    print(f"Prompt: {prompt}")
    print(f"Player 1: {word1}")
    print(f"Player 2: {word2}")

    scorer = WordScorer(llm)

    # Score both words
    print("\nScoring Player 1's word...")
    scores1 = scorer.calculate_total_score(word1, prompt)

    print("Scoring Player 2's word...")
    scores2 = scorer.calculate_total_score(word2, prompt)

    # Determine winner
    tie_breaker_explanation = ""
    if scores1['total'] > scores2['total']:
        winner = "Player 1"
        tie_breaker_used = False
    elif scores2['total'] > scores1['total']:
        winner = "Player 2"
        tie_breaker_used = False
    else:
        # Tie! Use tie-breaker
        print("\n⚖️  It's a tie! Using tie-breaker...")
        winner, tie_breaker_explanation = scorer.break_tie(prompt, word1, word2)
        tie_breaker_used = True

    return {
        'player1_scores': scores1,
        'player2_scores': scores2,
        'winner': winner,
        'tie_breaker_used': tie_breaker_used,
        'was_tie': scores1['total'] == scores2['total'],
        'tie_breaker_explanation': tie_breaker_explanation
    }


def display_results(evaluation_result: dict):
    """Display the game results in a formatted way"""
    result = evaluation_result
    word1_scores = result['player1_scores']
    word2_scores = result['player2_scores']

    print("\n" + "=" * 60)
    print("GAME RESULTS")
    print("=" * 60)

    # Player 1 results
    print(f"\nPlayer 1's Word:")
    print(f"  Commonality:       {word1_scores['commonality']:.1f}/10 points")
    print(f"  Spelling Complexity: {word1_scores['spelling_complexity']:.1f}/7 points")
    print(f"  Prompt Compatibility: {word1_scores['prompt_compatibility']:.1f}/15 points")
    if not word1_scores['spelling_correct']:
        print(f"  Spelling Penalty:  {word1_scores['spelling_penalty']:.1f} points")
    print(f"  TOTAL:             {word1_scores['total']:.1f} points")

    # Player 2 results
    print(f"\nPlayer 2's Word:")
    print(f"  Commonality:       {word2_scores['commonality']:.1f}/10 points")
    print(f"  Spelling Complexity: {word2_scores['spelling_complexity']:.1f}/7 points")
    print(f"  Prompt Compatibility: {word2_scores['prompt_compatibility']:.1f}/15 points")
    if not word2_scores['spelling_correct']:
        print(f"  Spelling Penalty:  {word2_scores['spelling_penalty']:.1f} points")
    print(f"  TOTAL:             {word2_scores['total']:.1f} points")

    # Display tie-breaker info if used
    if result['tie_breaker_used']:
        print(f"\n⚖️  TIE-BREAKER ACTIVATED!")
        if result['was_tie']:
            print(f"   Both words scored {word1_scores['total']:.1f} points")
        print(f"   AI determined that {result['winner']}'s word better matches the prompt")
        if result['tie_breaker_explanation']:
            print(f"   💡 Explanation: {result['tie_breaker_explanation']}")

    print(f"\n🎉 {result['winner']} wins! 🎉")
    print("=" * 60)


def start_new_game(llm):
    """Start a new game round"""
    print("\n" + "=" * 40)
    print("STARTING NEW GAME")
    print("=" * 40)

    # Generate prompt
    prompt = generate_prompt(llm)
    print(f"\n🎯 PROMPT: {prompt}\n")

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
    print("🚀 Welcome to the Word Association Game! 🚀")
    print("=" * 50)

    # Initialize LLM
    try:
        llm = init_chat_model(CHAT_MODEL, model_provider='ollama')
        print(f"✅ Connected to {CHAT_MODEL} successfully!")
    except Exception as e:
        print(f"❌ Error connecting to LLM: {e}")
        print("Please make sure Ollama is running with the qwen3:8b model available.")
        return

    while True:
        print("\nOptions:")
        print("1. Start new game")
        print("2. Quit")

        choice = input("\nEnter your choice (1 or 2): ").strip()

        if choice == "2":
            print("Thanks for playing! 👋")
            break
        elif choice == "1":
            try:
                start_new_game(llm)
            except Exception as e:
                print(f"❌ An error occurred: {e}")
                print("Please try again.")
        else:
            print("❌ Invalid choice. Please enter 1 or 2.")


if __name__ == '__main__':
    play_game()