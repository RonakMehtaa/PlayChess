# Deployment Guide - Railway + Vercel

## Backend Deployment (Railway)

### Step 1: Deploy to Railway

1. Go to https://railway.app and sign in with GitHub
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository: `RonakMehtaa/PlayChess`
4. Railway will automatically detect `nixpacks.toml` and configure everything
5. Configure settings:
   - **Root Directory:** `backend`
   - **Start Command:** `python main.py`
   - Railway will auto-install Stockfish via Nix packages

6. Add Environment Variable (if needed):
   - Go to Variables tab
   - Add: `PORT` = `8000` (Railway will override this automatically)

7. Click "Deploy"

8. Wait for deployment (3-5 minutes)

9. **Copy your backend URL** from Railway dashboard
   - Click on your deployment → Settings → Generate Domain
   - Example: `https://playchess-production-xxxx.up.railway.app`

### Alternative: Using Railway CLI

```powershell
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
cd C:\Users\rme\PlayChess
railway init

# Link to backend
railway link

# Deploy
railway up

# Get URL
railway domain
```

---

## Frontend Deployment (Vercel)

### Step 1: Update Frontend API URL

Before deploying, you need to tell the frontend where the backend is.

1. Edit `frontend/.env.production`:

```env
REACT_APP_API_URL=https://your-railway-url.up.railway.app
```

Replace with your actual Railway backend URL.

2. Commit and push:
```powershell
git add frontend/.env.production
git commit -m "Update production API URL for Railway"
git push origin main
```

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
   - Value: Your Railway backend URL
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

Then add environment variable:
```powershell
vercel env add REACT_APP_API_URL production
# Enter your Railway backend URL when prompted
```

---

## Testing Your Deployment

1. **Test Backend:**
   - Visit: `https://your-railway-url.up.railway.app`
   - You should see: `{"message": "Chess Web App API", "status": "running", ...}`

2. **Test Frontend:**
   - Visit: `https://your-app.vercel.app`
   - Try starting a game and making moves

---

## Important Notes

### Railway Free Tier:
- ✅ $5 monthly credit (usually enough for hobby projects)
- ✅ No sleep/spin-down like Render
- ✅ Always-on service
- ✅ 500MB RAM, 1GB disk
- ⚠️ Credit resets monthly
- ⚠️ After $5 credit used, service pauses until next month

### Railway Advantages:
- ✅ **No cold starts** - always responsive
- ✅ **Nix packages** - Easy Stockfish installation
- ✅ **Automatic HTTPS**
- ✅ **Built-in metrics and logs**
- ✅ **GitHub integration** - auto-deploy on push

### Vercel Free Tier:
- ✅ Unlimited bandwidth
- ✅ Automatic HTTPS
- ✅ Global CDN
- ✅ Instant deployments

---

## Monitoring Your Usage

### Railway:
1. Go to Railway dashboard
2. Click on your project
3. View "Usage" tab to see credit consumption
4. Typical usage: ~$2-3/month for low-traffic hobby project

### Vercel:
- Free tier is generous
- No bandwidth limits for hobby projects

---

## Troubleshooting

### Backend won't start on Railway:
- Check Railway logs (click on deployment → View Logs)
- Verify `nixpacks.toml` is in root directory
- Ensure Stockfish is in Nix packages list

### Frontend can't connect to backend:
- Check `REACT_APP_API_URL` environment variable in Vercel
- Verify Railway backend URL is correct (include `https://`)
- Check Railway logs for CORS errors
- Verify backend is actually running (check Railway metrics)

### Stockfish not found:
- Railway uses Nix packages - path is `/nix/store/*-stockfish-*/bin/stockfish`
- Backend auto-detects Stockfish path
- Check Railway logs for Stockfish initialization messages

### "Out of credits" error:
- Railway free tier has $5/month limit
- Check usage in Railway dashboard
- Either wait for monthly reset or upgrade to hobby plan ($5/month)

---

## Updating Your Deployment

Both Railway and Vercel auto-deploy on push to `main` branch:

```powershell
# Make changes
git add .
git commit -m "Your update message"
git push origin main
```

- Railway will rebuild backend (2-3 minutes)
- Vercel will rebuild frontend (1-2 minutes)

---

## Cost Estimate

- **Railway Backend:** FREE up to $5/month usage (typically $2-3/month for hobby project)
- **Vercel Frontend:** FREE
- **Total:** $0/month (within free credits) 🎉

If you exceed Railway free tier:
- Hobby Plan: $5/month (includes $5 usage credit)
- Pro Plan: $20/month (includes $10 usage credit)

**Most hobby projects stay within free tier!**

---

## Next Steps

1. ✅ Deploy backend to Railway
2. ✅ Copy Railway backend URL
3. ✅ Update `frontend/.env.production` with Railway URL
4. ✅ Deploy frontend to Vercel
5. ✅ Test the application
6. ✅ Share your live app!

Your app will be live at:
- Backend: `https://playchess-production-xxxx.up.railway.app`
- Frontend: `https://chess-web-app-xxxx.vercel.app`

---

## Why Railway + Vercel?

- ✅ **No cold starts** (unlike Render free tier)
- ✅ **Easy Stockfish setup** (Nix packages)
- ✅ **Auto-deploy from GitHub**
- ✅ **Production-ready** for hobby projects
- ✅ **Free tier sufficient** for low-medium traffic
- ✅ **Great developer experience**
