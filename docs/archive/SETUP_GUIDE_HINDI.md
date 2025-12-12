# 🚀 FREE Lead Generation Bot - Complete Setup Guide

## 💰 TOTAL COST: ₹0 (100% FREE!)

Ye system **completely FREE** hai. Koi paid API nahi chahiye!

---

## 📋 Step 1: Install Dependencies

```bash
# Virtual environment banao
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Dependencies install karo
pip install -r requirements.txt

# Playwright browsers install karo (FREE scraping ke liye)
playwright install chromium
```

---

## 🔑 Step 2: API Keys Setup (Sab FREE!)

### 2.1 Google Sheets Setup (FREE)

1. **Google Cloud Console** pe jao: https://console.cloud.google.com/
2. Naya project banao
3. **Google Sheets API** enable karo
4. **Service Account** banao:
   - IAM & Admin → Service Accounts → Create Service Account
   - JSON key download karo
   - File ko `config/service_account.json` mein save karo
5. **Google Sheet** banao aur service account email ko **Editor** access do

### 2.2 Gemini AI Setup (FREE!)

1. Jao: https://makersuite.google.com/app/apikey
2. **Create API Key** click karo
3. API key copy karo

**FREE Limits:**
- ✅ 60 requests per minute
- ✅ Unlimited daily usage (fair use policy)
- ✅ No credit card needed!

### 2.3 Gmail Setup (FREE - 500 emails/day)

1. Gmail account mein jao
2. **2-Step Verification** enable karo
3. **App Password** generate karo:
   - Jao: https://myaccount.google.com/apppasswords
   - "Mail" select karo
   - Password copy karo

**FREE Limits:**
- ✅ 500 emails per day
- ✅ No cost!

---

## ⚙️ Step 3: Configuration File

`config/settings.json` file edit karo:

```json
{
  "GOOGLE_SHEET_ID": "1abc...xyz",
  "GOOGLE_SERVICE_ACCOUNT_JSON": "config/service_account.json",
  "GEMINI_API_KEY": "AIza...your_key",
  "GMAIL_ADDRESS": "your.email@gmail.com",
  "GMAIL_APP_PASSWORD": "abcd efgh ijkl mnop",
  "MIN_RATING": 4.0,
  "MIN_REVIEWS": 20,
  "MAX_LEADS_PER_RUN": 50
}
```

### 🔍 Kaha se milega kya?

| Field | Kaha se milega |
|-------|---------------|
| `GOOGLE_SHEET_ID` | Google Sheet URL se: `docs.google.com/spreadsheets/d/[YE_ID_HAI]/edit` |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | Google Cloud Console se download kiya hua JSON file |
| `GEMINI_API_KEY` | https://makersuite.google.com/app/apikey |
| `GMAIL_ADDRESS` | Tumhara Gmail address |
| `GMAIL_APP_PASSWORD` | https://myaccount.google.com/apppasswords se generate kiya |

---

## 🎯 Step 4: Cities aur Categories Customize Karo

`src/queries.py` file edit karo:

```python
CITIES = [
    "Delhi, India",
    "Mumbai, India",
    "Bangalore, India",
    # Apne cities add karo
]

CATEGORIES = [
    "day care centre",
    "salon",
    "gym",
    # Apne categories add karo
]
```

---

## ▶️ Step 5: Run Karo!

```bash
# FREE version run karo (Playwright scraping + AI)
python src/main_free.py
```

### Kya hoga?

1. ✅ **FREE Scraping**: Playwright se Google Maps scrape hoga (no API cost!)
2. ✅ **Filtering**: Rating ≥ 4.0, Reviews ≥ 20, No website
3. ✅ **Deduplication**: Duplicate leads skip honge
4. ✅ **AI Content**: Gemini se email aur WhatsApp messages generate honge
5. ✅ **Storage**: Google Sheets + CSV backup
6. ✅ **AI Content File**: `data/ai_content_*.txt` mein save hoga

---

## 📊 Output Files

### 1. Google Sheets
Sare leads yaha save honge with all details

### 2. CSV Backup
`data/all_leads.csv` - Local backup

### 3. AI Generated Content
`data/ai_content_TIMESTAMP.txt` - Email aur WhatsApp messages

Example:
```
================================================================================
LEAD #1: ABC Day Care
================================================================================

📧 EMAIL:
--------------------------------------------------------------------------------
Hi,

I noticed ABC Day Care has an excellent reputation with 4.5 stars and 150 
reviews! However, I couldn't find your website online...

💬 WHATSAPP:
--------------------------------------------------------------------------------
Hi! 👋 I noticed ABC Day Care doesn't have a website. I help day care 
businesses get online with affordable websites...
```

---

## 🔄 Daily Automation (Optional)

### Linux/Mac (cron):
```bash
crontab -e
# Add:
0 9 * * * cd /path/to/project && /path/to/venv/bin/python src/main_free.py
```

### Windows (Task Scheduler):
1. Task Scheduler kholo
2. "Create Basic Task"
3. Daily, 9:00 AM
4. Action: `C:\path\to\venv\Scripts\python.exe`
5. Arguments: `C:\path\to\project\src\main_free.py`

---

## 📈 Daily Limits (FREE Tier)

| Service | Daily Limit | Cost |
|---------|-------------|------|
| Playwright Scraping | ~500 leads/day | ₹0 |
| Gemini AI | Unlimited (fair use) | ₹0 |
| Gmail Sending | 500 emails/day | ₹0 |
| Google Sheets | Unlimited | ₹0 |

**Reality Check:**
- 50 leads/day scrape karo
- 10 emails/day bhejo
- 1 client har 10-15 din mein
- Avg ₹15k/client = **₹30k/month** (ZERO cost!)

---

## 🎨 AI Prompts (Manual Use)

Agar AI automatic nahi chal raha, to manually use karo:

### Email Generation Prompt:
```
Write a short cold email (max 80 words) to [Business Name], 
a [Business Type] in [City] with [Rating] stars and [Reviews] reviews.

Mention their good reputation and missing website opportunity.
Offer affordable website services.
Tone: Friendly Indian English.
```

### WhatsApp Prompt:
```
Write a WhatsApp intro message for [Business Name], a [Business Type].
Very casual, friendly, use emojis. Max 50 words.
Offer affordable website services.
```

---

## 🐛 Troubleshooting

### "Playwright not found"
```bash
playwright install chromium
```

### "Google Sheets permission denied"
Service account email ko sheet mein Editor access do

### "Gmail authentication failed"
- 2-Step Verification enable karo
- App Password use karo (regular password nahi)

### "Gemini API error"
- API key check karo
- Internet connection check karo
- Daily limit exceed ho sakta hai (wait karo)

---

## 🎯 Next Steps

1. ✅ System test karo with 5-10 leads
2. ✅ AI generated content check karo
3. ✅ Manual outreach start karo
4. ✅ Results track karo
5. ✅ Scale karo gradually

---

## 💡 Pro Tips

1. **Start Small**: Pehle 10 leads/day se start karo
2. **Test AI Content**: Pehle manually check karo quality
3. **Personalize**: AI content ko thoda edit karo before sending
4. **Track Results**: Kaun se messages work kar rahe hain
5. **Be Patient**: Consistency is key!

---

## 🚀 Ready to Start!

```bash
# Test run
python src/main_free.py

# Check output
cat data/ai_content_*.txt
```

**Sab kuch FREE hai! Bas API keys setup karo aur start karo! 🎉**
