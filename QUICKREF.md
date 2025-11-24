# Quick Reference Guide

## 🚀 Quick Commands

### Backend

```powershell
# Navigate to backend
cd backend

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run server
python main.py

# Run tests
python test_api.py

# Deactivate venv
deactivate
```

### Frontend

```powershell
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start dev server
npm start

# Build for production
npm run build
```

### Using the Quick Start Script

```powershell
# From project root
.\start.ps1
```

---

## 🔧 Environment Setup

### Set Stockfish Path (Windows)

**Temporary (current session):**
```powershell
$env:STOCKFISH_PATH="C:\path\to\stockfish.exe"
```

**Permanent (system-wide):**
1. Search for "Environment Variables" in Windows
2. Add new system variable:
   - Name: `STOCKFISH_PATH`
   - Value: `C:\path\to\stockfish.exe`

---

## 🧪 Testing Endpoints

### Using PowerShell

**Health Check:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000"
```

**Start Game:**
```powershell
$body = @{
    player_color = "white"
    bot_level = 10
} | ConvertTo-Json

$result = Invoke-RestMethod -Uri "http://localhost:8000/start_game" -Method Post -Body $body -ContentType "application/json"
$gameId = $result.game_id
```

**Make Move:**
```powershell
$body = @{
    game_id = $gameId
    move = "e2e4"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/player_move" -Method Post -Body $body -ContentType "application/json"
```

**Get State:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/state/$gameId"
```

---

## 📝 Common UCI Moves

| Move | UCI | Description |
|------|-----|-------------|
| Pawn e2 to e4 | `e2e4` | King's pawn opening |
| Knight g1 to f3 | `g1f3` | Develop knight |
| Bishop f1 to c4 | `f1c4` | Italian game |
| Kingside castle | `e1g1` | King to g1 |
| Queenside castle | `e1c1` | King to c1 |
| Pawn promotion | `e7e8q` | Promote to queen |

---

## 🎨 Customization

### Change Bot Speed

Edit `backend/stockfish_engine.py`, line ~45:
```python
def get_best_move(self, board, skill_level=10, move_time=0.2):
    # Change move_time value (in seconds)
```

### Change Frontend Port

Edit `frontend/package.json`:
```json
"scripts": {
  "start": "PORT=3001 react-scripts start"
}
```

Or set environment variable:
```powershell
$env:PORT=3001; npm start
```

### Change API URL

Edit `frontend/.env`:
```
REACT_APP_API_URL=http://localhost:8000
```

---

## 🐛 Common Issues

### "Stockfish engine not available"
- Install Stockfish
- Set STOCKFISH_PATH environment variable
- Restart terminal after setting env variable

### "Module not found" (Python)
- Activate virtual environment
- Run `pip install -r requirements.txt`

### "Port already in use"
- Backend: Change port in `main.py` (last line)
- Frontend: Set PORT environment variable

### Frontend can't connect
- Verify backend is running: http://localhost:8000
- Check CORS settings in `backend/main.py`
- Verify `.env` file in frontend

### Moves not working
- Ensure it's your turn
- Use correct UCI format (e.g., `e2e4`)
- Check browser console for errors

---

## 📊 Bot Difficulty Levels

| Level | ELO Rating | Strength |
|-------|------------|----------|
| 0 | ~800 | Complete beginner |
| 5 | ~1350 | Novice player |
| 10 | ~1900 | Intermediate |
| 15 | ~2450 | Advanced club |
| 20 | ~3000+ | Master level |

---

## 🔍 Useful URLs

- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **Frontend**: http://localhost:3000
- **Stockfish**: https://stockfishchess.org

---

## 💡 Tips

1. **Start with level 5-8** for a fun game
2. **Use the evaluation** to learn - positive = white ahead
3. **Review move history** to understand mistakes
4. **Try different openings** - e4, d4, c4, Nf3
5. **Level 15+** is very strong - even strong players struggle

---

## 🎯 Example Game Flow

```powershell
# 1. Start backend
cd backend
.\venv\Scripts\Activate.ps1
python main.py

# 2. In new terminal - start frontend
cd frontend
npm start

# 3. In browser - http://localhost:3000
# - Select White
# - Set difficulty to 8
# - Click Start Game
# - Play!
```

---

## 📈 Performance

Typical response times:
- **Start game**: 50-100ms
- **Player move + bot response**: 200-500ms (depending on level)
- **Higher difficulty**: Slower responses (more thinking time)

---

## 🔐 Security Notes

**For Development:**
- CORS allows all origins (`*`)
- No authentication

**For Production:**
- Set specific CORS origins
- Add authentication
- Use HTTPS
- Rate limiting recommended
- Consider persistent storage (Redis/DB)

---

This quick reference should help you navigate the project efficiently! 🚀
