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
  const [botLevel, setBotLevel] = useState(10);
  const [gameStatus, setGameStatus] = useState('setup'); // setup, playing, ended
  const [statusMessage, setStatusMessage] = useState('');
  const [moveHistory, setMoveHistory] = useState([]);
  const [isThinking, setIsThinking] = useState(false);
  const [evaluation, setEvaluation] = useState(null);

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

      const response = await startGame(playerColor, botLevel);
      
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
  const onDrop = async (sourceSquare, targetSquare) => {
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
    try {
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

      // Move is valid, send to backend
      setIsThinking(true);
      setStatusMessage('Bot is thinking...');

      const response = await sendPlayerMove(gameId, move);

      if (response.success) {
        // Update game with new position
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
        return true;
      } else {
        setStatusMessage('Invalid move!');
        setIsThinking(false);
        return false;
      }
    } catch (error) {
      console.error('Error making move:', error);
      setStatusMessage('Error processing move.');
      setIsThinking(false);
      return false;
    }
  };

  // Format evaluation score
  const formatEvaluation = (score) => {
    if (score === null || score === undefined) return 'N/A';
    const pawns = (score / 100).toFixed(2);
    return pawns > 0 ? `+${pawns}` : pawns;
  };

  // Get difficulty label
  const getDifficultyLabel = (level) => {
    if (level <= 5) return 'Beginner';
    if (level <= 10) return 'Intermediate';
    if (level <= 15) return 'Advanced';
    return 'Expert';
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
                <label>Bot Difficulty: {botLevel} ({getDifficultyLabel(botLevel)})</label>
                <input
                  type="range"
                  min="0"
                  max="20"
                  value={botLevel}
                  onChange={(e) => setBotLevel(parseInt(e.target.value))}
                  className="slider"
                />
                <div className="difficulty-labels">
                  <span>0 (Easy)</span>
                  <span>20 (Hard)</span>
                </div>
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
                <strong>Bot Level:</strong> {botLevel} ({getDifficultyLabel(botLevel)})
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
            <li>Select bot difficulty (0-20)</li>
            <li>Click "Start Game"</li>
            <li>Drag and drop pieces to move</li>
            <li>Bot responds automatically</li>
          </ul>

          <h3>Difficulty Guide</h3>
          <div className="difficulty-guide">
            <div className="guide-item">
              <strong>0-5:</strong> Beginner<br/>
              <small>Makes obvious mistakes</small>
            </div>
            <div className="guide-item">
              <strong>6-10:</strong> Intermediate<br/>
              <small>Casual player level</small>
            </div>
            <div className="guide-item">
              <strong>11-15:</strong> Advanced<br/>
              <small>Club player level</small>
            </div>
            <div className="guide-item">
              <strong>16-20:</strong> Expert<br/>
              <small>Master level play</small>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChessBoard;
