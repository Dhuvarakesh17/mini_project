# 🚀 QUICK DEPLOYMENT GUIDE

## Fastest Way to Deploy (5 minutes): Render

### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Heart Risk Intelligence App"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/mini_project.git
git push -u origin main
```

### Step 2: Go to Render.com

- Visit https://render.com
- Click "Sign up" → "Continue with GitHub"
- Authorize Render

### Step 3: Create Web Service

- Click "New +" → "Web Service"
- Select your GitHub repo
- Choose the `main` branch
- Fill in settings:
  - **Name**: `heart-risk-app`
  - **Region**: Choose your region
  - **Branch**: `main`
  - **Runtime**: `Docker`
  - **Plan**: `Free`
- Click "Create Web Service"

### Step 4: Wait for Deployment

- Render will automatically build and deploy
- Takes 5-10 minutes
- You'll get a URL when ready: `https://heart-risk-app-xxxx.onrender.com`

**That's it! Your app is live!** 🎉

---

## Alternative: Docker on Local Machine (1 minute)

```bash
# Build
docker build -t heart-risk-app .

# Run
docker run -p 8000:8000 heart-risk-app

# Visit
# Frontend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

---

## If You Want to Use Google Cloud Run (Free)

### Prerequisites

- Google Cloud account
- gcloud CLI installed

### Deploy in 2 commands

```bash
gcloud auth login
gcloud run deploy heart-risk-app --source . --region us-central1 --allow-unauthenticated
```

---

## Production Checklist After Deployment

- [ ] Test all 3 pages (Dashboard, Reports, Risk Factors)
- [ ] Try making a prediction
- [ ] Check Reports page loads charts
- [ ] Verify Heart Risk Factors page display
- [ ] Test on mobile device
- [ ] Share URL with others

---

## Troubleshooting

| Problem                | Solution                                  |
| ---------------------- | ----------------------------------------- |
| Deploy takes too long  | It's normal! First build takes 5-10 min   |
| 504 error after deploy | Wait a bit longer, apps still starting up |
| Frontend shows blank   | Check browser console for API URL errors  |
| API returns 404        | Backend might not have started            |
| Models not found       | Add models/ to Dockerfile COPY commands   |

---

## After Deployment

### Update Frontend API URL

If your frontend can't reach backend:

1. Go to Render dashboard
2. Select your service
3. Go to "Environment"
4. Add variable: `VITE_API_BASE_URL=https://your-render-url.onrender.com`
5. Redeploy

### View Logs

- **Render**: Service Dashboard → Logs tab
- **Docker**: `docker logs <container-id>`
- **Google Cloud**: Cloud Console → Logs

### Scale Up Later

- **Render**: Upgrade from Free to Starter ($7/month)
- **Google Cloud**: Still free! (within limits)

---

## Want More Details?

Check `DEPLOYMENT_GUIDE.md` for:

- AWS deployment
- Heroku setup
- Custom VPS setup
- Production configurations

---

**Questions?** Ask and I'll help with specific deployment step!
