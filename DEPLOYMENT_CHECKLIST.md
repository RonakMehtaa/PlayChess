# Deployment Checklist

## Prerequisites
- [x] GitHub repository created: https://github.com/RonakMehtaa/PlayChess
- [x] Code pushed to GitHub
- [x] Deployment configuration files created

## Backend Deployment (Render)

### Option 1: Automatic with render.yaml (Recommended)
- [ ] Go to https://render.com and sign in with GitHub
- [ ] Click "New +" → "Blueprint"
- [ ] Select repository: `RonakMehtaa/PlayChess`
- [ ] Click "Apply" (Render will use render.yaml automatically)
- [ ] Wait 5-10 minutes for deployment
- [ ] Copy your backend URL: `https://chess-backend-XXXX.onrender.com`

### Option 2: Manual Setup
- [ ] Go to https://render.com and sign in with GitHub
- [ ] Click "New +" → "Web Service"
- [ ] Select repository: `RonakMehtaa/PlayChess`
- [ ] Configure:
  - Name: `chess-backend`
  - Root Directory: `backend`
  - Build Command: `apt-get update && apt-get install -y stockfish && pip install -r requirements.txt`
  - Start Command: `python main.py`
  - Environment Variables:
    - `STOCKFISH_PATH` = `/usr/games/stockfish`
- [ ] Click "Create Web Service"
- [ ] Wait for deployment
- [ ] Copy backend URL

## Frontend Deployment (Vercel)

### Step 1: Update .env.production
- [ ] Open `frontend/.env.production`
- [ ] Replace `https://chess-backend.onrender.com` with YOUR actual Render URL
- [ ] Commit and push:
  ```powershell
  git add frontend/.env.production
  git commit -m "Update production API URL"
  git push origin main
  ```

### Step 2: Deploy to Vercel
- [ ] Go to https://vercel.com and sign in with GitHub
- [ ] Click "Add New..." → "Project"
- [ ] Import repository: `RonakMehtaa/PlayChess`
- [ ] Configure:
  - Framework: Create React App
  - Root Directory: `frontend`
  - Build Command: `npm run build`
  - Output Directory: `build`
- [ ] Add Environment Variable:
  - Key: `REACT_APP_API_URL`
  - Value: Your Render backend URL
  - Apply to: Production, Preview, Development
- [ ] Click "Deploy"
- [ ] Wait 2-3 minutes
- [ ] Copy frontend URL: `https://play-chess-XXXX.vercel.app`

## Testing

- [ ] Visit backend health endpoint: `https://your-backend.onrender.com/`
  - Should see: `{"message": "Chess Web App API", "status": "running", ...}`
  
- [ ] Visit frontend: `https://your-app.vercel.app`
  - [ ] Start a new game
  - [ ] Make a move
  - [ ] Verify bot responds
  - [ ] Test different difficulty levels
  - [ ] Test both white and black player colors

## Post-Deployment

- [ ] Update README.md with live URLs
- [ ] Share your app!
- [ ] (Optional) Set up UptimeRobot to keep Render backend awake

## Troubleshooting

If frontend can't connect to backend:
1. Check browser console for CORS errors
2. Verify `REACT_APP_API_URL` in Vercel environment variables
3. Check Render logs for backend errors

If backend is slow to respond:
- Render free tier spins down after 15 minutes
- First request takes 30-60 seconds to wake up
- This is normal on free tier

## URLs to Save

- GitHub: https://github.com/RonakMehtaa/PlayChess
- Render Backend: ________________________________
- Vercel Frontend: ________________________________

## Estimated Time
- Backend deployment: 5-10 minutes
- Frontend deployment: 2-3 minutes
- Testing: 5 minutes
- **Total: ~15-20 minutes**

---

See DEPLOYMENT.md for detailed step-by-step instructions.
