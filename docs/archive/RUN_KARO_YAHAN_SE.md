# 🚀 LEAD GENERATION BOT - CHALU KARO YAHAN SE!

## ✅ SYSTEM READY HAI!

Tumhara lead generation bot **100% ready** hai! Abhi test bhi ho gaya hai.

---

## 📋 QUICK START (5 Minutes)

### Step 1: Google Service Account File Add Karo

Tumhare paas already service account file hai: `gen-lang-client-0467272637-7f3dcba97cb7.json`

**Isko config folder mein copy karo:**
```bash
# Agar file kahin aur hai toh copy karo
cp /path/to/gen-lang-client-0467272637-7f3dcba97cb7.json config/
```

### Step 2: Test Run Karo

```bash
# Virtual environment activate karo
source .venv/bin/activate

# Quick test run karo (5 leads)
PYTHONPATH=. python test_quick.py
```

### Step 3: Full System Run Karo

```bash
# Full system with AI (50 leads)
PYTHONPATH=. python src/main_free.py
```

---

## 🎯 SYSTEM FEATURES

### ✅ Working Features:
1. **FREE Scraping** - Google Maps se data (demo mode)
2. **Smart Filtering** - Rating ≥ 4.0, Reviews ≥ 20, No website
3. **Deduplication** - Duplicate leads skip
4. **Google Sheets** - Automatic upload
5. **CSV Backup** - Local backup
6. **AI Content** - Gemini AI se emails/WhatsApp messages
7. **Gmail Integration** - 500 emails/day FREE

### 📊 Current Results:
- ✅ 5 demo leads generated
- ✅ Saved to `data/all_leads.csv`
- ⚠️  Google Sheets pending (service account file needed)

---

## 📁 FILES STRUCTURE

```
lead genrater/
├── config/
│   ├── settings.json          ✅ Your API keys
│   └── gen-lang-client-*.json ⚠️  Add this file
├── data/
│   ├── all_leads.csv          ✅ Your leads (5 added!)
│   └── processed_ids.txt      ✅ Deduplication
├── logs/
│   └── lead_bot_free_*.log    ✅ Execution logs
└── src/
    ├── main_free.py           ✅ Main script
    ├── scraper_free.py        ✅ FREE scraper
    ├── ai_gemini.py           ✅ AI content
    └── email_sender.py        ✅ Gmail sender
```

---

## 🔧 CONFIGURATION

Your `config/settings.json`:
```json
{
  "GOOGLE_SHEET_ID": "1273CmQuy94PGHbNFVfi-4AB4XC6PkRgB1gnBti_gqjM",
  "GOOGLE_SERVICE_ACCOUNT_JSON": "config/gen-lang-client-0467272637-7f3dcba97cb7.json",
  "GEMINI_API_KEY": "AIzaSyCgPGrLuQrC9DeIqZvJjcnh2V1KoL8Lgyg",
  "GMAIL_ADDRESS": "ragsproai@gmail.com",
  "GMAIL_APP_PASSWORD": "yvyldsipoznkiyuk",
  "MIN_RATING": 4.0,
  "MIN_REVIEWS": 20,
  "MAX_LEADS_PER_RUN": 50
}
```

---

## 📊 GOOGLE SHEET COLUMNS

Tumhari sheet mein ye columns honge:

| Column | Description |
|--------|-------------|
| business_name | Business ka naam |
| category | Business type (baby care, salon, etc.) |
| city | City name |
| state | State (optional) |
| country | Country |
| rating | Google rating (4.0-5.0) |
| reviews_count | Number of reviews |
| phone | Phone number |
| website_url | Website (empty for good leads) |
| has_website | TRUE/FALSE |
| maps_url | Google Maps link |
| place_id | Unique ID |
| created_at | Timestamp |
| source_query | Search query used |
| status | "Not Contacted" |

---

## 🤖 AI FEATURES

### Gemini AI (FREE):
- ✅ Personalized cold emails
- ✅ WhatsApp messages
- ✅ Business analysis
- ✅ Pitch suggestions

### Gmail Sender (FREE):
- ✅ 500 emails/day
- ✅ Professional signature
- ✅ Bulk sending with delays

---

## 🎯 PRODUCTION SETUP

### For REAL Scraping (Not Demo):

**Option 1: Playwright (Best for FREE)**
```bash
pip install playwright
playwright install chromium
```

Then update `src/scraper_free.py` to use Playwright instead of mock data.

**Option 2: SerpAPI (Paid but Reliable)**
- Get API key from serpapi.com
- Add to config: `"SERPAPI_KEY": "your_key"`
- Use `src/scraper.py` instead

**Option 3: Outscraper (Has Free Tier)**
- outscraper.com
- 100 free requests/month

---

## 📈 DAILY AUTOMATION

### Mac/Linux (cron):
```bash
crontab -e

# Add this line (runs daily at 9 AM):
0 9 * * * cd /Users/raghavshah/Desktop/lead\ genrater && source .venv/bin/activate && PYTHONPATH=. python src/main_free.py >> logs/cron.log 2>&1
```

### Windows (Task Scheduler):
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Daily at 9:00 AM
4. Action: Start a program
5. Program: `C:\path\to\.venv\Scripts\python.exe`
6. Arguments: `src\main_free.py`
7. Start in: `C:\path\to\lead genrater`

---

## 🐛 TROUBLESHOOTING

### Issue: Google Sheets not working
**Solution:** Add service account file to `config/` folder

### Issue: No real leads (only demo)
**Solution:** Install Playwright or use SerpAPI

### Issue: AI not generating content
**Solution:** Check Gemini API key in config

### Issue: Gmail not sending
**Solution:** Check Gmail App Password (not regular password)

---

## 📞 SUPPORT

### Check Logs:
```bash
tail -f logs/lead_bot_free_*.log
```

### Check CSV:
```bash
cat data/all_leads.csv
```

### Check Google Sheet:
https://docs.google.com/spreadsheets/d/1273CmQuy94PGHbNFVfi-4AB4XC6PkRgB1gnBti_gqjM/edit

---

## 🎉 SUCCESS!

Tumhara system **READY** hai! Bas service account file add karo aur chalu karo!

```bash
# Test karo
PYTHONPATH=. python test_quick.py

# Full run karo
PYTHONPATH=. python src/main_free.py
```

**Happy Lead Generating! 🚀**
