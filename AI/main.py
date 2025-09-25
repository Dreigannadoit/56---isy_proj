import ollama
import string
from typing import Dict, Tuple, List
import re


class WordGameAgent:
    def __init__(self, model_name="qwen2:8b"):
        self.model_name = model_name
        self.client = ollama.Client()

    def generate_prompt(self) -> str:
        """Generate a creative prompt for the word game"""
        prompt_template = """
        Generate a creative, single-sentence prompt that describes something without naming it directly.
        The prompt should encourage players to think of descriptive words. 
        Make it engaging and suitable for a word association game.
        Examples:
        - "We use this term when something is exceptionally beautiful"
        - "What do you call something that shines brightly in the dark?"
        - "A word for when you feel completely at peace"

        Generate one new prompt:
        """

        try:
            response = self.client.generate(
                model=self.model_name,
                prompt=prompt_template,
                options={'temperature': 0.8}
            )
            return response['response'].strip().strip('"')
        except Exception as e:
            # Fallback prompts if LLM fails
            fallback_prompts = [
                "We use this term when something is incredibly beautiful",
                "What do you call something that glows with inner light?",
                "A word for when you feel completely content and happy",
                "Describe something that moves with grace and elegance",
                "What term would you use for something ancient and mysterious?"
            ]
            import random
            return random.choice(fallback_prompts)

    def analyze_word_commonality(self, word: str) -> float:
        """Analyze how common a word is (0-10 points)"""
        analysis_prompt = f"""
        On a scale of 1-10, where 1 is extremely common (like 'the', 'and', 'is') 
        and 10 is extremely rare/uncommon, rate how common the word "{word}" is in everyday English usage.
        Consider frequency in literature, conversation, and media.
        Return only a single number between 1 and 10.
        """

        try:
            response = self.client.generate(
                model=self.model_name,
                prompt=analysis_prompt,
                options={'temperature': 0.3}
            )
            score = float(response['response'].strip())
            return max(1, min(10, score))  # Clamp between 1-10
        except:
            # Fallback based on word length and complexity
            return min(10, max(1, len(word) * 0.7))

    def analyze_spelling_complexity(self, word: str) -> float:
        """Analyze spelling complexity (0-7 points)"""
        # Basic analysis first
        complexity_factors = 0

        # Length factor
        if len(word) > 8:
            complexity_factors += 2
        elif len(word) > 5:
            complexity_factors += 1

        # Special characters and patterns
        if any(char not in string.ascii_letters for char in word):
            complexity_factors += 1

        # Double letters, silent letters, unusual patterns
        if any(word.count(char) > 1 for char in set(word)):
            complexity_factors += 1

        # LLM analysis for finer grading
        analysis_prompt = f"""
        On a scale of 1-7, rate the spelling complexity of the word "{word}".
        Consider factors like unusual letter combinations, silent letters, exceptions to spelling rules, etc.
        1 = very simple to spell (like 'cat')
        7 = very complex to spell (like 'mnemonic' or 'psyche')
        Return only a single number between 1 and 7.
        """

        try:
            response = self.client.generate(
                model=self.model_name,
                prompt=analysis_prompt,
                options={'temperature': 0.3}
            )
            llm_score = float(response['response'].strip())
            return max(1, min(7, (complexity_factors + llm_score) / 2))
        except:
            return max(1, min(7, complexity_factors * 1.5))

    def analyze_prompt_compatibility(self, word: str, prompt: str) -> float:
        """Analyze how well the word matches the prompt (0-15 points)"""
        analysis_prompt = f"""
        Prompt: "{prompt}"
        Word: "{word}"

        On a scale of 1-15, rate how well the word matches or responds to the prompt.
        Consider relevance, creativity, and appropriateness.
        1 = completely unrelated
        15 = perfectly matches and enhances the prompt
        Return only a single number between 1 and 15.
        """

        try:
            response = self.client.generate(
                model=self.model_name,
                prompt=analysis_prompt,
                options={'temperature': 0.4}
            )
            score = float(response['response'].strip())
            return max(1, min(15, score))
        except:
            # Fallback: basic keyword matching
            prompt_words = set(re.findall(r'\w+', prompt.lower()))
            word_lower = word.lower()
            matches = sum(1 for pw in prompt_words if len(pw) > 3 and pw in word_lower or word_lower in pw)
            return max(5, min(15, matches * 3))

    def check_spelling(self, word: str) -> Tuple[bool, float]:
        """Check if word is spelled correctly and return deduction amount"""
        check_prompt = f"""
        Is the word "{word}" spelled correctly in English? 
        Respond with only "YES" or "NO".
        """

        try:
            response = self.client.generate(
                model=self.model_name,
                prompt=check_prompt,
                options={'temperature': 0.1}
            )
            is_correct = "YES" in response['response'].strip().upper()
            deduction = 0.0 if is_correct else 3.0  # Deduct 3 points for misspelling
            return is_correct, deduction
        except:
            # Basic check: all alphabetic and reasonable length
            if word and all(c in string.ascii_letters for c in word) and 2 <= len(word) <= 20:
                return True, 0.0
            return False, 3.0

    def calculate_length_points(self, word: str) -> float:
        """Calculate points based on word length (0-5 points)"""
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

    def evaluate_word(self, word: str, prompt: str) -> Dict:
        """Evaluate a word against all criteria"""
        # Check spelling first
        is_correct, spelling_deduction = self.check_spelling(word)

        # Calculate all scores
        commonality_score = self.analyze_word_commonality(word)
        length_score = self.calculate_length_points(word)
        spelling_complexity_score = self.analyze_spelling_complexity(word)
        prompt_compatibility_score = self.analyze_prompt_compatibility(word, prompt)

        # Calculate total (apply spelling deduction)
        total_score = (commonality_score + length_score +
                       spelling_complexity_score + prompt_compatibility_score - spelling_deduction)

        return {
            'word': word,
            'is_spelled_correctly': is_correct,
            'spelling_deduction': spelling_deduction,
            'scores': {
                'commonality': commonality_score,
                'length': length_score,
                'spelling_complexity': spelling_complexity_score,
                'prompt_compatibility': prompt_compatibility_score
            },
            'total_score': max(0, total_score)  # Ensure non-negative
        }


