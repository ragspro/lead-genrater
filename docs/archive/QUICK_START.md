# ⚡ Quick Start - 5 Minutes Setup

## 🚀 Sabse Pehle Ye Karo

```bash
# 1. Install everything
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium

# 2. Test system
python test_free_system.py

# 3. Run bot
python src/main_free.py
```

---

## 🔑 API Keys Kaha Se Milenge?

### 1. Google Sheets (2 mins)
```
1. https://console.cloud.google.com/
2. New Project → Enable Sheets API
3. Create Service Account → Download JSON
4. Save as: config/service_account.json
5. Share sheet with service account email
```

### 2. Gemini AI (30 seconds)
```
1. https://makersuite.google.com/app/apikey
2. Create API Key
3. Copy key (starts with AIza...)
```

### 3. Gmail (1 min)
```
1. Enable 2-Step Verification
2. https://myaccount.google.com/apppasswords
3. Generate App Password
4. Copy 16-character password
```

---

## ⚙️ Config File

Edit `config/settings.json`:

```json
{
  "GOOGLE_SHEET_ID": "PASTE_SHEET_ID_HERE",
  "GOOGLE_SERVICE_ACCOUNT_JSON": "config/service_account.json",
  "GEMINI_API_KEY": "PASTE_GEMINI_KEY_HERE",
  "GMAIL_ADDRESS": "your@gmail.com",
  "GMAIL_APP_PASSWORD": "PASTE_APP_PASSWORD_HERE",
  "MIN_RATING": 4.0,
  "MIN_REVIEWS": 20,
  "MAX_LEADS_PER_RUN": 50
}
```

---

## ✅ Test Checklist

```bash
python test_free_system.py
```

Should show:
- ✅ Dependencies
- ✅ Playwright
- ✅ Configuration
- ✅ Scraper
- ✅ AI

---

## 🎯 First Run

```bash
python src/main_free.py
```

Output:
- `data/all_leads.csv` - Leads
- `data/ai_content_*.txt` - AI content
- `logs/lead_bot_free_*.log` - Logs

---

## 📊 Check Results

```bash
# View AI content
cat data/ai_content_*.txt

# View leads
cat data/all_leads.csv

# View logs
tail -f logs/lead_bot_free_*.log
```

---

## 🐛 If Error

### "Playwright not found"
```bash
playwright install chromium
```

### "Config error"
Check `API_KEYS_GUIDE.md` for detailed setup

### "Permission denied"
Share Google Sheet with service account email

---

## 💡 Quick Tips

1. **Test first:** `python test_free_system.py`
2. **Start small:** 5-10 leads first
3. **Review AI:** Check content quality
4. **Track results:** Note what works

---

## 📚 Full Guides

- **Complete Setup:** `SETUP_GUIDE_HINDI.md`
- **API Keys:** `API_KEYS_GUIDE.md`
- **Full Docs:** `README_FREE.md`
- **Summary:** `COMPLETE_SYSTEM_SUMMARY.md`

---

## 🎉 Ready!

```bash
python src/main_free.py
```

**Happy Lead Generating! 🚀**
