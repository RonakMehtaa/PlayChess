/**
 * API Client for Chess Backend
 * Handles all communication with FastAPI backend
 */
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Start a new game
 * @param {string} playerColor - 'white' or 'black'
 * @param {number} botElo - Bot ELO rating (1320-3000)
 * @returns {Promise<Object>} Game state
 */
export const startGame = async (playerColor, botElo) => {
  const response = await apiClient.post('/start_game', {
    player_color: playerColor,
    bot_elo: botElo
  });
  return response.data;
};

/**
 * Send player's move to backend
 * @param {string} gameId - Unique game identifier
 * @param {string} move - Move in UCI format (e.g., "e2e4")
 * @returns {Promise} Updated game state with bot's response
 */
export const sendPlayerMove = async (gameId, move) => {
  try {
    const response = await apiClient.post('/player_move', {
      game_id: gameId,
      move: move,
    });
    return response.data;
  } catch (error) {
    console.error('Error sending move:', error);
    throw error;
  }
};

/**
 * Get current game state
 * @param {string} gameId - Unique game identifier
 * @returns {Promise} Complete game state
 */
export const getGameState = async (gameId) => {
  try {
    const response = await apiClient.get(`/state/${gameId}`);
    return response.data;
  } catch (error) {
    console.error('Error getting game state:', error);
    throw error;
  }
};

/**
 * Delete a game
 * @param {string} gameId - Unique game identifier
 * @returns {Promise}
 */
export const deleteGame = async (gameId) => {
  try {
    const response = await apiClient.delete(`/game/${gameId}`);
    return response.data;
  } catch (error) {
    console.error('Error deleting game:', error);
    throw error;
  }
};

/**
 * Get all active games
 * @returns {Promise} List of all games
 */
export const getAllGames = async () => {
  try {
    const response = await apiClient.get('/games');
    return response.data;
  } catch (error) {
    console.error('Error getting games:', error);
    throw error;
  }
};

/**
 * Health check
 * @returns {Promise} Server status
 */
export const healthCheck = async () => {
  try {
    const response = await apiClient.get('/');
    return response.data;
  } catch (error) {
    console.error('Error checking health:', error);
    throw error;
  }
};

export default apiClient;
