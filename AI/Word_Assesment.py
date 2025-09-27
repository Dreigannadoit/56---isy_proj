import os
import json
from typing import Dict, Any, Tuple, List


class Word_Assesment:
    """Handles scoring for words based on various criteria"""

    def __init__(self, llm):
        self.llm = llm


    def prompt_template(self, llm, playerId: int, prompt: str, operationName: str) -> Dict[str, Any]:
        response = self.llm.invoke(prompt).content.strip()

        # Clean up the response
        final_response = response.split('</think>')[-1].strip()
        print(f"LLM response: {final_response}")

        try:
            scores = json.loads(final_response)
            print(f"Parsed Scores: {scores}")

            # Validate the response structure
            if 'id' in scores and 'score' in scores:
                return scores
            else:
                print("Invalid JSON structure, using default score")
                return {'id': playerId, 'score': 5.0}

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Error while parsing response for {operationName}: {e}")
            print(f"Response Failed: {final_response}")
            return {'id': playerId, 'score': 5.0}


    def score_word_commonality(self, llm, word: str, playerId: int) -> Dict[str, Any]:
        """Score word based on how common it is in elementary conversation"""

        prompt = f"""
            Analyze the word and rate its commonality in everyday English conversation among Elementary students from the Ages 7 to 11. 
            Consider how frequently an average ELEMENTARY student from the AGES 7 to 11 would use this word in everyday conversation.

            Word to analyze and score: "{word}"

            Return ONLY a JSON object with this exact format:
            {{"id": {playerId}, "score": score}}

            Where id is the player ID and score is the player score, scored from 1-10 using this scale:

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

        result = self.prompt_template(playerId = playerId, prompt = prompt, operationName = "Word Commonality")


    def score_spelling_complexity(self, llm, word: str, playerId: int) -> Dict[str, Any]:
        """Score word based on spelling complexity"""

        prompt = f"""
            Analyze the spelling complexity of the word "{word}". Consider:
            - Unusual letter combinations
            - Silent letters
            - Double letters
            - Exceptions to common spelling rules
            - Overall predictability of spelling
                
            Word to analyze and score: "{word}"

            Return ONLY a JSON object with this exact format:
            {{"id": {playerId}, "score": score}}
            
            Where id is the player ID and score is the player score, scored from 1-7 using this scale:
        
            Scoring scale:
            1-2: Very simple (cat, dog, run)
            3-4: Simple (happy, water, table)
            5-6: Moderate (receive, necessary, rhythm)
            7 : Complex (conscience, questionnaire, bureaucracy)
                
            Higher scores mean the word is HARDER to spell (better for the game).
            """

        response = self.llm.invoke(prompt).content.strip()

        # Clean up the response
        final_response = response.split('</think>')[-1].strip()
        print(f"LLM response: {final_response}")

        try:
            scores = json.loads(final_response)
            print(f"Parsed Scores: {scores}")

            # Validate the response structure
            if 'id' in scores and 'score' in scores:
                return scores
            else:
                print("Invalid JSON structure, using default score")
                return {'id': playerId, 'score': 5.0}

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Error while parsing response for spelling complexity prompt: {e}")
            print(f"Response Failed: {final_response}")
            return {'id': playerId, 'score': 5.0}


    def score_prompt_compatibility(self, llm, word: str, playerId: int, prompt: str) -> Dict[str, Any]:
        """Score word based on prompt compatibility"""

        prompt = f"""
        PROMPT: "{prompt}"
        WORD TO EVALUATE: "{word}"

        How perfectly does this word capture the essence of the prompt?
                
        Word to analyze and score: "{word}"

        Return ONLY a JSON object with this exact format:
        {{"id": {playerId}, "score": score}}

        Where id is the player ID and score is the player score, scored from 1-15 using this scale:
        1-3: Poor match (tangentially related at best)
        4-7: Fair match (somewhat related but not ideal)
        8-11: Good match (clearly related and appropriate)
        12-15: Excellent match (perfectly captures the prompt's meaning)

        Consider: specificity, relevance, and how well it embodies the concept.
                
        Higher scores mean the word is very closely related to the prompt.
        """

        response = self.llm.invoke(prompt).content.strip()

        # Clean up the response
        final_response = response.split('</think>')[-1].strip()
        print(f"LLM response: {final_response}")

        try:
            scores = json.loads(final_response)
            print(f"Parsed Scores: {scores}")

            # Validate the response structure
            if 'id' in scores and 'score' in scores:
                return scores
            else:
                print("Invalid JSON structure, using default score")
                return {'id': playerId, 'score': 5.0}

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Error while parsing response for spelling prompt compatability prompt: {e}")
            print(f"Response Failed: {final_response}")
            return {'id': playerId, 'score': 5.0}


    def check_spelling(self, llm, word: str) -> bool:
        """Check if word is spelled correctly"""

        # Simple spelling check - you might want to implement a proper spell checker
        return True  # Placeholder


    def break_tie(self, llm, players_scores: List[Dict]) -> List[int]:
        """Break ties between players with same scores"""

        # For now, return the original order
        return [score['id'] for score in players_scores]


    def calculate_total_score(self, llm, words: Dict[int, str], prompt: str) -> List[Dict[str, Any]]:
        """Calculate total scores for all players"""

        print("Starting Calculation")

        playerScores = []
        for player_id, word in words.items():
            # Get commonality score
            print(f"Getting commonality score for Player {player_id}: {word}")
            commonalityScore = self.score_word_commonality(llm, word, player_id)

            # Get Spelling Complexity Score
            print(f"Getting Spelling Complexity score for Player {player_id}: {word}")
            complexityScore = self.score_spelling_complexity(llm, word, player_id)

            # Get Prompt Combatability Score
            print(f"Getting Prompt Compatability score for Player {player_id}: {word}")
            combatabilityScore = self.score_prompt_compatibility(llm, word, prompt, player_id)

            # You can add other scoring components later
            totalScore = commonalityScore['score'] + complexityScore['score'] + combatabilityScore["score"]

            playerScores.append({
                'id': player_id,
                'word': word,
                'commonality': commonalityScore['score'],
                'complexity': complexityScore['score'],
                'compatability' : combatabilityScore["score"],
                'total': totalScore
            })

        return playerScores


    def generate_prompt(self, llm,  theme: str) -> str:
        """Generate a prompt covering a certain theme for the word game"""

        print("Generating prompt...")

        prompt = f"""
        Create a SINGLE, clear prompt for a word association game following the theme "{theme}". 
        The prompt should describe a concept that can be represented by multiple words. 
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

        Return only the prompt text without any additional explanation.
        """

        response = self.llm.invoke(prompt).content.strip()
        finalResponse = response.split('</think>')[-1].strip()

        return finalResponse


    def get_player_input(self, player_num: int) -> str:
        """Get word input from a player via terminal"""

        word = input(f"Player {player_num}, enter a word: ").strip()
        return word


    def get_player_count(self) -> int:
        """Get number of players with validation"""

        while True:
            try:
                count = int(input("How many players? (2-5): ").strip())
                if 2 <= count <= 5:
                    return count
                else:
                    print("Please enter a number between 2 and 5.")
            except ValueError:
                print("Please enter a valid number.")


    def evaluate_words(self, llm, prompt: str, words: Dict[int, str]) -> Dict[str, Any]:
        """Evaluate all words and determine the winner"""
        print("Evaluating words...")
        print(f"Prompt: {prompt}")

        for player_id, word in words.items():
            print(f"Player {player_id}: {word}")

        print("\nScoring Players' Words")
        playerScores = self.calculate_total_score(llm, words, prompt)

        # Sort players by total score (descending - higher score is better)
        playerScores.sort(key=lambda x: x['total'], reverse=True)

        # Check for ties
        winners = []
        if len(playerScores) > 1 and playerScores[0]['total'] == playerScores[1]['total']:
            print("Tie detected! Breaking tie...")

            # Implement tie-breaking logic here
            tied_players = [score for score in playerScores if score['total'] == playerScores[0]['total']]
            winner_ids = self.break_tie(tied_players)
            winners = [f"Player {id}" for id in winner_ids]
        else:
            winners = [f"Player {playerScores[0]['id']}"]

        return {
            'playerScores': playerScores,
            'winners': winners,
            'prompt': prompt
        }


    def display_result(self, evaluationResult: Dict[str, Any]):
        """Display the winner and scores in a readable format"""

        playerScores = evaluationResult['playerScores']
        winners = evaluationResult['winners']
        prompt = evaluationResult['prompt']

        print("\n" + "=" * 50)
        print("GAME RESULTS")
        print("=" * 50)
        print(f"Prompt: {prompt}\n")

        print("Scores:")
        for scoreData in playerScores:
            print(f"Player {scoreData['id']} ('{scoreData['word']}'): {scoreData['total']:.1f} points")
            print(f"\n  - Commonality: {scoreData['commonality']:.1f}/10")
            print(f" - Spelling Complexity: {scoreData['complexity']:.1f}/10")
            print(f" - Prompt Compatability: {scoreData['compatability']:.1f}/10\n")

        print(f"\nWinner(s): {', '.join(winners)}!")

        if len(winners) > 1:
            print("It's a tie! The winning words are equally uncommon.")
        else:
            winnerData = next(score for score in playerScores if f"Player {score['id']}" == winners[0])
            print(f"'{winnerData['word']}' (score: {winnerData['total']:.1f}) is the least common word!")

        print("=" * 50)


    def start_new_game(self, llm):
        """Start a new game with multiple players"""

        print("\n" + "*" * 40)
        print("START NEW GAME")
        print("*" * 40)

        # Get number of players
        player_count = self.get_player_count()

        # Generate Prompt
        prompt = self.generate_prompt(llm, "")
        print(f"\nPrompt: {prompt}\n")

        # Get player inputs
        words = {}
        for i in range(1, player_count + 1):
            words[i] = self.get_player_input(i)

        # Evaluate words
        evaluation = self.evaluate_words(llm, prompt, words)

        # Display results
        self.display_result(evaluation)

        return {
            'prompt': prompt,
            'player_words': words,
            'evaluationResult': evaluation
        }