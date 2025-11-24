"""
FastAPI Backend for Chess Web App
Provides REST API for playing chess against Stockfish.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
import chess
import logging
import os
from contextlib import asynccontextmanager

from stockfish_engine import StockfishEngine
from game_manager import GameManager, GameState

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global instances
game_manager: Optional[GameManager] = None
stockfish: Optional[StockfishEngine] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup resources."""
    global game_manager, stockfish
    
    # Startup
    logger.info("Starting Chess API backend...")
    
    # Initialize game manager
    game_manager = GameManager()
    
    # Initialize Stockfish
    # Try common Stockfish paths for different environments
    stockfish_path = os.getenv("STOCKFISH_PATH")
    if not stockfish_path:
        # Try common locations
        import subprocess
        import shutil
        
        # First, try to find stockfish in PATH
        stockfish_in_path = shutil.which("stockfish")
        if stockfish_in_path:
            stockfish_path = stockfish_in_path
            logger.info(f"Found Stockfish in PATH: {stockfish_path}")
        else:
            # Try specific paths
            for path in ["/usr/games/stockfish", "/usr/bin/stockfish", "/usr/local/bin/stockfish"]:
                if os.path.exists(path):
                    try:
                        subprocess.run([path, "--version"], capture_output=True, timeout=1, check=True)
                        stockfish_path = path
                        logger.info(f"Found Stockfish at: {path}")
                        break
                    except Exception as e:
                        logger.debug(f"Failed to verify {path}: {e}")
                        continue
    
    if not stockfish_path:
        logger.error("Stockfish not found in any common location")
        stockfish_path = "stockfish"  # Last resort - try anyway
    
    try:
        stockfish = StockfishEngine(stockfish_path)
        logger.info(f"Stockfish initialized successfully from: {stockfish_path}")
    except Exception as e:
        logger.error(f"Failed to initialize Stockfish: {e}")
        logger.warning("Server will start but games will fail without Stockfish")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Chess API backend...")
    if stockfish:
        stockfish.close()


