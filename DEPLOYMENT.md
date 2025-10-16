# Deployment Guide for Render.com

## Quick Start

### Step 1: Prepare Your Repository

1. Initialize git repository (if not already done):
```bash
cd safepay-deploy
git init
git add .
git commit -m "Initial commit: SafePay secure payment system"
```

2. Create a new repository on GitHub

3. Push to GitHub:
```bash
git remote add origin <your-github-repo-url>
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Render.com

#### Option A: Using Blueprint (Automatic)

1. Go to https://dashboard.render.com/
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub account (if not connected)
4. Select your `safepay-deploy` repository
5. Click **"Apply"**
6. Render will automatically:
   - Read the `render.yaml` configuration
   - Run `build.sh` to install dependencies and initialize the database
   - Start the application with Gunicorn
   - Provide you with a live URL

#### Option B: Manual Web Service Setup

1. Go to https://dashboard.render.com/
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `safepay` (or your preferred name)
   - **Environment**: `Python 3`
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn app:app`
5. Click **"Create Web Service"**

### Step 3: Make build.sh Executable (if needed)

If you encounter permission errors, run locally:
```bash
chmod +x build.sh
git add build.sh
git commit -m "Make build.sh executable"
git push
```

### Step 4: Access Your Application

Once deployed, Render will provide a URL like:
```
https://safepay-xxxx.onrender.com
```

## Important Production Considerations

### 1. Secret Key
Update the secret key in `app.py` for production:
```python
import os
app.secret_key = os.environ.get('SECRET_KEY', 'fallback-secret-key')
```

Then add `SECRET_KEY` as an environment variable in Render dashboard.

### 2. Database Persistence
SQLite database will reset on each deployment. For production:
- Use Render's PostgreSQL database
- Or use persistent disk storage (available on paid plans)

### 3. Environment Variables
Add these in Render dashboard under "Environment":
- `SECRET_KEY`: Your secure secret key
- `PYTHON_VERSION`: `3.11.0` (or your preferred version)

### 4. HTTPS
Render provides free SSL certificates automatically.

## Troubleshooting

### Build Fails
- Check that `requirements.txt` has correct package versions
- Ensure `build.sh` has execute permissions
- Check build logs in Render dashboard

### Application Won't Start
- Verify `gunicorn` is in `requirements.txt`
- Check that `app.py` has `app = Flask(__name__)`
- Review application logs in Render dashboard

### Database Errors
- Ensure `db.py` runs successfully during build
- Check that `database.db` is created
- Verify SQLite is available (it's included in Python)

## Monitoring

- **Logs**: Available in Render dashboard under "Logs" tab
- **Metrics**: View CPU, memory usage in "Metrics" tab
- **Health Checks**: Render automatically monitors your service

## Updating Your Application

1. Make changes locally
2. Commit and push to GitHub:
```bash
git add .
git commit -m "Your update message"
git push
```
3. Render will automatically detect changes and redeploy

## Free Tier Limitations

Render's free tier includes:
- 750 hours/month of runtime
- Services spin down after 15 minutes of inactivity
- First request after spin-down may take 30-60 seconds
- 512 MB RAM

For production use, consider upgrading to a paid plan.

## Support

- Render Documentation: https://render.com/docs
- Render Community: https://community.render.com/
