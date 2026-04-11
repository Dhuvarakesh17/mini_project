# Deploy to Vercel

Vercel is optimized for frontend hosting and serverless functions. For your full-stack app:

- **Frontend (React)**: Deploy to Vercel ✅ (easy)
- **Backend (FastAPI)**: Deploy elsewhere (Render, Railway, Google Cloud Run)

---

## Option 1: Split Deployment (Recommended)

### Frontend on Vercel (5 min)

### Backend on Render (5 min)

### Total Time: 10 minutes

---

## Step 1: Deploy Frontend to Vercel

### Prerequisites

- GitHub account (code pushed to repo)
- Vercel account (free signup at vercel.com)

### Deploy

1. **Go to vercel.com**
   - Sign up with GitHub
   - Click "Import Project"
   - Select your `mini_project` repo
   - Click "Import"

2. **Configure Build Settings**
   - **Framework**: `Vite`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

3. **Add Environment Variable**
   - Click "Environment Variables"
   - Add new variable:
     - **Name**: `VITE_API_BASE_URL`
     - **Value**: `https://your-backend-url.com` (we'll set this after deploying backend)

4. **Deploy**
   - Click "Deploy"
   - Wait 2-3 minutes
   - You'll get a URL: `https://your-project-name.vercel.app`

**Your frontend is live!** 🎉

---

## Step 2: Deploy Backend to Render

### On Render.com

1. Go to render.com
2. Create new Web Service
3. Connect GitHub repo
4. Settings:
   - **Build Command**: `pip install -r requirements.txt && cd frontend && npm install && npm run build`
   - **Start Command**: `uvicorn src.api.main:app --host 0.0.0.0 --port $PORT`
5. Deploy

Takes 5-10 minutes. You'll get URL: `https://heart-risk-api-xxxx.onrender.com`

---

## Step 3: Connect Frontend to Backend

### Update Environment Variable

1. Go back to Vercel project settings
2. Update `VITE_API_BASE_URL` environment variable:
   - Change to your Render backend URL
   - Example: `https://heart-risk-api-xxxx.onrender.com`

3. Redeploy frontend:
   - Go to Deployments tab
   - Click the latest deployment
   - Click "Redeploy"

**Done!** 🚀

---

## Verification Checklist

- [ ] Frontend loads at vercel.app URL
- [ ] Navigate to all 3 pages
- [ ] Try making a prediction
- [ ] Reports load correctly
- [ ] No "Connection refused" errors in console

If frontend shows blank or errors, check browser console (F12) for API URL issues.

---

## Cost Comparison

| Component | Platform | Cost     | Notes                          |
| --------- | -------- | -------- | ------------------------------ |
| Frontend  | Vercel   | Free     | Up to 100 GB bandwidth/month   |
| Backend   | Render   | Free     | May spin down after inactivity |
| Storage   | Included | Included | Models take ~500MB             |
| **Total** | **Free** | **$0**   | Suitable for hobby/testing     |

---

## If You Want Vercel for Backend Too

Vercel supports Python via serverless functions, but it's complex. Better options:

| Service              | Python            | Cost      | Best For            |
| -------------------- | ----------------- | --------- | ------------------- |
| **Render**           | ✅ Full app       | Free/$7   | Easiest for FastAPI |
| **Railway**          | ✅ Full app       | Free/$5   | Simple deployment   |
| **Google Cloud Run** | ✅ Full app       | Free      | Scalable            |
| **AWS Lambda**       | ✅ Functions only | Free tier | Complex setup       |
| **Azure**            | ✅ Functions      | Free tier | Enterprise          |

**Recommendation**: Keep frontend on Vercel, backend on Render.

---

## All-in-One Alternative: Keep on Render

If you prefer everything in one place:

```bash
# Single platform (Render)
- Deploy: render.com
- Runtime: Docker
- Both frontend + backend included
- Cost: Free or $7/month
- URL: single domain
```

Then skip Vercel entirely. This is simpler!

---

## Production Setup (Best Practice)

```
Frontend: Vercel (optimized CDN, edge functions)
         ↓ (API calls)
Backend: Render/Railway (Python, models, ML)
```

This separates concerns and gives you:

- Fast frontend delivery on Vercel's global CDN
- Reliable backend on a platform built for Python apps
- Easy to scale each independently

---

## Troubleshooting Vercel Deployment

| Issue                      | Fix                                          |
| -------------------------- | -------------------------------------------- |
| Build fails                | Check build command matches your setup       |
| Blank page                 | Check VITE_API_BASE_URL environment variable |
| 404 errors when navigating | Ensure build outputs to `dist` folder        |
| CORS errors                | Update backend CORS: allow Vercel domain     |

---

## Next Steps

1. **If going Vercel + Render**:
   - Deploy frontend to Vercel (now)
   - Deploy backend to Render (5 min later)
   - Update API URL

2. **If keeping everything on Render**:
   - You already have the setup! Just deploy as is.

**Which approach do you prefer?** I can give detailed steps for either.
