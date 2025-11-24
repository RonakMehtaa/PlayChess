# 📁 Project Structure Overview

```
PlayChess/
│
├── 📄 README.md                    # Main documentation
├── 📄 QUICKREF.md                  # Quick reference guide
├── 📄 .gitignore                   # Git ignore file
├── 🔧 start.ps1                    # PowerShell quick start script
├── 🔧 start.bat                    # Batch file quick start script
│
├── 📂 backend/                     # FastAPI Backend
│   ├── 📄 main.py                  # Main FastAPI application
│   ├── 📄 stockfish_engine.py      # Stockfish wrapper class
│   ├── 📄 game_manager.py          # Game state management
│   ├── 📄 requirements.txt         # Python dependencies
│   ├── 📄 test_api.py             # API testing script
│   └── 📂 venv/                    # Virtual environment (created on setup)
│
└── 📂 frontend/                    # React Frontend
    ├── 📄 package.json             # Node dependencies
    ├── 📄 .env                     # Environment variables
    │
    ├── 📂 public/
    │   └── 📄 index.html           # HTML template
    │
    ├── 📂 src/
    │   ├── 📄 index.js             # React entry point
    │   ├── 📄 index.css            # Global styles
    │   ├── 📄 App.js               # Main App component
    │   ├── 📄 App.css              # App styles
    │   │
    │   ├── 📂 components/
    │   │   ├── 📄 ChessBoard.jsx   # Main chess component
    │   │   └── 📄 ChessBoard.css   # Chess component styles
    │   │
    │   └── 📂 api/
    │       └── 📄 client.js        # Backend API client
    │
    ├── 📂 build/                   # Production build (created by npm build)
    └── 📂 node_modules/            # Node packages (created by npm install)
```

---

## 📋 File Descriptions

### Root Directory

| File | Purpose |
|------|---------|
| `README.md` | Complete setup and usage documentation |
| `QUICKREF.md` | Quick reference for common commands |
| `.gitignore` | Files to exclude from version control |
| `start.ps1` | PowerShell script for easy setup/launch |
| `start.bat` | Batch file for easy setup/launch |

### Backend Files

| File | Purpose | Lines | Key Functions |
|------|---------|-------|---------------|
| `main.py` | FastAPI app with all endpoints | ~300 | `/start_game`, `/player_move`, `/state` |
| `stockfish_engine.py` | Stockfish integration | ~150 | `get_best_move()`, skill level config |
| `game_manager.py` | Game state management | ~200 | `create_game()`, `apply_move()` |
| `requirements.txt` | Python dependencies | ~5 | fastapi, uvicorn, python-chess |
| `test_api.py` | API testing suite | ~250 | Tests all endpoints |

### Frontend Files

| File | Purpose | Lines | Key Features |
|------|---------|-------|--------------|
| `App.js` | Root component | ~10 | Renders ChessBoard |
| `ChessBoard.jsx` | Main game UI | ~300 | Board, controls, move handling |
| `ChessBoard.css` | Component styling | ~400 | Responsive design, themes |
| `client.js` | API communication | ~100 | HTTP calls to backend |
| `package.json` | Dependencies | ~30 | react, chess.js, react-chessboard |

---

## 🔄 Data Flow

```
User Action (Frontend)
    ↓
Chess.js validates move locally
    ↓
API Client sends move to backend
    ↓
FastAPI validates move (python-chess)
    ↓
Game Manager updates state
    ↓
Stockfish Engine calculates response
    ↓
Backend returns new position + bot move
    ↓
Frontend updates board
    ↓
User sees result
```

---

## 🎯 Key Components

### Backend Architecture

```
FastAPI App (main.py)
    ├── Game Manager (in-memory dict)
    │   └── Game State (FEN, history, status)
    │
    └── Stockfish Engine (singleton)
        └── UCI communication
```

### Frontend Architecture

```
App.js
    └── ChessBoard.jsx
        ├── react-chessboard (visual board)
        ├── chess.js (move validation)
        └── API Client (backend comm)
```

---

## 📊 Technology Stack Summary

### Backend
- **Framework**: FastAPI (async Python web framework)
- **Chess Engine**: Stockfish (world's strongest chess engine)
- **Chess Library**: python-chess (move validation, FEN handling)
- **Server**: Uvicorn (ASGI server)

### Frontend
- **Framework**: React 18
- **Board Component**: react-chessboard
- **Chess Logic**: chess.js
- **HTTP Client**: Axios
- **Build Tool**: Create React App

### Communication
- **Protocol**: HTTP REST API
- **Format**: JSON
- **CORS**: Enabled for local development

---

## 🔢 File Statistics

### Backend
- **Total Python files**: 4
- **Total lines of code**: ~900
- **API endpoints**: 6
- **Data models**: 4

### Frontend
- **Total JS/JSX files**: 5
- **Total CSS files**: 3
- **Total lines of code**: ~800
- **Components**: 1 main component

### Documentation
- **README**: ~500 lines
- **Quick Reference**: ~200 lines
- **Code comments**: Throughout

---

## 🚀 Startup Sequence

### First Time Setup
1. Run `start.ps1` or `start.bat`
2. Choose option 1 (Install dependencies)
3. Wait for installation to complete
4. Run script again, choose option 4 (Start both)

### Regular Usage
1. Run `start.ps1` or `start.bat`
2. Choose option 4 (Start both)
3. Backend opens at :8000
4. Frontend opens at :3000
5. Play chess! 🎉

---

## 💾 State Management

### Backend (In-Memory)
```python
games = {
    "game-id-1": GameState(...),
    "game-id-2": GameState(...),
}
```

### Frontend (React State)
```javascript
const [game, setGame] = useState(new Chess());
const [gameId, setGameId] = useState(null);
const [gameStatus, setGameStatus] = useState('setup');
```

---

## 🔐 Configuration

### Backend Environment Variables
- `STOCKFISH_PATH`: Path to Stockfish executable

### Frontend Environment Variables
- `REACT_APP_API_URL`: Backend API URL (default: http://localhost:8000)

---

## 📈 Future Extensibility

### Easy to Add
- ✅ Database persistence (replace in-memory dict)
- ✅ User authentication (add middleware)
- ✅ Move time limits
- ✅ Game analysis features
- ✅ Multiple board themes
- ✅ Sound effects

### Moderate Effort
- 🔶 Opening book integration
- 🔶 Bot personality customization
- 🔶 Multiplayer support
- 🔶 Tournament mode

### Advanced Features
- 🔴 Real-time spectating
- 🔴 Machine learning integration
- 🔴 Mobile app version
- 🔴 Live streaming integration

---

This overview should help you understand the complete project structure! 🎯
