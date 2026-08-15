# 🚀 QUICK DEPLOYMENT GUIDE - FIX THE NETLIFY SITE (5 minutes)

## Problem
The Netlify frontend at https://edttravelhelper.netlify.app/ is trying to connect to a backend that doesn't exist yet.

**Frontend URL**: https://edttravelhelper.netlify.app/ ✅ (deployed)  
**Backend URL**: https://travel-planner-api.onrender.com ❌ (NOT deployed yet)

## Solution: Deploy Backend to Render.com

### Step 1: Go to Render.com
Visit: https://render.com

### Step 2: Create Web Service
1. Click **"New +"** button (top right)
2. Select **"Web Service"**

### Step 3: Connect GitHub Repository
1. Click **"Connect account"** (GitHub)
2. Authorize Render to access your GitHub
3. Select repository: **Enkalviulagam/travel**
4. Click **"Connect"**

### Step 4: Configure Service
Fill in the following fields:

**Name**: `travel-planner-api`

**Environment**: `Python 3`

**Build Command**:
```
pip install -r requirements.txt
```

**Start Command**:
```
gunicorn -w 1 -k uvicorn.workers.UvicornWorker app:app --bind 0.0.0.0:8000
```

**Instance Type**: Free (or Starter if you want)

### Step 5: Add Environment Variables
Click **"Advanced"** → **"Add Environment Variable"**

Add these 3 variables (copy from your .env file):

1. **AZURE_ENDPOINT**
   - Value: `https://[your-resource].openai.azure.com/`

2. **AZURE_DEPLOYMENT**
   - Value: `gpt-4.1-mini`

3. **AZURE_API_KEY**
   - Value: `your-api-key-here`

### Step 6: Deploy
Click **"Create Web Service"**

⏳ **Wait 2-3 minutes** for deployment to complete

You'll see:
```
Deploying...
✓ Build succeeded
✓ Deploy succeeded
Live at: https://travel-planner-api.onrender.com
```

### Step 7: Test the Frontend
Once deployed, visit:
```
https://edttravelhelper.netlify.app/
```

Send a message like: "Plan a trip to Tokyo"

✅ **It should work!**

---

## Troubleshooting

### "Failed to fetch" error
- Wait 2-3 minutes for Render deployment to complete
- Check that all 3 Azure variables are set
- Reload the page (hard refresh: Ctrl+Shift+R)

### "Build failed" error
- Make sure `requirements.txt` is in the repository
- Check that `.env` file is in `.gitignore` (it should be)
- Azure variables must be set in Render dashboard, not in code

### "Server error" after deployment
- Check that Azure credentials are correct
- Test locally first: `python -m uvicorn app:app --reload`
- Check Render logs for error details

---

## Alternative: Deploy Locally for Testing

If you want to test locally first:

```bash
cd C:\Users\rruba\Travel
.\.venv\Scripts\activate
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

Then visit: `http://127.0.0.1:8000`

---

## Current Status

```
✅ Backend Code: Ready (tested and working)
✅ Frontend: Deployed on Netlify (waiting for backend)
❌ Backend Deployment: Not yet deployed
⏳ Next Step: Deploy to Render.com (5 minutes)
```

---

**Once Render deployment is complete, the site will work perfectly!**
