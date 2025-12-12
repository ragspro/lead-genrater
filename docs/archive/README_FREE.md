# 🚀 FREE Lead Generation Bot with AI

## 💰 TOTAL COST: ₹0 (100% FREE!)

Complete lead generation system with:
- ✅ **FREE Scraping** (Playwright - no API costs!)
- ✅ **FREE AI** (Google Gemini)
- ✅ **FREE Email** (Gmail - 500/day)
- ✅ **FREE Storage** (Google Sheets + CSV)

---

## 🎯 Quick Start (5 Minutes)

### 1. Install
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

### 2. Configure
Edit `config/settings.json`:
```json
{
  "GOOGLE_SHEET_ID": "your_sheet_id",
  "GOOGLE_SERVICE_ACCOUNT_JSON": "config/service_account.json",
  "GEMINI_API_KEY": "your_gemini_key",
  "GMAIL_ADDRESS": "your@gmail.com",
  "GMAIL_APP_PASSWORD": "your_app_password",
  "MIN_RATING": 4.0,
  "MIN_REVIEWS": 20,
  "MAX_LEADS_PER_RUN": 50
}
```

### 3. Test
```bash
python test_free_system.py
```

### 4. Run
```bash
python src/main_free.py
```

---

## 🔑 Where to Get API Keys (All FREE!)

### Google Sheets (FREE)
1. Go to: https://console.cloud.google.com/
2. Create project → Enable Google Sheets API
3. Create Service Account → Download JSON
4. Share your sheet with service account email

### Gemini AI (FREE)
1. Go to: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key

**Limits:** 60 requests/min, unlimited daily (fair use)

### Gmail (FREE - 500/day)
1. Enable 2-Step Verification
2. Go to: https://myaccount.google.com/apppasswords
3. Generate App Password
4. Copy the password

---

## 📊 What You Get

### 1. Scraped Leads
- Business name, rating, reviews
- Address, phone, category
- No website (perfect targets!)

### 2. AI-Generated Content
```
📧 EMAIL:
Hi, I noticed ABC Day Care has excellent reputation with 4.5 stars...

💬 WHATSAPP:
Hi! 👋 I noticed ABC Day Care doesn't have a website...
```

### 3. Storage
- Google Sheets (collaborative)
- CSV backup (local)
- AI content file (ready to use)

---

## 🎨 Features

### FREE Scraping
- Uses Playwright (no API costs!)
- Scrapes Google Maps directly
- ~50 leads/day realistic
- No rate limits

### AI Content Generation
- Personalized emails
- WhatsApp messages
- Business analysis
- Powered by Gemini (FREE)

### Smart Filtering
- Rating ≥ 4.0
- Reviews ≥ 20
- No website (perfect targets!)
- Auto deduplication

### Dual Storage
- Google Sheets (team access)
- CSV backup (local)
- AI content files

---

## 📈 Daily Workflow

```
1. Run bot (morning)
   → 50 new leads scraped
   → AI content generated
   
2. Review leads (afternoon)
   → Check Google Sheet
   → Read AI content file
   
3. Outreach (evening)
   → Send 10 emails
   → Send 10 WhatsApp messages
   
4. Track results
   → Update sheet with responses
   → Adjust strategy
```

---

## 💡 Realistic Expectations

**FREE Tier Limits:**
- Scraping: ~50 leads/day
- Gemini AI: Unlimited (fair use)
- Gmail: 500 emails/day
- Google Sheets: Unlimited

**Expected Results:**
- 50 leads/day
- 10 contacts/day
- 1 client every 10-15 days
- ₹15k/client average
- **= ₹30k/month (ZERO cost!)**

---

## 🛠️ Customization

### Add Cities/Categories
Edit `src/queries.py`:
```python
CITIES = [
    "Delhi, India",
    "Mumbai, India",
    # Add your cities
]

CATEGORIES = [
    "day care centre",
    "salon",
    # Add your categories
]
```

### Adjust Filters
Edit `config/settings.json`:
```json
{
  "MIN_RATING": 4.0,
  "MIN_REVIEWS": 20,
  "MAX_LEADS_PER_RUN": 50
}
```

---

## 📚 Documentation

- **Setup Guide (Hindi):** `SETUP_GUIDE_HINDI.md`
- **Implementation Status:** `IMPLEMENTATION_STATUS.md`
- **Original README:** `README.md`

---

## 🐛 Troubleshooting

### Playwright Error
```bash
playwright install chromium
```

### Google Sheets Permission Denied
Share sheet with service account email (Editor access)

### Gmail Authentication Failed
- Enable 2-Step Verification
- Use App Password (not regular password)

### Gemini API Error
- Check API key
- Check internet connection
- Wait if rate limited

---

## 🎯 Pro Tips

1. **Start Small:** Test with 5-10 leads first
2. **Review AI Content:** Edit before sending
3. **Track Results:** Note what works
4. **Be Consistent:** Daily outreach is key
5. **Personalize:** Add personal touch to AI content

---

## 🚀 Ready to Start!

```bash
# Test everything
python test_free_system.py

# Run the bot
python src/main_free.py

# Check results
cat data/ai_content_*.txt
```

---

## 📞 Support

Check these files for help:
- `SETUP_GUIDE_HINDI.md` - Detailed setup (Hindi)
- `test_free_system.py` - System diagnostics
- `IMPLEMENTATION_STATUS.md` - Technical details

---

## 🎉 Success!

**You now have a complete FREE lead generation system!**

No monthly costs, no API fees, just results! 🚀

---

**Made with ❤️ for Indian entrepreneurs**