# Create FastAPI app
app = FastAPI(
    title="Chess Web App API",
    description="REST API for playing chess against Stockfish",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
# Allow local development and Vercel deployments
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
if "*" not in allowed_origins:
    # Add common Vercel patterns
    allowed_origins.extend([
        "https://*.vercel.app",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for development; restrict in production via ALLOWED_ORIGINS env var
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class StartGameRequest(BaseModel):
    player_color: str = Field(..., pattern="^(white|black)$", description="Player color: white or black")
    bot_level: int = Field(..., ge=0, le=20, description="Bot difficulty level (0-20)")


class StartGameResponse(BaseModel):
    game_id: str
    board_fen: str
    current_turn: str
    player_color: str
    bot_level: int
    bot_move: Optional[str] = None  # If player is black, bot makes first move


class PlayerMoveRequest(BaseModel):
    game_id: str
    move: str = Field(..., description="Move in UCI format (e.g., e2e4)")


class PlayerMoveResponse(BaseModel):
    success: bool
    board_fen: str
    bot_move: Optional[str] = None
    status: str
    winner: Optional[str] = None
    message: Optional[str] = None
    evaluation: Optional[int] = None  # Centipawn evaluation


class GameStateResponse(BaseModel):
    game_id: str
    board_fen: str
    player_color: str
    bot_level: int
    move_history: List[str]
    status: str
    winner: Optional[str]
    current_turn: str
    legal_moves: List[str]


# API Endpoints
@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "message": "Chess Web App API",
        "status": "running",
        "stockfish_ready": stockfish is not None,
        "active_games": game_manager.get_game_count() if game_manager else 0
    }


@app.get("/health")
async def health_check():
    """Railway health check endpoint."""
    return {"status": "healthy"}


@app.post("/start_game", response_model=StartGameResponse)
async def start_game(request: StartGameRequest):
    """
    Start a new chess game.
    
    Creates a new game with specified player color and bot difficulty.
    If player chooses black, bot makes the first move.
    """
    if not game_manager:
        raise HTTPException(status_code=500, detail="Game manager not initialized")
    
    if not stockfish:
        raise HTTPException(status_code=500, detail="Stockfish engine not available")
    
    try:
        # Create new game
        game = game_manager.create_game(request.player_color, request.bot_level)
        
        response_data = {
            "game_id": game.game_id,
            "board_fen": game.board_fen,
            "current_turn": game.current_turn,
            "player_color": game.player_color,
            "bot_level": game.bot_level,
            "bot_move": None
        }
        
        # If player is black, bot (white) makes first move
        if request.player_color == "black":
            board = chess.Board(game.board_fen)
            bot_move, _ = stockfish.get_best_move(board, request.bot_level)
            
            # Apply bot move
            game_manager.apply_move(game.game_id, bot_move.uci())
            updated_game = game_manager.get_game(game.game_id)
            
            response_data["bot_move"] = bot_move.uci()
            response_data["board_fen"] = updated_game.board_fen
            response_data["current_turn"] = updated_game.current_turn
        
        logger.info(f"Started game {game.game_id}")
        return response_data
        
    except Exception as e:
        logger.error(f"Error starting game: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/player_move", response_model=PlayerMoveResponse)
async def player_move(request: PlayerMoveRequest):
    """
    Process player's move and get bot's response.
    
    Validates player move, applies it, then gets and applies bot's move.
    Returns updated game state.
    """
    if not game_manager:
        raise HTTPException(status_code=500, detail="Game manager not initialized")
    
    if not stockfish:
        raise HTTPException(status_code=500, detail="Stockfish engine not available")
    
    game = game_manager.get_game(request.game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    if game.status != "ongoing":
        raise HTTPException(status_code=400, detail=f"Game is {game.status}")
    
    try:
        # Validate it's player's turn
        board = chess.Board(game.board_fen)
        player_turn = game.player_color == "white" and board.turn == chess.WHITE or \
                      game.player_color == "black" and board.turn == chess.BLACK
        
        if not player_turn:
            raise HTTPException(status_code=400, detail="Not player's turn")
        
        # Apply player move
        if not game_manager.apply_move(request.game_id, request.move):
            raise HTTPException(status_code=400, detail="Invalid move")
        
        # Get updated game state
        game = game_manager.get_game(request.game_id)
        
        # If game ended after player move, return status
        if game.status != "ongoing":
            return PlayerMoveResponse(
                success=True,
                board_fen=game.board_fen,
                bot_move=None,
                status=game.status,
                winner=game.winner,
                message=f"Game ended: {game.status}"
            )
        
        # Get bot move
        board = chess.Board(game.board_fen)
        bot_move, evaluation = stockfish.get_best_move(board, game.bot_level)
        
        # Apply bot move
        game_manager.apply_move(request.game_id, bot_move.uci())
        game = game_manager.get_game(request.game_id)
        
        return PlayerMoveResponse(
            success=True,
            board_fen=game.board_fen,
            bot_move=bot_move.uci(),
            status=game.status,
            winner=game.winner,
            evaluation=evaluation
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing move: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/state/{game_id}", response_model=GameStateResponse)
async def get_game_state(game_id: str):
    """
    Get current state of a game.
    
    Returns complete game state including position, history, and legal moves.
    """
    if not game_manager:
        raise HTTPException(status_code=500, detail="Game manager not initialized")
    
    game = game_manager.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    # Get legal moves
    legal_moves = game_manager.get_legal_moves(game_id)
    
    return GameStateResponse(
        game_id=game.game_id,
        board_fen=game.board_fen,
        player_color=game.player_color,
        bot_level=game.bot_level,
        move_history=game.move_history,
        status=game.status,
        winner=game.winner,
        current_turn=game.current_turn,
        legal_moves=legal_moves
    )


@app.delete("/game/{game_id}")
async def delete_game(game_id: str):
    """Delete a game from memory."""
    if not game_manager:
        raise HTTPException(status_code=500, detail="Game manager not initialized")
    
    if game_manager.delete_game(game_id):
        return {"message": "Game deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Game not found")


@app.get("/games")
async def list_games():
    """List all active games."""
    if not game_manager:
        raise HTTPException(status_code=500, detail="Game manager not initialized")
    
    games = game_manager.get_all_games()
    return {
        "count": len(games),
        "games": [game.to_dict() for game in games]
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
