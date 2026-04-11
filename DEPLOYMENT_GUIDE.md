# Deployment Guide: Heart Disease Risk Intelligence

This project has two components:

- **Backend**: FastAPI (Python)
- **Frontend**: React with Vite (JavaScript)

---

## Quick Overview

You have **3 main deployment options**:

1. **Docker** (Recommended - Works everywhere)
2. **Cloud Platform** (Heroku, Railway, Render, Fly.io, AWS, Google Cloud)
3. **Traditional Server** (VPS, Dedicated Server)

---

## Option 1: Docker Deployment (Recommended)

Docker packages your entire app with all dependencies, making deployment consistent across environments.

### Step 1: Create Dockerfile (Backend)

Create `Dockerfile` in project root:

```dockerfile
# Build stage
FROM node:18 as build-frontend
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend .
RUN npm run build

# Runtime stage
FROM python:3.11-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy backend
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY models ./models
COPY config ./config
COPY data ./data
COPY reports ./reports

# Copy frontend build
COPY --from=build-frontend /app/frontend/dist ./frontend/dist

# Expose port
EXPOSE 8000

# Run
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Step 2: Create .dockerignore

```
.git
.gitignore
.venv
venv
node_modules
__pycache__
.pytest_cache
.mypy_cache
.DS_Store
*.pyc
.env.local
frontend/node_modules
frontend/dist
```

### Step 3: Build & Run Locally

```bash
# Build image
docker build -t heart-risk-app .

# Run container
docker run -p 8000:8000 heart-risk-app
```

Visit: `http://localhost:8000`

---

## Option 2: Deploy to Render (Easiest Free Option)

### Prerequisites

- GitHub account with repo pushed
- Render account (free tier available)

### Steps

1. **Push to GitHub**

   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/mini_project.git
   git push -u origin main
   ```

2. **Create Render.yaml** in project root:

   ```yaml
   services:
     - type: web
       name: heart-risk-api
       env: python
       plan: free
       buildCommand: "pip install -r requirements.txt && cd frontend && npm install && npm run build"
       startCommand: "uvicorn src.api.main:app --host 0.0.0.0 --port $PORT"
       envVars:
         - key: PYTHON_VERSION
           value: 3.11
   ```

3. **On Render Dashboard**
   - Click "New Web Service"
   - Connect your GitHub repo
   - Select the repo and main branch
   - Build command: `pip install -r requirements.txt && cd frontend && npm install && npm run build`
   - Start command: `uvicorn src.api.main:app --host 0.0.0.0 --port $PORT`
   - Deploy

**Cost**: Free tier available (limited resources)

---

## Option 3: Deploy to Heroku

### Prerequisites

- Heroku account
- Heroku CLI installed

### Steps

1. **Create Procfile** in project root:

   ```
   release: ./release.sh
   web: gunicorn src.api.main:app
   ```

2. **Create release.sh**:

   ```bash
   #!/bin/bash
   cd frontend
   npm install
   npm run build
   cd ..
   ```

3. **Make it executable**:

   ```bash
   chmod +x release.sh
   ```

4. **Create runtime.txt**:

   ```
   python-3.11.0
   ```

5. **Update requirements.txt** - Add gunicorn:

   ```bash
   pip freeze > requirements.txt
   echo "gunicorn==21.2.0" >> requirements.txt
   ```

6. **Deploy**:
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   ```

**Note**: Heroku free tier is discontinued. Use Render instead.

---

## Option 4: AWS Deployment

### Using AWS Elastic Beanstalk (Simplest)

1. **Create .ebextensions/python.config**:

   ```yaml
   option_settings:
     aws:elasticbeanstalk:container:python:
       WSGIPath: src.api.main:app
   ```

2. **Install AWS CLI and EB CLI**:

   ```bash
   pip install awsebcli
   ```

