# Deployment Guide - Render + Vercel

## Backend Deployment (Render)

### Step 1: Deploy to Render

1. Go to https://render.com and sign in with GitHub
2. Click "New +" → "Web Service"
3. Connect your GitHub repository: `RonakMehtaa/PlayChess`
4. Configure:
   - **Name:** `chess-backend`
   - **Region:** Oregon (US West)
   - **Branch:** `main`
   - **Root Directory:** `backend`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python main.py`

5. Add Environment Variables:
   - Click "Advanced" → "Add Environment Variable"
   - Key: `STOCKFISH_PATH`
   - Value: `/usr/games/stockfish`

6. Add Stockfish Installation:
   - In "Build Command", add before pip:
   ```
   apt-get update && apt-get install -y stockfish && pip install -r requirements.txt
   ```

7. Click "Create Web Service"

8. Wait for deployment (5-10 minutes)

9. **Copy your backend URL** (e.g., `https://chess-backend-xxxx.onrender.com`)

### Alternative: Use render.yaml (Automatic)

1. Go to https://render.com
2. Click "New +" → "Blueprint"
3. Select your repository
4. Render will automatically detect `render.yaml` and configure everything
5. Click "Apply"

---

## Frontend Deployment (Vercel)

### Step 1: Update Frontend API URL

Before deploying, you need to tell the frontend where the backend is.

1. Create a production environment file in `frontend/`:

```bash
# frontend/.env.production
REACT_APP_API_URL=https://your-backend-url.onrender.com
```

Replace `your-backend-url.onrender.com` with your actual Render backend URL.

### Step 2: Deploy to Vercel

#### Option A: Using Vercel Dashboard (Easiest)

1. Go to https://vercel.com and sign in with GitHub
2. Click "Add New..." → "Project"
3. Import your repository: `RonakMehtaa/PlayChess`
4. Configure:
   - **Framework Preset:** Create React App
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `build`
   
5. Add Environment Variable:
   - Click "Environment Variables"
   - Key: `REACT_APP_API_URL`
   - Value: `https://your-backend-url.onrender.com` (from Render)
   - Apply to: Production, Preview, Development

6. Click "Deploy"

7. Wait 2-3 minutes for deployment

8. Visit your frontend URL (e.g., `https://play-chess-xxxx.vercel.app`)

#### Option B: Using Vercel CLI

```powershell
# Install Vercel CLI
npm install -g vercel

# Navigate to your project
cd C:\Users\rme\PlayChess

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

When prompted:
- Set up and deploy? **Y**
- Which scope? Choose your account
- Link to existing project? **N**
- Project name? `chess-web-app`
- In which directory is your code? `./frontend`
- Auto-detect settings? **Y**
- Override settings? **Y** (to add environment variable)

Then add environment variable:
```powershell
vercel env add REACT_APP_API_URL production
# Enter your Render backend URL when prompted
```

---

## Testing Your Deployment

1. **Test Backend:**
   - Visit: `https://your-backend.onrender.com`
   - You should see: `{"message": "Chess Web App API", "status": "running", ...}`

2. **Test Frontend:**
   - Visit: `https://your-app.vercel.app`
   - Try starting a game and making moves

---

## Important Notes

### Render Free Tier Limitations:
- ⚠️ **Spins down after 15 minutes of inactivity**
- First request after sleep takes 30-60 seconds to wake up
- 750 hours/month free (enough for hobby projects)

### Solutions:
1. **Add a health check ping** (optional):
   - Use UptimeRobot or similar to ping your backend every 14 minutes
   - Keeps it awake during active hours

2. **User Experience:**
   - Show a "Waking up server..." message on first load
   - The frontend will automatically retry

### Vercel Free Tier:
- ✅ Unlimited bandwidth
- ✅ Automatic HTTPS
- ✅ Global CDN
- ✅ Instant deployments

---

## Troubleshooting

### Backend won't start on Render:
- Check Render logs for errors
- Verify Stockfish installed: Add to build command:
  ```
  apt-get update && apt-get install -y stockfish && pip install -r requirements.txt
  ```

### Frontend can't connect to backend:
- Check `REACT_APP_API_URL` environment variable in Vercel
- Verify backend URL is correct (include `https://`)
- Check CORS settings in `backend/main.py`

### Moves not working:
- Check Render logs during gameplay
- Verify Stockfish path: `/usr/games/stockfish`

---

## Updating Your Deployment

Both Render and Vercel auto-deploy on push to `main` branch:

```powershell
# Make changes
git add .
git commit -m "Your update message"
git push origin main
```

- Render will rebuild backend (3-5 minutes)
- Vercel will rebuild frontend (1-2 minutes)

---

## Cost Estimate

- **Render Backend:** FREE (with limitations)
- **Vercel Frontend:** FREE
- **Total:** $0/month 🎉

For production without sleep limitations:
- Render Pro: $7/month (no sleep, better performance)

---

## Next Steps

1. ✅ Deploy backend to Render
2. ✅ Copy backend URL
3. ✅ Create `frontend/.env.production` with backend URL
4. ✅ Deploy frontend to Vercel
5. ✅ Test the application
6. ✅ Share your live app!

Your app will be live at:
- Backend: `https://chess-backend-xxxx.onrender.com`
- Frontend: `https://chess-web-app-xxxx.vercel.app`
