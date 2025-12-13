# 🧪 AI Analyze Testing Guide

## How to Test AI Analyze Button

### Step 1: Open Dashboard
```
http://localhost:5002
```

### Step 2: Check if Leads are Loaded
- You should see 20 Delhi dental clinics
- Each lead has a "🔍 AI Analyze" button

### Step 3: Click AI Analyze on Any Lead
1. Click the purple "🔍 AI Analyze" button
2. Wait 2-3 seconds
3. A modal should appear with:
   - 🎯 Quick Pitch
   - ⚠️ Pain Points (3-5 items)
   - 💡 RagsPro Solutions (3-5 items)
   - 💰 Revenue Opportunity
   - 📞 Call Script
   - 📧 Email Content
   - 💬 WhatsApp Message

### Step 4: Verify AI is Working
**Signs AI is working:**
- ✅ Modal appears within 3 seconds
- ✅ Content is personalized (mentions business name)
- ✅ Pain points are specific to the business
- ✅ Solutions are relevant
- ✅ Call script mentions business details

**Signs AI is NOT working:**
- ❌ Modal takes >10 seconds
- ❌ Generic content (no business name)
- ❌ Error message appears
- ❌ Empty fields

### Step 5: Check Browser Console
1. Press F12 to open Developer Tools
2. Go to Console tab
3. Look for:
   - ✅ "✅ Analysis complete!" (success)
   - ❌ Any red error messages (failure)

### Step 6: Check Backend Logs
Look at terminal where dashboard is running:
```
✅ Good logs:
INFO:src.ai_gemini:✅ Gemini AI initialized
INFO:__main__:Generated analysis for DR BHUTANI DENTAL CLINIC

❌ Bad logs:
ERROR:__main__:Lead analysis error: ...
ERROR:src.ai_gemini:Gemini AI error: ...
```

## How to Test Bulk AI Analyze

### Step 1: Select Multiple Leads
- Click checkboxes on 3-5 leads
- Bulk actions bar appears at bottom

### Step 2: Click "🤖 AI Analyze"
- Purple button in bulk actions bar
- Wait 3-5 seconds

### Step 3: Verify Results
- Modal shows analysis for all selected leads
- Each lead has: Quick Pitch, Pain Point, Solution

## Troubleshooting

### Problem: "AI not configured" error
**Solution:** Check if GEMINI_API_KEY is set
```bash
# Check config
cat src/config.py | grep GEMINI_API_KEY

# Should show:
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'your-key-here')
```

### Problem: Slow response (>10 seconds)
**Possible causes:**
- Gemini API rate limit
- Network issues
- API key invalid

**Solution:**
1. Check API key is valid
2. Check internet connection
3. Try again after 1 minute

### Problem: Generic content (not personalized)
**Cause:** AI fallback being used instead of real AI

**Solution:**
1. Verify GEMINI_API_KEY is correct
2. Check logs for "Gemini AI error"
3. Test API key separately

## Expected AI Response Example

```json
{
  "success": true,
  "analysis": {
    "pain_points": [
      "Strong reputation (4.9★) but limited online visibility",
      "No online booking system for 827+ satisfied patients",
      "Missing modern website to capture online searches",
      "Weak SEO - losing patients to competitors",
      "No mobile app for patient convenience"
    ],
    "solutions": [
      "Modern responsive website with SEO optimization",
      "Mobile app for iOS & Android",
      "Online appointment booking system",
      "AI-powered chatbot for 24/7 patient support",
      "Digital marketing & Google Ads management"
    ],
    "revenue_opportunity": "$50k-$200k project value",
    "quick_pitch": "Hi DR BHUTANI DENTAL CLINIC! Your 4.9★ rating shows patients love you. Let's capture the 70% searching online!",
    "call_script": "Hi, this is Raghav from RagsPro. I noticed DR BHUTANI DENTAL CLINIC has an amazing 4.9-star rating with 827 reviews! We help dental clinics like yours get 3-5x more patients through modern websites and apps. Do you have 2 minutes?"
  },
  "email_content": "[Full personalized email]",
  "whatsapp_content": "[Short WhatsApp message]"
}
```

## Production Checklist

Before deploying to leads.ragspro.com:

- [ ] AI Analyze works locally
- [ ] Bulk AI Analyze works locally
- [ ] GEMINI_API_KEY is set in environment
- [ ] SERPAPI_KEY is set in environment
- [ ] All endpoints return 200 (no 404s)
- [ ] Leads save correctly
- [ ] History loads without errors
- [ ] No console errors in browser
- [ ] No backend errors in logs

## Quick Test Command

```bash
# Test if AI endpoint is responding
curl -X POST http://localhost:5002/api/lead/analyze \
  -H "Content-Type: application/json" \
  -d '{"lead":{"title":"Test Clinic","type":"dental clinic","rating":4.5,"reviews":100,"address":"Delhi, India"}}'

# Should return JSON with analysis
```

If this returns valid JSON with pain_points, solutions, etc., AI is working! ✅
