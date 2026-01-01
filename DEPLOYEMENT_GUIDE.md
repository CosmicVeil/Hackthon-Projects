# Deployment Guide

## Why Netlify Won't Work

Netlify is designed for **static websites** and **serverless functions**. Your Flask application requires a Python runtime environment, which Netlify doesn't provide. This is why you're getting a 404 error - Netlify doesn't know how to run your Flask app.

## Recommended Solution: Deploy to Render (Free & Easy)

Render is perfect for Flask applications and offers a free tier. Here's how to deploy:

### Step 1: Update Your Code
- ✅ `requirements.txt` - Already created
- ✅ `Procfile` - Already created
- ✅ Updated `app.py` to use environment variables

### Step 2: Push to GitHub
Make sure your code (including the new files) is pushed to GitHub.

### Step 3: Deploy on Render

1. Go to [render.com](https://render.com) and sign up/login
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure your service:
   - **Name**: Choose a name (e.g., "ms-question-generator")
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn MathWebsite.app:app`
   - **Root Directory**: Leave empty (or set to `.`)

5. **Add Environment Variable**:
   - Key: `OPENAI_API_KEY`
   - Value: Your actual OpenAI API key (NOT "IN DISCORD")

6. Click "Create Web Service"
7. Wait for deployment (takes 2-3 minutes)

### Step 4: Your Site is Live! 🎉

Render will give you a URL like: `https://your-app-name.onrender.com`

---

## Alternative: Deploy to Railway (Also Free)

Railway is another great option:

1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub"
3. Select your repository
4. Railway will auto-detect it's a Python app
5. Add environment variable: `OPENAI_API_KEY` = your API key
6. Deploy!

---

## If You Really Want Netlify

If you absolutely must use Netlify, you'd need to:
1. Convert your Flask routes to Netlify Serverless Functions
2. This requires significant code restructuring
3. Not recommended for Flask apps

**Bottom line**: Use Render or Railway - they're made for Flask apps and will work immediately!

