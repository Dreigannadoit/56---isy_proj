import os
import json
from typing import Dict, Any, Tuple


class Word_Assesment:
    """Handles scoring for words based on various criteria"""

    def __init__(self, llm):
        self.llm = llm

    def score_word_commonality(self, word1: str, word2: str) -> Dict[str, float]:
        """Score word based on how common it is in elementary conversation"""

        prompt = f"""
            Analyze the 2 words and rate its commonality in everyday English conversation among Elementary students from the Ages 7 to 11. 
            Consider how frequently an average ELEMENTARY student from the AGES 7 to 11 would use this words in everyday conversation.

            Words to analyze and score: "{word1}" and "{word2}"

            Return ONLY a JSON object with this exact format
            {{ {word1}: score1, {word2}: score2 }}

            Where score1 is for "{word1}" and score2 is for "{word2}", scored from 1-10 using this scale:

            1 – Universal: Used in almost every conversation. (e.g., I, you, yes, no, mom, dad, school)  
            2 – Extremely Common: Very frequent in everyday talk. (e.g., friend, play, game, eat, teacher)  
            3 – Very Common: Appears often in casual or school-related conversations. (e.g., book, movie, fun, house, run)  
            4 – Common: Known and sometimes used, though not in every chat. (e.g., homework, pet, candy, music)  
            5 – Fairly Common: Recognized by most kids but used only in certain contexts. (e.g., castle, balloon, brave, computer)  
            6 – Moderately Common: Kids understand the word, but don't say it often. (e.g., science, travel, concert, clever)  
            7 – Less Common: Kids may know it but would need context to use it naturally. (e.g., enormous, invent, mystery, forest)  
            8 – Rare: Recognized occasionally (through reading, shows, or class), but rarely used in their own speech. (e.g., galaxy, experiment, rescue, adventure)  
            9 – Very Rare: Kids might understand if explained, but don't use it conversationally. (e.g., democracy, microscope, ancient, universe)  
            10 – Uncommon / Advanced: Almost never appears in everyday conversations of 7–11-year-olds. (e.g., hypothesis, algorithm, nostalgia, philosophy)

            Higher scores mean the word is LESS common (better for the game).

        """

        response = self.llm.invoke(prompt).content.strip()
        print(f"LLM response: {response}")

        try:
            scores = json.loads(response)
            print(scores)
            return scores
            # word1_score = scores.get("word1_score") or scores.get("score1") or scores.get(word1) or scores.get(
            #     word1.lower()) or scores.get(word1.upper())
            # word2_score = scores.get("word2_score") or scores.get("score2") or scores.get(word2) or scores.get(
            #     word2.lower()) or scores.get(word2.upper())
            #
            # if word1_score is not None and word2_score is not None:
            #     print("conversion of commonality prompt to float value")
            #
            #     word1_score_float = max(1, min(10, float(word1_score)))
            #     word2_score_float = max(1, min(10, float(word2_score)))
            #
            #     result = {word1: word1_score_float, word2: word2_score_float}
            #
            #     return result
            # else:
            #     print("Was not able to extract scores from response")
            #     return {word1: 5.0, word2: 5.0}
        except (json.decoder.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Error while parsing response for commonality prompt: {e}")
            return {word1: 5.0, word2: 5.0}

    def score_spelling_complexity(self, word1: str, word2: str) -> Dict[str, float]:
        """Score word based on how spelling complexity"""

        return 0.0

    def score_prompt_compatability(self, word1: str, word2: str) -> Dict[str, float]:
        """Score word based on how prompt compatability"""

        return 0.0

    def check_spelling(self, word1: str, word2: str) -> bool:
        """Check if word is spelled correctly"""
        response = "correct"

        return "correct" in response

    def break_tie(self, prompt: str, word1: str, word2: str) -> Tuple[str, str]:
        return

    def calculate_total_score(self, word1: str, word2: str, prompt: str) -> Dict[str, Any]:
        isSpellingCorrect = self.check_spelling(word1, word2)

        print("Starting Calculation")
        print("Getting commonality score")
        commonality_scores = self.score_word_commonality(word1, word2)

        scores = {
            'commonality': commonality_scores,
            'total': {
                word1: commonality_scores.get(word1, 0.0),
                word2: commonality_scores.get(word2, 0.0),
            }
        }

        return scores

    def generate_prompt(self, llm, theme: str):
        """Generate a prompt covering a certain theme for the word game"""

        print("Generating prompt...")

        prompt = f"""
        Create a SINGLE, clear prompt for a word association game following the theme "{theme}". The prompt should describe a concept that can be represented by multiple words. 
        Make sure that the prompt does not describe a particular word.
        DO NOT GIVE MORE THAN 1 (ONE) PROMPT
        
        Example format: 

        - "A word for when you finally understand something."  
        - "Something you find when people celebrate together."  
        - "A place where many children spend their day learning."  
        - "Something people use to travel long distances."  
        - "A feeling you get when you are very excited about something."  
        - "Something that shines in the sky at night."  
        - "A sound you often hear when people are laughing."  
        - "Something people eat when they are hungry."  
        """
        response = llm.invoke(prompt).content.strip()

        return response


    def get_player_input(self, player_num: int):
        """Get word input from a player via terminal"""
        word = input(f"Player {player_num}, enter a word: ").strip()

        return word

    def evaluate_words(self, llm, prompt: str, word1: str, word2: str):
        """Evaluate both words and determine the winner"""
        print("Evaluating words...")
        print(f"Prompt: {prompt}")
        print(f"Player 1: {word1}")
        print(f"Player 2: {word2}")

        scorer = Word_Assesment(llm)

        print("\nScoring Player's Words")
        scores = scorer.calculate_total_score(word1, word2, prompt)

        # Ensure we're using the original words that were input
        player1_score = scores['total'].get(word1, 0)
        player2_score = scores['total'].get(word2, 0)

        if player1_score > player2_score:
            winner = "Player 1"
        elif player1_score < player2_score:
            winner = "Player 2"
        else:
            winner = "Tie"

        return {
            'player_scores': scores,
            'winner': winner,
            'player1_score': player1_score,
            'player2_score': player2_score,
            'player1_word': word1,  # Store the original words
            'player2_word': word2,  # Store the original words
        }

    def display_result(self, evaluation_result: dict):
        """Display the winner and scores in a readable format"""

        scores = evaluation_result['player_scores']
        winner = evaluation_result['winner']
        player1_score = evaluation_result['player1_score']
        player2_score = evaluation_result['player2_score']
        word1 = evaluation_result['player1_word']
        word2 = evaluation_result['player2_word']

        print("\n" + "=" * 50)
        print("GAME RESULTS")
        print("=" * 50)

        print(f"\nScores:")
        print(f"Player 1 ('{word1}'): {player1_score:.1f} points")
        print(f"Player 2 ('{word2}'): {player2_score:.1f} points")

        print(f"\nCommonality Breakdown:")
        commonality_scores = scores['commonality']
        for word, score in commonality_scores.items():
            print(f"  '{word}': {score:.1f}/10")

        print(f"\nWinner: {winner}!")

        if winner == "Tie":
            print("It's a tie! Both words are equally uncommon.")
        else:
            winning_word = word1 if winner == "Player 1" else word2
            losing_word = word2 if winner == "Player 1" else word1
            winning_score = player1_score if winner == "Player 1" else player2_score
            losing_score = player2_score if winner == "Player 1" else player1_score
            print(
                f"'{winning_word}' (score: {winning_score:.1f}) is less common than '{losing_word}' (score: {losing_score:.1f}) for elementary students aged 7-11.")

        print("=" * 50)


    def start_new_game(self, llm):
        """Start a new game"""
        print("\n" +  "*" * 40)
        print("START NEW GAME")
        print("*" * 40)

        # Generate Prompt
        prompt = self.generate_prompt(llm, "")
        print(f"\nPrompt: {prompt}\n")

        # get player inputs
        word1 = self.get_player_input(1)
        word2 = self.get_player_input(2)

        # evaluate words
        evaluation = self.evaluate_words(llm, prompt, word1, word2)

        # display results
        self.display_result(evaluation)

        return {
            'prompt': prompt,
            'player1_word': word1,
            'player2_word': word2,
            'evaluation_result': evaluation
        }