3. **Initialize and Deploy**:
   ```bash
   eb init -p python-3.11 heart-risk-app
   eb create heart-risk-env
   eb deploy
   ```

**Cost**: AWS free tier for 12 months

---

## Option 5: Google Cloud Run (Recommended for Free)

### Steps

1. **Install Google Cloud CLI**

2. **Authenticate**:

   ```bash
   gcloud auth login
   ```

3. **Build and deploy**:
   ```bash
   gcloud run deploy heart-risk --source . --platform managed --region us-central1 --allow-unauthenticated
   ```

**Cost**: Free tier: 2M requests/month

---

## Option 6: Self-Hosted VPS (DigitalOcean, Linode, etc.)

### On Your VPS:

1. **Install dependencies**:

   ```bash
   sudo apt update
   sudo apt install python3.11 python3-pip nodejs npm git
   ```

2. **Clone repo**:

   ```bash
   git clone https://github.com/YOUR_USERNAME/mini_project.git
   cd mini_project
   ```

3. **Setup backend**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Build frontend**:

   ```bash
   cd frontend
   npm install
   npm run build
   cd ..
   ```

5. **Create systemd service** (`/etc/systemd/system/heart-risk.service`):

   ```ini
   [Unit]
   Description=Heart Risk API
   After=network.target

   [Service]
   User=www-data
   WorkingDirectory=/var/www/mini_project
   Environment="PATH=/var/www/mini_project/venv/bin"
   ExecStart=/var/www/mini_project/venv/bin/uvicorn src.api.main:app --host 0.0.0.0 --port 8000
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

6. **Enable service**:

   ```bash
   sudo systemctl enable heart-risk
   sudo systemctl start heart-risk
   ```

7. **Setup Nginx reverse proxy**:

   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

**Cost**: $5-20/month depending on provider

---

## Production Checklist

Before deploying to production:

- [ ] Set `VITE_API_BASE_URL` environment variable to your backend URL
- [ ] Update CORS origins in `src/api/main.py` (don't use `["*"]`)
- [ ] Enable HTTPS/SSL (Let's Encrypt is free)
- [ ] Set up database backups if using persistent storage
- [ ] Configure error logging (Sentry, LogRocket)
- [ ] Add rate limiting to API
- [ ] Test all three pages (Dashboard, Reports, Risk Factors)
- [ ] Verify model files are included in deployment
- [ ] Test predictions work end-to-end
- [ ] Monitor performance and errors

---

## Environment Variables Template

Create `.env.production`:

```
VITE_API_BASE_URL=https://your-backend-domain.com
API_CORS_ORIGINS=https://your-frontend-domain.com
ENVIRONMENT=production
```

---

## Recommended Deployment Path

1. **Development**: Local testing
2. **Staging**: Deploy to free tier (Render/Google Cloud Run)
3. **Production**:
   - Docker + VPS: Full control, moderate cost ($10-50/month)
   - Google Cloud Run: Managed, pay-per-use
   - AWS: Feature-rich but higher learning curve

---

## Quick Start: Deploy to Render (Fastest)

1. Push code to GitHub
2. Go to render.com
3. Create new "Web Service"
4. Connect GitHub repo
5. Use these settings:
   - **Build Command**: `pip install -r requirements.txt && cd frontend && npm install && npm run build`
   - **Start Command**: `gunicorn src.api.main:app` (or install gunicorn first)
6. Click Deploy

Your app will be live in 5-10 minutes!

---

## Troubleshooting

| Issue               | Solution                                            |
| ------------------- | --------------------------------------------------- |
| Port conflicts      | Change port in Uvicorn or use different port number |
| CORS errors         | Update allow_origins in src/api/main.py             |
| 404 on React routes | Ensure frontend is built and served correctly       |
| Model not found     | Verify models/ directory is deployed                |
| Memory issues       | Reduce model size or use smaller instances          |

---

## Questions?

For more details on any deployment option, ask specifically and I can provide detailed setup steps!