class WordGame:
    def __init__(self):
        self.agent = WordGameAgent()
        self.players = []

    def get_player_input(self, player_name: str, prompt: str) -> str:
        """Get word input from a player via terminal"""
        print(f"\n{player_name}, enter your word for the prompt:")
        print(f'Prompt: "{prompt}"')
        while True:
            word = input("Your word: ").strip()
            if word and all(c.isalpha() or c.isspace() for c in word):
                # Take only the first word if multiple words entered
                return word.split()[0].lower()
            else:
                print("Please enter a valid word (letters only):")

    def display_results(self, result1: Dict, result2: Dict, prompt: str):
        """Display detailed results for both players"""
        print(f"\n{'=' * 50}")
        print(f"PROMPT: {prompt}")
        print(f"{'=' * 50}")

        for i, (player, result) in enumerate(zip(self.players, [result1, result2]), 1):
            print(f"\n{player}'s word: {result['word'].title()}")
            if not result['is_spelled_correctly']:
                print("⚠️  Spelling error! -3 points deducted")

            scores = result['scores']
            print(f"How common is the word: {scores['commonality']:.1f} points")
            print(f"Length of the word: {scores['length']:.1f} points")
            print(f"Spelling Complexity: {scores['spelling_complexity']:.1f} points")
            print(f"Prompt Compatibility: {scores['prompt_compatibility']:.1f} points")

            if result['spelling_deduction'] > 0:
                print(f"Spelling Deduction: -{result['spelling_deduction']:.1f} points")

            print(f"TOTAL: {result['total_score']:.1f} points")
            print("-" * 30)

    def determine_winner(self, result1: Dict, result2: Dict) -> str:
        """Determine and announce the winner"""
        score1 = result1['total_score']
        score2 = result2['total_score']

        if abs(score1 - score2) < 0.1:  # Tie with small tolerance
            return "It's a tie!"
        elif score1 > score2:
            return f"{self.players[0]} wins!"
        else:
            return f"{self.players[1]} wins!"

    def play_round(self):
        """Play one round of the word game"""
        print("\n" + "🎮 WORD GAME ROUND 🎮".center(50, "="))

        # Generate prompt
        prompt = self.agent.generate_prompt()
        print(f"\nGenerated Prompt: {prompt}")

        # Get player words
        word1 = self.get_player_input(self.players[0], prompt)
        word2 = self.get_player_input(self.players[1], prompt)

        # Evaluate words
        print("\nEvaluating words...")
        result1 = self.agent.evaluate_word(word1, prompt)
        result2 = self.agent.evaluate_word(word2, prompt)

        # Display results
        self.display_results(result1, result2, prompt)

        # Announce winner
        winner = self.determine_winner(result1, result2)
        print(f"\n🎉 {winner}")

    def setup_players(self):
        """Set up player names"""
        print("Welcome to the AI Word Game!")
        player1 = input("Enter name for Player 1: ").strip() or "Player 1"
        player2 = input("Enter name for Player 2: ").strip() or "Player 2"
        self.players = [player1, player2]

    def run_game(self):
        """Main game loop"""
        self.setup_players()

        while True:
            self.play_round()

            # Ask to play again
            play_again = input("\nPlay another round? (y/n): ").strip().lower()
            if play_again not in ['y', 'yes']:
                print("Thanks for playing!")
                break


def main():
    """Main function to run the game"""
    try:
        # Test Ollama connection
        client = ollama.Client()
        models = client.list()
        print("Ollama connection successful!")

        game = WordGame()
        game.run_game()

    except Exception as e:
        print(f"Error: {e}")
        print("Make sure Ollama is running and the qwen2:8b model is installed.")
        print("You can install it with: ollama pull qwen2:8b")


if __name__ == "__main__":
    main()