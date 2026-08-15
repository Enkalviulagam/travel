# Travel Planner - Deployment & Testing Guide

## ✅ Current Status
- **Backend**: ✓ FastAPI server running on port 8000
- **Frontend**: ✓ React UI with red theme deployed to Netlify
- **Azure Integration**: ✓ Connected to Azure OpenAI API

## 📋 Tests Completed

### Unit Tests (TestClient)
- ✓ Home page loads HTML (200 OK)
- ✓ Chat endpoint returns valid JSON
- ✓ Multi-turn conversation support
- ✓ Error handling for missing messages
- ✓ Azure configuration loaded correctly

### HTTP API Tests
- ✓ GET / returns HTML UI (200 OK)
- ✓ POST /chat returns valid JSON responses
- ✓ Multiple conversation types tested (destination, budget)
- ✓ Proper Content-Type headers

## 🚀 Local Setup (Your Machine)

### Prerequisites
- Python 3.13+
- Virtual environment activated: `.\.venv\Scripts\activate`

### Running Locally
```powershell
cd C:\Users\rruba\Travel
.\.venv\Scripts\python.exe -m uvicorn app:app --host 0.0.0.0 --port 8000
```

Then visit: http://127.0.0.1:8000/

## 🌍 Cloud Deployment (Recommended: Render)

### Step 1: Prepare Backend for Deployment
The repository includes:
- `render.yaml` - Deployment configuration for Render.com
- `Dockerfile` - Docker container configuration
- `requirements.txt` - Python dependencies

### Step 2: Deploy to Render
1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repo: `Enkalviulagam/travel`
4. Configure:
   - **Name**: travel-planner-api
   - **Runtime**: Python 3.13
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port 8000`
5. Add Environment Variables:
   - `AZURE_ENDPOINT`: Your Azure OpenAI endpoint
   - `AZURE_DEPLOYMENT`: Your deployment name (e.g., gpt-4.1-mini)
   - `AZURE_API_KEY`: Your Azure API key
6. Click "Create Web Service"
7. Wait for deployment (2-3 minutes)
8. Copy your Render URL (e.g., `https://travel-planner-api.onrender.com`)

### Step 3: Update Frontend with Backend URL
Update `index.html` line 275:
```javascript
const apiBaseUrl = window.__API_URL__ || 'https://YOUR-RENDER-URL.onrender.com';
```

### Step 4: Redeploy Frontend
1. Commit changes: `git add . && git commit -m "Update backend URL" && git push`
2. Netlify auto-redeploys from GitHub
3. Visit https://edttravelhelper.netlify.app/

## 🧪 Testing the Deployment

### Local Testing
```bash
# Test from browser
http://127.0.0.1:8000/

# Try these prompts:
- "Plan a trip to Paris"
- "What's the best time to visit Japan?"
- "Budget $2000 for 2 weeks in Southeast Asia"
```

### Production Testing
Once deployed:
1. Visit the Netlify URL
2. Send test messages
3. Verify responses are returned correctly
4. Test multi-turn conversations

## 📁 Project Structure

```
travel/
├── app.py                 # FastAPI backend
├── index.html            # React UI
├── requirements.txt      # Python dependencies
├── .env                  # Local Azure credentials (gitignored)
├── .env.example          # Template for .env
├── .gitignore            # Git exclusions
├── Dockerfile            # Container configuration
├── render.yaml           # Render.com deployment config
└── README.md             # This file
```

## 🔧 Troubleshooting

### Backend won't start
- Check Python 3.13 installed: `python --version`
- Reinstall dependencies: `pip install -r requirements.txt`
- Ensure .venv is activated

### Frontend shows "server unable to answer"
- Verify backend is running on correct port
- Check API URL in index.html is correct
- Test backend directly: `curl http://localhost:8000/chat`

### Azure API errors
- Verify credentials in .env file
- Test endpoint and deployment name
- Check API key hasn't expired

## 🎨 UI Features

- **Red Theme**: Dynamic gradient header (#c0392b → #e74c3c)
- **Real-time Chat**: WebSocket-style message updates
- **Mobile Responsive**: Works on all screen sizes
- **Loading Indicators**: Animated dots while waiting for response
- **Error Handling**: User-friendly error messages

## 📚 API Reference

### GET /
Returns the HTML UI

### POST /chat
Request:
```json
{
  "messages": [
    {"role": "user", "content": "Your question here"},
    {"role": "assistant", "content": "Previous response"}
  ]
}
```

Response:
```json
{
  "reply": "AI-generated response..."
}
```

## 🔐 Security Notes

- `.env` file is gitignored (credentials not in repo)
- Azure API key is never sent to frontend
- All API calls go through FastAPI backend
- No sensitive data stored in localStorage

## ✨ Next Steps

1. Deploy backend to Render (free tier)
2. Update frontend with production backend URL
3. Run full end-to-end tests
4. Share public links!

---

**Repository**: https://github.com/Enkalviulagam/travel
**Frontend**: https://edttravelhelper.netlify.app/
