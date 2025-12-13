"""
Game Manager
Manages chess game state in-memory with unique game IDs.
"""
import uuid
import chess
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class GameState:
    """Represents the state of a chess game."""
    game_id: str
    board_fen: str
    player_color: str  # "white" or "black"
    bot_elo: int  # 1320-3000
    move_history: List[str]
    status: str  # "ongoing", "checkmate", "stalemate", "draw"
    winner: Optional[str]  # "white", "black", or None
    current_turn: str  # "white" or "black"
    created_at: str
    last_move: Optional[str]
    
    def to_dict(self):
        """Convert to dictionary."""
        return asdict(self)


class GameManager:
    """Manages multiple chess games in memory."""
    
    # ELO rating constraints
    MIN_ELO = 1320
    MAX_ELO = 3000
    
    def __init__(self):
        """Initialize the game manager with empty game storage."""
        self.games: Dict[str, GameState] = {}
        logger.info("Game manager initialized")
    
    def create_game(self, player_color: str, bot_elo: int) -> GameState:
        """
        Create a new chess game.
        
        Args:
            player_color: "white" or "black"
            bot_elo: Bot ELO rating (1320-3000)
            
        Returns:
            GameState object
        """
        # Validate inputs
        if player_color not in ["white", "black"]:
            raise ValueError("player_color must be 'white' or 'black'")
        
        bot_elo = max(self.MIN_ELO, min(self.MAX_ELO, bot_elo))
        
        # Create new game
        game_id = str(uuid.uuid4())
        board = chess.Board()
        
        game_state = GameState(
            game_id=game_id,
            board_fen=board.fen(),
            player_color=player_color,
            bot_elo=bot_elo,
            move_history=[],
            status="ongoing",
            winner=None,
            current_turn="white",
            created_at=datetime.utcnow().isoformat(),
            last_move=None
        )
        
        self.games[game_id] = game_state
        logger.info(f"Created game {game_id}: {player_color} vs bot (ELO {bot_elo})")
        
        return game_state
    
    def get_game(self, game_id: str) -> Optional[GameState]:
        """
        Retrieve a game by ID.
        
        Args:
            game_id: Unique game identifier
            
        Returns:
            GameState object or None if not found
        """
        return self.games.get(game_id)
    
    def apply_move(self, game_id: str, move_uci: str) -> bool:
        """
        Apply a move to the game board.
        
        Args:
            game_id: Unique game identifier
            move_uci: Move in UCI format (e.g., "e2e4")
            
        Returns:
            True if move was applied successfully, False otherwise
        """
        game = self.get_game(game_id)
        if not game:
            logger.warning(f"Game {game_id} not found")
            return False
        
        try:
            board = chess.Board(game.board_fen)
            move = chess.Move.from_uci(move_uci)
            
            # Validate move is legal
            if move not in board.legal_moves:
                logger.warning(f"Illegal move {move_uci} in game {game_id}")
                return False
            
            # Apply move
            board.push(move)
            
            # Update game state
            game.board_fen = board.fen()
            game.move_history.append(move_uci)
            game.last_move = move_uci
            game.current_turn = "white" if board.turn == chess.WHITE else "black"
            
            # Check game status
            self._update_game_status(game, board)
            
            logger.info(f"Applied move {move_uci} in game {game_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error applying move {move_uci} in game {game_id}: {e}")
            return False
    
    def _update_game_status(self, game: GameState, board: chess.Board):
        """
        Update game status based on board state.
        
        Args:
            game: GameState object to update
            board: Current chess board
        """
        if board.is_checkmate():
            game.status = "checkmate"
            # Winner is the player who just moved (opposite of current turn)
            game.winner = "black" if board.turn == chess.WHITE else "white"
            logger.info(f"Game {game.game_id} ended: checkmate, winner: {game.winner}")
        elif board.is_stalemate():
            game.status = "stalemate"
            game.winner = None
            logger.info(f"Game {game.game_id} ended: stalemate")
        elif board.is_insufficient_material():
            game.status = "draw"
            game.winner = None
            logger.info(f"Game {game.game_id} ended: insufficient material")
        elif board.can_claim_fifty_moves():
            game.status = "draw"
            game.winner = None
            logger.info(f"Game {game.game_id} ended: fifty-move rule")
        elif board.can_claim_threefold_repetition():
            game.status = "draw"
            game.winner = None
            logger.info(f"Game {game.game_id} ended: threefold repetition")
        else:
            game.status = "ongoing"
    
    def get_legal_moves(self, game_id: str) -> List[str]:
        """
        Get all legal moves for current position.
        
        Args:
            game_id: Unique game identifier
            
        Returns:
            List of legal moves in UCI format
        """
        game = self.get_game(game_id)
        if not game:
            return []
        
        board = chess.Board(game.board_fen)
        return [move.uci() for move in board.legal_moves]
    
    def delete_game(self, game_id: str) -> bool:
        """
        Delete a game from memory.
        
        Args:
            game_id: Unique game identifier
            
        Returns:
            True if game was deleted, False if not found
        """
        if game_id in self.games:
            del self.games[game_id]
            logger.info(f"Deleted game {game_id}")
            return True
        return False
    
    def get_all_games(self) -> List[GameState]:
        """Get all active games."""
        return list(self.games.values())
    
    def get_game_count(self) -> int:
        """Get total number of active games."""
        return len(self.games)
