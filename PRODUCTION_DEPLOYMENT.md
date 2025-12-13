# 🚀 Production Deployment Guide - leads.ragspro.com

## Prerequisites

1. **Domain:** leads.ragspro.com configured
2. **Hosting:** Render.com account (or similar)
3. **API Keys:**
   - GEMINI_API_KEY (for AI analysis)
   - SERPAPI_KEY (for lead scraping)
   - SECRET_KEY (for Flask sessions)

## Step 1: Environment Variables

Create `.env` file for production (DO NOT commit to Git):

```bash
# Production Environment Variables
FLASK_ENV=production
SECRET_KEY=your-super-secret-production-key-change-this
GEMINI_API_KEY=your-gemini-api-key-here
SERPAPI_KEY=your-serpapi-key-here
PORT=5002
```

## Step 2: Update render.yaml

```yaml
services:
  - type: web
    name: ragspro-leads
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn dashboard_ragspro:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
    envVars:
      - key: FLASK_ENV
        value: production
      - key: SECRET_KEY
        generateValue: true
      - key: GEMINI_API_KEY
        sync: false  # Set manually in Render dashboard
      - key: SERPAPI_KEY
        sync: false  # Set manually in Render dashboard
      - key: PORT
        value: 5002
    domains:
      - leads.ragspro.com
```

## Step 3: Update requirements.txt

Ensure all dependencies are listed:

```txt
flask==3.0.0
flask-limiter==4.1.1
gunicorn==21.2.0
google-generativeai==0.3.2
serpapi==0.1.5
openpyxl==3.1.2
reportlab==4.0.7
requests==2.31.0
```

## Step 4: Production Configuration

Update `dashboard_ragspro.py` for production:

```python
# At the end of file, change:
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5002))
    debug = os.getenv('FLASK_ENV') != 'production'
    
    print(f"""
    ╔══════════════════════════════════════════════════════════╗
    ║           RAGSPRO DASHBOARD - {'PRODUCTION' if not debug else 'DEVELOPMENT'}                 ║
    ║                                                          ║
    ║  🎯 Complete Lead Management System                      ║
    ║  💰 AI-Powered Content Generation                        ║
    ║  🚀 Real-time Lead Generation                            ║
    ╚══════════════════════════════════════════════════════════╝
    
    🚀 Dashboard running at: http://0.0.0.0:{port}
    📊 Environment: {'PRODUCTION' if not debug else 'DEVELOPMENT'}
    """)
    
    app.run(debug=debug, host='0.0.0.0', port=port)
```

## Step 5: Deploy to Render

### Option A: Via GitHub (Recommended)

1. **Push to GitHub:**
```bash
git add .
git commit -m "Production ready deployment"
git push origin main
```

2. **Connect Render to GitHub:**
   - Go to https://dashboard.render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select branch: `main`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn dashboard_ragspro:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`

3. **Set Environment Variables in Render:**
   - Go to Environment tab
   - Add:
     - `FLASK_ENV` = `production`
     - `SECRET_KEY` = (generate random string)
     - `GEMINI_API_KEY` = (your Gemini API key)
     - `SERPAPI_KEY` = (your SerpAPI key)
     - `PORT` = `5002`

4. **Configure Custom Domain:**
   - Go to Settings → Custom Domain
   - Add: `leads.ragspro.com`
   - Update DNS:
     - Type: CNAME
     - Name: leads
     - Value: your-app.onrender.com

### Option B: Via Docker

1. **Build Docker image:**
```bash
docker build -t ragspro-leads .
```

2. **Test locally:**
```bash
docker run -p 5002:5002 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=your-secret \
  -e GEMINI_API_KEY=your-key \
  -e SERPAPI_KEY=your-key \
  ragspro-leads
```

3. **Deploy to Render:**
   - Push image to Docker Hub
   - Deploy from Docker Hub on Render

## Step 6: Post-Deployment Verification

### 1. Check Health
```bash
curl https://leads.ragspro.com/
# Should return HTML (200 OK)
```

### 2. Test API Endpoints
```bash
# Test stats
curl https://leads.ragspro.com/api/stats

# Test leads
curl https://leads.ragspro.com/api/leads

# Test history
curl https://leads.ragspro.com/api/history
```

### 3. Test Lead Generation
1. Open: https://leads.ragspro.com
2. Select: Country, City, Category
3. Click: 🚀 Generate
4. Verify: Leads appear

### 4. Test AI Analyze
1. Click: 🔍 AI Analyze on any lead
2. Verify: Modal appears with analysis
3. Check: Pain points, solutions, scripts

### 5. Test Bulk Operations
1. Select: 3-5 leads
2. Click: 🤖 AI Analyze
3. Verify: Bulk analysis works

## Step 7: Monitoring

### Check Logs
```bash
# On Render dashboard
Go to Logs tab → View real-time logs
```

### Monitor Errors
Look for:
- ❌ 500 errors
- ❌ API key errors
- ❌ Database errors
- ❌ Rate limit errors

### Performance Metrics
- Response time < 2 seconds
- Lead generation < 30 seconds
- AI analysis < 5 seconds

## Step 8: Security Checklist

- [ ] SECRET_KEY is random and secure
- [ ] API keys are in environment variables (not in code)
- [ ] .env file is in .gitignore
- [ ] Rate limiting is enabled
- [ ] HTTPS is enforced
- [ ] CORS is configured properly
- [ ] Debug mode is OFF in production

## Troubleshooting

### Problem: 502 Bad Gateway
**Solution:**
- Check if app is running
- Check logs for startup errors
- Verify PORT environment variable

### Problem: API Keys Not Working
**Solution:**
- Verify keys are set in Render dashboard
- Check key format (no extra spaces)
- Test keys locally first

### Problem: Slow Performance
**Solution:**
- Increase worker count in gunicorn
- Add caching for API responses
- Optimize database queries

### Problem: Leads Not Saving
**Solution:**
- Check file permissions
- Verify data directory exists
- Check disk space

## Rollback Plan

If deployment fails:

1. **Revert to previous version:**
```bash
git revert HEAD
git push origin main
```

2. **Render will auto-deploy previous version**

3. **Or manually rollback in Render dashboard:**
   - Go to Deploys tab
   - Click "Rollback" on previous successful deploy

## Production URLs

- **Dashboard:** https://leads.ragspro.com
- **API Docs:** https://leads.ragspro.com/api/docs (if enabled)
- **Health Check:** https://leads.ragspro.com/api/stats

## Support

If issues persist:
1. Check logs in Render dashboard
2. Test locally with production environment variables
3. Verify all API keys are valid
4. Check DNS configuration for custom domain

## Success Criteria

✅ Dashboard loads at leads.ragspro.com  
✅ Lead generation works  
✅ AI Analyze works  
✅ Bulk operations work  
✅ No 404 errors  
✅ No 500 errors  
✅ Response time < 3 seconds  
✅ All features functional  

**System is production-ready!** 🚀
