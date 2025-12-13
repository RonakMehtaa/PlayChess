/**
 * ChessBoard Component
 * Main interactive chess board with game controls
 */
import React, { useState } from 'react';
import { Chessboard } from 'react-chessboard';
import { Chess } from 'chess.js';
import { startGame, sendPlayerMove } from '../api/client';
import './ChessBoard.css';

const ChessBoard = () => {
  // Game state
  const [game, setGame] = useState(new Chess());
  const [gameId, setGameId] = useState(null);
  const [playerColor, setPlayerColor] = useState('white');
  const [botElo, setBotElo] = useState(1500);
  const [gameStatus, setGameStatus] = useState('setup'); // setup, playing, ended
  const [statusMessage, setStatusMessage] = useState('');
  const [moveHistory, setMoveHistory] = useState([]);
  const [isThinking, setIsThinking] = useState(false);
  const [evaluation, setEvaluation] = useState(null);

  // Available ELO ratings
  const availableRatings = [1320, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2200, 2400, 2600, 2800, 3000];

  // Reset game state
  const resetGame = () => {
    setGame(new Chess());
    setGameId(null);
    setGameStatus('setup');
    setStatusMessage('');
    setMoveHistory([]);
    setIsThinking(false);
    setEvaluation(null);
  };

  // Start new game
  const handleStartGame = async () => {
    try {
      setIsThinking(true);
      setStatusMessage('Starting game...');

      const response = await startGame(playerColor, botElo);
      
      setGameId(response.game_id);
      const newGame = new Chess(response.board_fen);
      setGame(newGame);
      setGameStatus('playing');
      setMoveHistory([]);

      // If bot made first move (player is black)
      if (response.bot_move) {
        setStatusMessage(`Bot played: ${response.bot_move}`);
        setMoveHistory([response.bot_move]);
      } else {
        setStatusMessage('Your turn!');
      }
      
      setIsThinking(false);
    } catch (error) {
      console.error('Error starting game:', error);
      setStatusMessage('Error starting game. Make sure backend is running.');
      setIsThinking(false);
    }
  };

  // Handle piece drop (player move)
  const onDrop = (sourceSquare, targetSquare) => {
    // Check if it's player's turn
    const isPlayerTurn = 
      (playerColor === 'white' && game.turn() === 'w') ||
      (playerColor === 'black' && game.turn() === 'b');

    if (!isPlayerTurn) {
      setStatusMessage("It's not your turn!");
      return false;
    }

    if (gameStatus !== 'playing') {
      return false;
    }

    // Create move in UCI format
    const move = sourceSquare + targetSquare;
    
    // Try move locally first for validation
    const gameCopy = new Chess(game.fen());
    const result = gameCopy.move({
      from: sourceSquare,
      to: targetSquare,
      promotion: 'q', // Always promote to queen for simplicity
    });

    if (result === null) {
      setStatusMessage('Illegal move!');
      return false;
    }

    // Move is valid locally, update immediately for responsiveness
    setGame(gameCopy);
    setIsThinking(true);
    setStatusMessage('Bot is thinking...');

    // Send to backend asynchronously
    sendPlayerMove(gameId, move)
      .then(response => {
        if (response.success) {
          // Update game with backend's authoritative position
          const newGame = new Chess(response.board_fen);
          setGame(newGame);

          // Update move history
          const newHistory = [...moveHistory, move];
          if (response.bot_move) {
            newHistory.push(response.bot_move);
            setStatusMessage(`Bot played: ${response.bot_move}`);
          }
          setMoveHistory(newHistory);

          // Update evaluation if available
          if (response.evaluation !== null && response.evaluation !== undefined) {
            setEvaluation(response.evaluation);
          }

          // Check game status
          if (response.status !== 'ongoing') {
            setGameStatus('ended');
            if (response.status === 'checkmate') {
              setStatusMessage(`Checkmate! ${response.winner} wins!`);
            } else if (response.status === 'stalemate') {
              setStatusMessage('Stalemate! Draw.');
            } else {
              setStatusMessage(`Game ended: ${response.status}`);
            }
          }

          setIsThinking(false);
        } else {
          // Revert the move if backend rejects it
          setGame(new Chess(game.fen()));
          setStatusMessage('Invalid move!');
          setIsThinking(false);
        }
      })
      .catch(error => {
        console.error('Error making move:', error);
        
        // Revert the optimistic update
        setGame(new Chess(game.fen()));
        
        // Check if it's a 404 error (game not found)
        if (error.response?.status === 404) {
          setStatusMessage('Game session expired. Please start a new game.');
          setGameStatus('ended');
          alert('Your game session has expired (server may have restarted). Please start a new game.');
        } else {
          setStatusMessage(`Error: ${error.response?.data?.detail || error.message}`);
        }
        
        setIsThinking(false);
      });

    // Return true immediately to allow the piece to move visually
    return true;
  };

  // Format evaluation score
  const formatEvaluation = (score) => {
    if (score === null || score === undefined) return 'N/A';
    const pawns = (score / 100).toFixed(2);
    return pawns > 0 ? `+${pawns}` : pawns;
  };

  // Get rating category label
  const getRatingCategory = (elo) => {
    if (elo < 1400) return 'Beginner';
    if (elo < 1600) return 'Casual Player';
    if (elo < 1800) return 'Intermediate';
    if (elo < 2000) return 'Advanced';
    if (elo < 2200) return 'Expert';
    if (elo < 2400) return 'Master';
    if (elo < 2600) return 'International Master';
    return 'Grandmaster';
  };

  return (
    <div className="chess-app">
      <div className="header">
        <h1>♟️ Chess vs Stockfish</h1>
      </div>

      <div className="game-container">
        {/* Left Panel: Game Controls */}
        <div className="controls-panel">
          <h2>Game Settings</h2>
          
          {gameStatus === 'setup' && (
            <div className="setup-controls">
              <div className="control-group">
                <label>Play as:</label>
                <select 
                  value={playerColor} 
                  onChange={(e) => setPlayerColor(e.target.value)}
                >
                  <option value="white">White</option>
                  <option value="black">Black</option>
                </select>
              </div>

              <div className="control-group">
                <label>Bot Rating: {botElo} ({getRatingCategory(botElo)})</label>
                <select 
                  value={botElo} 
                  onChange={(e) => setBotElo(parseInt(e.target.value))}
                  className="rating-select"
                >
                  {availableRatings.map(rating => (
                    <option key={rating} value={rating}>
                      {rating} - {getRatingCategory(rating)}
                    </option>
                  ))}
                </select>
              </div>

              <button 
                className="btn btn-primary" 
                onClick={handleStartGame}
                disabled={isThinking}
              >
                Start Game
              </button>
            </div>
          )}

          {gameStatus !== 'setup' && (
            <div className="game-info">
              <div className="info-item">
                <strong>Playing as:</strong> {playerColor}
              </div>
              <div className="info-item">
                <strong>Bot Rating:</strong> {botElo} ({getRatingCategory(botElo)})
              </div>
              <div className="info-item">
                <strong>Status:</strong> {gameStatus}
              </div>
              {evaluation !== null && (
                <div className="info-item">
                  <strong>Evaluation:</strong> {formatEvaluation(evaluation)}
                </div>
              )}
              
              <button 
                className="btn btn-secondary" 
                onClick={resetGame}
              >
                New Game
              </button>
            </div>
          )}

          {/* Move History */}
          <div className="move-history">
            <h3>Move History</h3>
            <div className="moves-list">
              {moveHistory.length === 0 && <p className="no-moves">No moves yet</p>}
              {moveHistory.map((move, index) => (
                <div key={index} className="move-item">
                  <span className="move-number">{Math.floor(index / 2) + 1}.</span>
                  <span className="move-text">{move}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Center: Chess Board */}
        <div className="board-container">
          <div className="board-wrapper">
            <Chessboard
              position={game.fen()}
              onPieceDrop={onDrop}
              boardOrientation={playerColor}
              customBoardStyle={{
                borderRadius: '4px',
                boxShadow: '0 5px 15px rgba(0, 0, 0, 0.5)',
              }}
              arePiecesDraggable={gameStatus === 'playing' && !isThinking}
            />
          </div>
          
          {/* Status Message */}
          <div className={`status-message ${isThinking ? 'thinking' : ''}`}>
            {isThinking && <span className="spinner">⏳</span>}
            {statusMessage}
          </div>
        </div>

        {/* Right Panel: Info */}
        <div className="info-panel">
          <h3>How to Play</h3>
          <ul className="instructions">
            <li>Choose your color (White/Black)</li>
            <li>Select bot ELO rating</li>
            <li>Click "Start Game"</li>
            <li>Drag and drop pieces to move</li>
            <li>Bot responds automatically</li>
          </ul>

          <h3>Rating Guide</h3>
          <div className="difficulty-guide">
            <div className="guide-item">
              <strong>1320-1400:</strong> Beginner<br/>
              <small>Learning the basics</small>
            </div>
            <div className="guide-item">
              <strong>1400-1600:</strong> Casual<br/>
              <small>Recreational player</small>
            </div>
            <div className="guide-item">
              <strong>1600-1800:</strong> Intermediate<br/>
              <small>Club player level</small>
            </div>
            <div className="guide-item">
              <strong>1800-2000:</strong> Advanced<br/>
              <small>Strong club player</small>
            </div>
            <div className="guide-item">
              <strong>2000-2200:</strong> Expert<br/>
              <small>Candidate Master</small>
            </div>
            <div className="guide-item">
              <strong>2200-2400:</strong> Master<br/>
              <small>FIDE Master level</small>
            </div>
            <div className="guide-item">
              <strong>2400+:</strong> Elite<br/>
              <small>Grandmaster level</small>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChessBoard;
