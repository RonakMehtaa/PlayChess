# Railway Deployment Checklist

## Prerequisites
- [x] GitHub repository created: https://github.com/RonakMehtaa/PlayChess
- [x] Code pushed to GitHub
- [x] Railway configuration files created

## Backend Deployment (Railway)

### Step 1: Sign Up & Deploy
- [ ] Go to https://railway.app
- [ ] Click "Login" → Sign in with GitHub
- [ ] Click "New Project"
- [ ] Select "Deploy from GitHub repo"
- [ ] Choose repository: `RonakMehtaa/PlayChess`
- [ ] Railway auto-detects `nixpacks.toml`
- [ ] Wait 3-5 minutes for deployment

### Step 2: Get Backend URL
- [ ] Click on your deployment
- [ ] Go to "Settings" tab
- [ ] Click "Generate Domain" under "Domains"
- [ ] Copy your Railway URL: `https://playchess-production-XXXX.up.railway.app`
- [ ] Test URL in browser - should see API message

### Step 3: Verify Stockfish
- [ ] In Railway dashboard, click "Deployments"
- [ ] Click latest deployment → "View Logs"
- [ ] Look for: "Stockfish initialized successfully"
- [ ] Verify no errors about Stockfish not found

## Frontend Deployment (Vercel)

### Step 1: Update Production Config
- [ ] Open `frontend/.env.production` in your editor
- [ ] Replace URL with YOUR Railway URL
- [ ] Save file
- [ ] Run:
  ```powershell
  git add frontend/.env.production
  git commit -m "Update Railway API URL"
  git push origin main
  ```

### Step 2: Deploy to Vercel
- [ ] Go to https://vercel.com
- [ ] Click "Login" → Sign in with GitHub
- [ ] Click "Add New..." → "Project"
- [ ] Import `RonakMehtaa/PlayChess`
- [ ] Configure:
  - Framework: Create React App
  - Root Directory: `frontend`
  - Build Command: `npm run build`
  - Output Directory: `build`
- [ ] Add Environment Variable:
  - Key: `REACT_APP_API_URL`
  - Value: Your Railway URL (paste from Railway)
  - Apply to: All environments
- [ ] Click "Deploy"
- [ ] Wait 2-3 minutes
- [ ] Copy Vercel URL: `https://play-chess-XXXX.vercel.app`

## Testing

### Backend Test
- [ ] Visit: `https://your-railway-url.up.railway.app/`
- [ ] Should see JSON: `{"message": "Chess Web App API", "status": "running", ...}`
- [ ] Status should be "running"

### Frontend Test  
- [ ] Visit: `https://your-vercel-url.vercel.app`
- [ ] Click "New Game"
- [ ] Select color (White/Black)
- [ ] Choose difficulty (try level 5)
- [ ] Click "Start Game"
- [ ] Make a move by dragging a piece
- [ ] Verify bot responds within 1-2 seconds
- [ ] Test multiple difficulty levels
- [ ] Test both colors

### Integration Test
- [ ] Open browser DevTools (F12)
- [ ] Go to Console tab
- [ ] Start a new game
- [ ] Make a move
- [ ] Verify no CORS errors
- [ ] Verify API calls succeed (Network tab)

## Monitor Usage

### Railway Usage Check
- [ ] Go to Railway dashboard
- [ ] Click "Usage" tab
- [ ] Note current usage: $_____ / $5.00
- [ ] Set reminder to check monthly

### Performance Check
- [ ] Test game response time (should be < 2 seconds)
- [ ] Check Railway logs for errors
- [ ] Verify no crashes or restarts

## Post-Deployment

- [ ] Update README.md with live URLs:
  ```markdown
  ## 🚀 Live Demo
  - Frontend: https://your-vercel-url.vercel.app
  - Backend: https://your-railway-url.up.railway.app
  ```

- [ ] (Optional) Enable Railway notifications:
  - Go to Project Settings
  - Enable "Deploy notifications"
  - Get notified of failures

- [ ] Share your app!
  - Test on different devices
  - Share with friends
  - Post on social media

## Troubleshooting

If backend shows errors in Railway logs:
1. Check for Stockfish path issues
2. Verify Python version (3.10+)
3. Check environment variables
4. Review build logs for failed dependencies

If frontend can't connect:
1. Verify `REACT_APP_API_URL` in Vercel settings
2. Check for CORS errors in browser console
3. Ensure Railway backend URL is correct (https://)
4. Test backend URL directly in browser

If bot doesn't respond:
1. Check Railway logs during gameplay
2. Verify Stockfish initialized (check logs)
3. Test with different difficulty levels
4. Check for timeout errors

## URLs to Save

- **GitHub:** https://github.com/RonakMehtaa/PlayChess
- **Railway Backend:** ________________________________
- **Vercel Frontend:** ________________________________
- **Railway Dashboard:** https://railway.app/dashboard

## Estimated Time
- Railway setup: 5 minutes
- Railway deployment: 3-5 minutes
- Frontend config update: 2 minutes
- Vercel deployment: 2-3 minutes
- Testing: 5 minutes
- **Total: ~15-20 minutes**

## Monthly Maintenance
- [ ] Check Railway usage (stays under $5?)
- [ ] Review Railway logs for errors
- [ ] Test app functionality
- [ ] Update dependencies if needed

---

✅ Once all checkboxes are complete, your Chess app is live!

See DEPLOYMENT_RAILWAY.md for detailed instructions.
