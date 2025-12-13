"""
Stockfish Chess Engine Wrapper
Manages Stockfish initialization and move generation with ELO-based difficulty.
"""
import chess
import chess.engine
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class StockfishEngine:
    """Wrapper for Stockfish chess engine with ELO rating management."""
    
    # Stockfish rating constraints
    MIN_ELO = 1320
    MAX_ELO = 3000
    
    def __init__(self, stockfish_path: str):
        """
        Initialize Stockfish engine.
        
        Args:
            stockfish_path: Path to Stockfish executable
        """
        self.stockfish_path = stockfish_path
        self.engine: Optional[chess.engine.SimpleEngine] = None
        self._init_engine()
    
    def _init_engine(self):
        """Initialize the Stockfish engine."""
        try:
            self.engine = chess.engine.SimpleEngine.popen_uci(self.stockfish_path)
            logger.info("Stockfish engine initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Stockfish: {e}")
            raise RuntimeError(f"Could not start Stockfish engine: {e}")
    
    def get_best_move(
        self, 
        board: chess.Board, 
        elo_rating: int = 1500,
        move_time: float = 0.2
    ) -> Tuple[chess.Move, Optional[int]]:
        """
        Get best move from Stockfish based on ELO rating.
        
        Args:
            board: Current chess board state
            elo_rating: Target ELO rating (1320-3000)
            move_time: Time limit for move calculation in seconds
            
        Returns:
            Tuple of (best_move, score_cp) where score_cp is centipawn evaluation
        """
        if not self.engine:
            raise RuntimeError("Stockfish engine not initialized")
        
        # Clamp ELO to valid range
        elo_rating = max(self.MIN_ELO, min(self.MAX_ELO, elo_rating))
        
        # Convert ELO to skill level for proper engine configuration
        skill_level = self._elo_to_skill(elo_rating)
        
        # Configure engine options based on ELO rating
        if elo_rating >= self.MAX_ELO:
            # Maximum strength - no limitations
            self.engine.configure({
                "Skill Level": 20,
                "UCI_LimitStrength": False,
            })
        else:
            # Limited strength mode
            self.engine.configure({
                "Skill Level": skill_level,
                "UCI_LimitStrength": True,
                "UCI_Elo": elo_rating
            })
        
        # Calculate move time based on rating
        # Higher ratings get slightly more time to think
        rating_factor = (elo_rating - self.MIN_ELO) / (self.MAX_ELO - self.MIN_ELO)
        adjusted_time = move_time * (1 + rating_factor * 0.5)
        
        # Get best move with time limit
        result = self.engine.play(
            board,
            chess.engine.Limit(time=adjusted_time),
            info=chess.engine.INFO_SCORE
        )
        
        # Ensure we have a valid move
        if result.move is None:
            raise RuntimeError("Stockfish failed to generate a move")
        
        # Extract score if available
        score_cp = None
        if hasattr(result, 'info') and 'score' in result.info:
            score = result.info['score']
            if score.relative and hasattr(score.relative, 'score'):
                score_cp = score.relative.score()
        
        return result.move, score_cp
    
    def _elo_to_skill(self, elo_rating: int) -> int:
        """
        Convert ELO rating to Stockfish skill level (0-20).
        
        Args:
            elo_rating: ELO rating (1320-3000)
            
        Returns:
            Skill level 0-20
        """
        # Linear mapping from ELO range to skill level
        skill = int((elo_rating - self.MIN_ELO) / (self.MAX_ELO - self.MIN_ELO) * 20)
        return max(0, min(20, skill))
    
    def get_evaluation(self, board: chess.Board, depth: int = 15) -> Optional[int]:
        """
        Get static evaluation of current position.
        
        Args:
            board: Current chess board state
            depth: Search depth for evaluation
            
        Returns:
            Evaluation in centipawns (positive = white advantage)
        """
        if not self.engine:
            raise RuntimeError("Stockfish engine not initialized")
        
        info = self.engine.analyse(board, chess.engine.Limit(depth=depth))
        
        if 'score' in info and info['score'].relative:
            score = info['score'].relative.score()
            if score is not None:
                # Flip score if black to move
                return score if board.turn == chess.WHITE else -score
        
        return None
    
    def close(self):
        """Close the Stockfish engine."""
        if self.engine:
            self.engine.quit()
            logger.info("Stockfish engine closed")
    
    def __del__(self):
        """Cleanup on deletion."""
        self.close()
