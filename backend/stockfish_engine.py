"""
Stockfish Chess Engine Wrapper
Manages Stockfish initialization and move generation with configurable skill levels.
"""
import chess
import chess.engine
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class StockfishEngine:
    """Wrapper for Stockfish chess engine with skill level management."""
    
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
        skill_level: int = 10,
        move_time: float = 0.2
    ) -> Tuple[chess.Move, Optional[int]]:
        """
        Get best move from Stockfish based on skill level.
        
        Args:
            board: Current chess board state
            skill_level: Skill level 0-20 (0 = weakest, 20 = strongest)
            move_time: Time limit for move calculation in seconds
            
        Returns:
            Tuple of (best_move, score_cp) where score_cp is centipawn evaluation
        """
        if not self.engine:
            raise RuntimeError("Stockfish engine not initialized")
        
        # Clamp skill level to valid range
        skill_level = max(0, min(20, skill_level))
        
        # Configure engine options based on skill level
        self.engine.configure({
            "Skill Level": skill_level,
            "UCI_LimitStrength": skill_level < 20,
            "UCI_Elo": self._skill_to_elo(skill_level) if skill_level < 20 else 3000
        })
        
        # Calculate move time based on skill level
        # Higher levels get slightly more time to think
        adjusted_time = move_time * (1 + skill_level / 40)
        
        # Get best move with time limit
        result = self.engine.play(
            board,
            chess.engine.Limit(time=adjusted_time),
            info=chess.engine.INFO_SCORE
        )
        
        # Extract score if available
        score_cp = None
        if hasattr(result, 'info') and 'score' in result.info:
            score = result.info['score']
            if score.relative and hasattr(score.relative, 'score'):
                score_cp = score.relative.score()
        
        return result.move, score_cp
    
    def _skill_to_elo(self, skill_level: int) -> int:
        """
        Convert skill level (0-20) to approximate ELO rating.
        
        Args:
            skill_level: Skill level 0-20
            
        Returns:
            Approximate ELO rating (minimum 1320 per Stockfish requirement)
        """
        # Mapping: Level 0 ≈ 1320 ELO (Stockfish minimum), Level 20 ≈ 3000 ELO
        return int(1320 + (skill_level * 84))
    
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
