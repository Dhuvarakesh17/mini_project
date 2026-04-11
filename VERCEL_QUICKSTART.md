# ⚡ VERCEL DEPLOYMENT - QUICK START

## The Simplest Way (3 clicks)

### Frontend to Vercel

1. **Push code to GitHub**

   ```bash
   git add .
   git commit -m "Ready for Vercel"
   git push origin main
   ```

2. **Go to vercel.com**
   - Sign up → GitHub OAuth
   - "Import Project"
   - Select `mini_project`
   - Click "Import"
   - Click "Deploy"

   **Status**: DONE! ✅ Frontend is live

3. **Deploy Backend Separately**

   Since Vercel doesn't run Python well, deploy FastAPI to Render:
   - Go to render.com
   - New Web Service → Select repo
   - Build: `pip install -r requirements.txt && cd frontend && npm install && npm run build`
   - Start: `uvicorn src.api.main:app --host 0.0.0.0 --port $PORT`
   - Deploy

   **Status**: Backend is live ✅

4. **Connect Them**

   In Vercel dashboard:
   - Project Settings → Environment Variables
   - Add: `VITE_API_BASE_URL = https://your-render-url.onrender.com`
   - Redeploy

**Total Time: 10 minutes** ⏱️

---

## The URLs You'll Get

- **Frontend**: `https://your-project.vercel.app` ← Main app here
- **Backend**: `https://heart-risk-api-xxxx.onrender.com` ← API here

---

## Cost

- Vercel: **$0** (free tier)
- Render: **$0** (free tier, may sleep after 15 min inactivity)
- **Total: $0/month** 🎉

---

## After Deployment - Test It

1. Open `https://your-project.vercel.app`
2. Go to Dashboard page
3. Enter some patient data
4. Click "Predict Risk"
5. Should work! ✅

---

## If Something Breaks

**Problem**: Blank screen

- **Fix**: Check Network tab (F12 → Network)
- Look for failed requests to backend
- Update `VITE_API_BASE_URL` to correct backend URL

**Problem**: "Cannot connect to API"

- **Fix**: Backend might be sleeping
- Visit backend URL in browser, wait 30s for wakeup
- Try prediction again

**Problem**: Build fails on Vercel

- **Fix**: Check Vercel Logs
- Usually: missing `vercel.json` or wrong start command

---

## Want Full Control?

See **VERCEL_DEPLOYMENT.md** for detailed options:

- Custom domains
- Environment variables
- Production configuration
- Troubleshooting

---

## Still Want Everything on One Platform?

Use **Render** instead (simpler):

```bash
1. Go render.com
2. New Web Service → Connect repo
3. Deploy
4. Done! Single URL, both frontend + backend
```

---

## TL;DR (Copy-Paste)

1. Push to GitHub ✓
2. vercel.com → Import → Deploy ✓
3. render.com → New Service → Deploy ✓
4. Vercel settings → Add API URL ✓
5. Vercel → Redeploy ✓

**Live in 10 minutes!** 🚀
