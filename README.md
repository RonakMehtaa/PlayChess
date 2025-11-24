# ♟️ Chess Web App - Play Against Stockfish

A full-stack web application where you can play chess against Stockfish AI with adjustable difficulty levels (0-20).

**Tech Stack:**
- **Frontend:** React.js with react-chessboard and chess.js
- **Backend:** FastAPI (Python)
- **Chess Engine:** Stockfish
- **Move Validation:** python-chess

## 📋 Features

✅ Play as White or Black  
✅ Adjustable bot difficulty (0-20 skill levels)  
✅ Interactive drag-and-drop chessboard  
✅ Real-time move validation  
✅ Move history tracking  
✅ Position evaluation display  
✅ Automatic checkmate/stalemate/draw detection  
✅ Beautiful, responsive UI  

---

## 🚀 Quick Start Guide

### Prerequisites

- **Python 3.8+** installed
- **Node.js 14+** and npm installed
- **Stockfish** chess engine installed

---

## 📥 Installation Instructions

### 1. Install Stockfish

#### **Windows:**
1. Download from: https://stockfishchess.org/download/
2. Extract to a folder (e.g., `C:\stockfish\`)
3. Note the path to `stockfish.exe`

#### **macOS:**
```bash
brew install stockfish
```

#### **Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install stockfish
```

To verify installation:
```bash
# Windows
stockfish.exe

# macOS/Linux
stockfish
```

You should see the Stockfish engine start. Type `quit` to exit.

---

### 2. Backend Setup

Navigate to the backend directory:

```powershell
cd c:\Users\rme\PlayChess\backend
```

#### Create a virtual environment (recommended):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### Install Python dependencies:

```powershell
pip install -r requirements.txt
```

#### Set Stockfish path (Windows):

**Option 1: Environment Variable (Recommended)**
```powershell
$env:STOCKFISH_PATH="C:\path\to\stockfish.exe"
```

**Option 2: Add to system PATH**
Add the Stockfish directory to your system PATH, then the backend will find it automatically.

**Option 3: Use default**
If `stockfish` or `stockfish.exe` is in your PATH, no configuration needed.

#### Run the backend:

```powershell
python main.py
```

Or using uvicorn directly:

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will start at: **http://localhost:8000**

Verify it's running by visiting: http://localhost:8000
You should see:
```json
{
  "message": "Chess Web App API",
  "status": "running",
  "stockfish_ready": true,
  "active_games": 0
}
```

---

### 3. Frontend Setup

Open a **new terminal** and navigate to the frontend directory:

```powershell
cd c:\Users\rme\PlayChess\frontend
```

#### Install Node dependencies:

```powershell
npm install
```

#### Start the React development server:

```powershell
npm start
```

The frontend will automatically open in your browser at: **http://localhost:3000**

---

## 🎮 How to Play

1. **Choose your color:** Select White or Black
2. **Set difficulty:** Use the slider to choose bot strength (0-20)
   - 0-5: Beginner (makes mistakes)
   - 6-10: Intermediate (casual player)
   - 11-15: Advanced (club level)
   - 16-20: Expert (master level)
3. **Start the game:** Click "Start Game"
4. **Make moves:** Drag and drop pieces on the board
5. **The bot responds automatically** after each move
6. **Game ends** on checkmate, stalemate, or draw

---

## 🧪 Testing the API

### Using PowerShell (curl equivalent)

**Health Check:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000" -Method Get
```

**Start a new game:**
```powershell
$body = @{
    player_color = "white"
    bot_level = 10
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/start_game" -Method Post -Body $body -ContentType "application/json"
```

**Make a move:**
```powershell
$body = @{
    game_id = "YOUR_GAME_ID_HERE"
    move = "e2e4"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/player_move" -Method Post -Body $body -ContentType "application/json"
```

**Get game state:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/state/YOUR_GAME_ID_HERE" -Method Get
```

### Using curl (if installed on Windows)

**Start a game:**
```bash
curl -X POST "http://localhost:8000/start_game" \
  -H "Content-Type: application/json" \
  -d "{\"player_color\": \"white\", \"bot_level\": 10}"
```

**Make a move:**
```bash
curl -X POST "http://localhost:8000/player_move" \
  -H "Content-Type: application/json" \
  -d "{\"game_id\": \"YOUR_GAME_ID\", \"move\": \"e2e4\"}"
```

---

## 📁 Project Structure

```
PlayChess/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── stockfish_engine.py     # Stockfish wrapper
│   ├── game_manager.py         # Game state management
│   └── requirements.txt        # Python dependencies
│
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── api/
│   │   │   └── client.js       # Backend API client
│   │   ├── components/
│   │   │   ├── ChessBoard.jsx  # Main chess component
│   │   │   └── ChessBoard.css  # Component styles
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── index.js
│   │   └── index.css
│   ├── package.json
│   └── .env                    # Environment variables
│
└── README.md
```

---

## 🔧 API Endpoints

### `POST /start_game`
Start a new chess game.

**Request:**
```json
{
  "player_color": "white",  // "white" or "black"
  "bot_level": 10           // 0-20
}
```

**Response:**
```json
{
  "game_id": "uuid-here",
  "board_fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
  "current_turn": "white",
  "player_color": "white",
  "bot_level": 10,
  "bot_move": null
}
```

### `POST /player_move`
Send a player move and get bot's response.

**Request:**
```json
{
  "game_id": "uuid-here",
  "move": "e2e4"  // UCI format
}
```

**Response:**
```json
{
  "success": true,
  "board_fen": "updated-fen",
  "bot_move": "e7e5",
  "status": "ongoing",
  "winner": null,
  "evaluation": 15
}
```

### `GET /state/{game_id}`
Get current game state.

**Response:**
```json
{
  "game_id": "uuid-here",
  "board_fen": "current-fen",
  "player_color": "white",
  "bot_level": 10,
  "move_history": ["e2e4", "e7e5"],
  "status": "ongoing",
  "winner": null,
  "current_turn": "white",
  "legal_moves": ["a2a3", "a2a4", ...]
}
```

### `GET /`
Health check endpoint.

### `DELETE /game/{game_id}`
Delete a game from memory.

### `GET /games`
List all active games.

---

## 🎨 Customization

### Adjust Bot Thinking Time

Edit `backend/stockfish_engine.py`:
```python
def get_best_move(self, board, skill_level=10, move_time=0.2):
    # Change move_time (in seconds)
```

### Change Board Theme

The app uses `react-chessboard` which supports themes. Edit `ChessBoard.jsx`:
```jsx
<Chessboard
  customBoardStyle={{
    borderRadius: '4px',
    boxShadow: '0 5px 15px rgba(0, 0, 0, 0.5)',
  }}
  customDarkSquareStyle={{ backgroundColor: '#779952' }}
  customLightSquareStyle={{ backgroundColor: '#edeed1' }}
/>
```

### Enable HTTPS (Production)

For production, update CORS settings in `backend/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🐛 Troubleshooting

### Backend won't start
- **Error:** `Could not start Stockfish engine`
  - ✅ Make sure Stockfish is installed
  - ✅ Set `STOCKFISH_PATH` environment variable correctly
  - ✅ On Windows, use full path like `C:\stockfish\stockfish.exe`

### Frontend can't connect to backend
- **Error:** Network error when starting game
  - ✅ Make sure backend is running on http://localhost:8000
  - ✅ Check `.env` file has `REACT_APP_API_URL=http://localhost:8000`
  - ✅ Restart React dev server after changing `.env`

### Illegal move errors
- ✅ Make sure you're moving on your turn
- ✅ The move must be legal according to chess rules
- ✅ Promotion is always to Queen (simplification)

### CORS errors
- ✅ Backend CORS is configured for all origins (`*`)
- ✅ If issues persist, check browser console for details

---

## 📝 Move Format

Moves use **UCI (Universal Chess Interface)** format:
- Format: `[from_square][to_square][promotion]`
- Examples:
  - `e2e4` - Pawn from e2 to e4
  - `e1g1` - Kingside castling
  - `e7e8q` - Pawn promotion to queen

---

## 🚀 Production Deployment

### Backend
```bash
# Install production server
pip install gunicorn

# Run with gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend
```bash
# Build for production
npm run build

# Serve the build folder with any static server
# Example with serve:
npx serve -s build
```

---

## 📦 Dependencies

### Backend
- `fastapi` - Modern web framework
- `uvicorn` - ASGI server
- `pydantic` - Data validation
- `python-chess` - Chess library

### Frontend
- `react` - UI framework
- `react-chessboard` - Chess board component
- `chess.js` - Chess logic
- `axios` - HTTP client

---

## 🎯 Future Enhancements

Possible additions:
- 🎨 Multiple board themes
- 💾 Game save/load functionality
- 📊 Move analysis and hints
- 🤖 Bot personalities (aggressive, defensive, etc.)
- 📚 Opening book integration
- 📈 Player statistics tracking
- 🌐 Multiplayer support
- ⏱️ Time controls

---

## 📄 License

This project is open source and available for educational purposes.

---

## 🙏 Credits

- **Stockfish** - Chess engine (https://stockfishchess.org/)
- **python-chess** - Python chess library
- **react-chessboard** - React chessboard component
- **FastAPI** - Modern Python web framework

---

## 💡 Tips for Best Experience

1. **Start with lower difficulty** (5-10) to learn
2. **Watch the move history** to review the game
3. **Use the evaluation** to understand position strength
4. **Try different colors** - playing as black is a different challenge
5. **Experiment with difficulty** - even level 15 is very strong

---

Enjoy playing chess! 🎉
