import os
import json
from typing import Dict, Any, Tuple


class Word_Assesment:
    """Handles scoring for words based on various criteria"""

    def __init__(self, llm):
        self.llm

    def score_word_commanility(self, word1: str, word2: str) -> float:
        """Score word based on how common it is in elementary conversation"""

        return 0.0

    def score_spelling_complexity(self, word1: str, word2: str) -> float:
        """Score word based on how spelling complexity"""

        return 0.0

    def score_prompt_compatability(self, word1: str, word2: str) -> float:
        """Score word based on how prompt compatability"""

        return 0.0

    def check_spelling(self, word1: str, word2: str) -> bool:
        """Check if word is spelled correctly"""
        response = "correct"

        return "correct" in response

    def break_tie(self, prompt: str, word1: str, word2: str) -> Tuple[str, str]:
        return prompt, word1, word2

    def calculate_total_score(self, word: str, prompt: str) -> Dict[str, Any]:
        return {"word": word, "prompt": prompt}

    def generate_prompt(llm):
        """Generate a prompt covering a certain theme for the word game"""

        print("Generating prompt...")

        prompt = ""

        response = llm.invoke(prompt).content.strip()

        return response

    def evaluate_words(llm, prompt: str, word1: str, word2: str):
        """Evaluate both words and determine the winner"""

        pass

    def display_result(evaluation_result: dict):
        """Display the winner"""

        pass






