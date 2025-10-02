import React, { useState } from 'react';

const Test = () => {
  const [playerCount, setPlayerCount] = useState(2);
  const [prompt, setPrompt] = useState('');
  const [playerWords, setPlayerWords] = useState({}); // Stores words like {1: "word", 2: "another"}
  const [evaluationResult, setEvaluationResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const API_BASE_URL = 'http://localhost:5000'; // Your Flask API URL

  const handlePlayerCountChange = (e) => {
    setPlayerCount(parseInt(e.target.value, 10));
    setPlayerWords({}); // Reset words when player count changes
  };

  const handleWordChange = (playerId, word) => {
    setPlayerWords(prevWords => ({
      ...prevWords,
      [playerId]: word
    }));
  };

  const startNewGame = async () => {
    setLoading(true);
    setError(null);
    setEvaluationResult(null);
    setPlayerWords({}); // Clear previous words

    try {
      const response = await fetch(`${API_BASE_URL}/start_game`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ player_count: playerCount, theme: 'nature' }), // Example theme
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to start game');
      }

      const data = await response.json();
      setPrompt(data.prompt);
      // Initialize player words state for the number of players
      const initialWords = {};
      for (let i = 1; i <= data.player_count; i++) {
        initialWords[i] = '';
      }
      setPlayerWords(initialWords);

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const submitWords = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    // Basic validation to ensure all players have entered a word
    const allWordsEntered = Object.values(playerWords).every(word => word.trim() !== '');
    if (!allWordsEntered) {
      setError("Please ensure all players have entered a word.");
      setLoading(false);
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/submit_words`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt, player_words: playerWords }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to submit words');
      }

      const data = await response.json();
      setEvaluationResult(data); // Store the full evaluation result
      console.log(data);

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const renderPlayerInputs = () => {
    const inputs = [];
    for (let i = 1; i <= playerCount; i++) {
      inputs.push(
        <div key={i} className="player-input-group">
          <label htmlFor={`player-${i}`}>Player {i}:</label>
          <textarea
            id={`player-${i}`}
            value={playerWords[i] || ''}
            onChange={(e) => handleWordChange(i, e.target.value)}
            disabled={!prompt || loading}
            rows="1"
          ></textarea>
        </div>
      );
    }
    return inputs;
  };

  return (
    <div className="game-container">
      <h1>The Notebook Word Game</h1>

      <div className="controls">
        <label htmlFor="player-count">Number of Players:</label>
        <select id="player-count" value={playerCount} onChange={handlePlayerCountChange} disabled={loading || prompt}>
          {[2, 3, 4, 5].map(num => (
            <option key={num} value={num}>{num}</option>
          ))}
        </select>
        <button onClick={startNewGame} disabled={loading || prompt}>
          {loading && !prompt ? 'Generating Prompt...' : 'Start New Game'}
        </button>
      </div>

      {error && <p className="error-message">Error: {error}</p>}

      {prompt && (
        <div className="game-area">
          <p className="prompt-display">
            <strong>Prompt:</strong> {prompt}
          </p>

          <form onSubmit={submitWords}>
            <div className="player-inputs">
              {renderPlayerInputs()}
            </div>
            <button type="submit" disabled={loading}>
              {loading ? 'Submitting...' : 'Submit Words'}
            </button>
          </form>

          {evaluationResult && (
            <div className="results-display">
              <h2>Game Results</h2>
              <p>Prompt: {evaluationResult.prompt}</p>
              <h3>Scores:</h3>
              {evaluationResult.playerScores.map((scoreData) => (
                <div key={scoreData.id} className="player-score-card">
                  <p>
                    <strong>Player {scoreData.id} ('{scoreData.word}'):</strong>{' '}
                    {scoreData.total.toFixed(1)} points
                  </p>
                  {/* You can display more detailed scores here if needed,
                      based on whether you use separate or combined scoring in backend.
                      For combined scoring, `criteriaResult` is the main score. */}
                      {/* Example for combined scoring: */}
                      {scoreData.criteriaResult && (
                         <p className="detail-score">  - Criteria Result: {scoreData.criteriaResult.toFixed(1)}</p>
                      )}
                </div>
              ))}
              <h3>Winner(s): {evaluationResult.winners.join(', ')}!</h3>
              {evaluationResult.winners.length > 1 && (
                <p>It's a tie! The winning words are equally uncommon.</p>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Test;