# 🔑 API Keys Setup Guide - Step by Step

## Kaha se kya API key milega? (All FREE!)

---

## 1️⃣ Google Sheets API (FREE)

### Step 1: Google Cloud Console
1. Jao: https://console.cloud.google.com/
2. **New Project** click karo
3. Project name: "Lead Generation Bot"
4. **Create** click karo

### Step 2: Enable Google Sheets API
1. Left menu → **APIs & Services** → **Library**
2. Search: "Google Sheets API"
3. **Enable** click karo

### Step 3: Create Service Account
1. Left menu → **APIs & Services** → **Credentials**
2. **Create Credentials** → **Service Account**
3. Name: "lead-bot-service"
4. **Create and Continue**
5. Role: **Editor**
6. **Done**

### Step 4: Download JSON Key
1. Service Accounts list mein apna account click karo
2. **Keys** tab → **Add Key** → **Create New Key**
3. Type: **JSON**
4. **Create** - file download hogi
5. File ko `config/service_account.json` mein save karo

### Step 5: Share Google Sheet
1. Naya Google Sheet banao
2. Service account email copy karo (JSON file mein hai)
   - Example: `lead-bot-service@project-id.iam.gserviceaccount.com`
3. Sheet ko is email ke saath **share** karo
4. Permission: **Editor**
5. Sheet URL se ID copy karo:
   - URL: `https://docs.google.com/spreadsheets/d/1abc...xyz/edit`
   - ID: `1abc...xyz` (ye part copy karo)

**✅ Done! Google Sheets ready hai**

---

## 2️⃣ Gemini AI API (FREE)

### Step 1: Get API Key
1. Jao: https://makersuite.google.com/app/apikey
2. Google account se login karo
3. **Create API Key** click karo
4. **Create API key in new project** select karo
5. API key copy karo

### Example Key:
```
AIzaSyAbc123...xyz789
```

### FREE Limits:
- ✅ 60 requests per minute
- ✅ Unlimited daily requests (fair use)
- ✅ No credit card needed
- ✅ No expiry

**✅ Done! Gemini AI ready hai**

---

## 3️⃣ Gmail SMTP (FREE - 500/day)

### Step 1: Enable 2-Step Verification
1. Jao: https://myaccount.google.com/security
2. **2-Step Verification** click karo
3. Enable karo (phone number chahiye)

### Step 2: Generate App Password
1. Jao: https://myaccount.google.com/apppasswords
2. **Select app**: Mail
3. **Select device**: Other (Custom name)
4. Name: "Lead Bot"
5. **Generate** click karo
6. 16-character password copy karo

### Example Password:
```
abcd efgh ijkl mnop
```

**Important:**
- Ye password regular Gmail password NAHI hai
- Ye sirf app ke liye hai
- Spaces hata do jab config mein paste karo

**✅ Done! Gmail ready hai**

---

## 📝 Final Configuration File

Ab `config/settings.json` file edit karo:

```json
{
  "GOOGLE_SHEET_ID": "1abc...xyz",
  "GOOGLE_SERVICE_ACCOUNT_JSON": "config/service_account.json",
  "GEMINI_API_KEY": "AIzaSyAbc123...xyz789",
  "GMAIL_ADDRESS": "your.email@gmail.com",
  "GMAIL_APP_PASSWORD": "abcdefghijklmnop",
  "MIN_RATING": 4.0,
  "MIN_REVIEWS": 20,
  "MAX_LEADS_PER_RUN": 50
}
```

---

## ✅ Verification Checklist

### Google Sheets
- [ ] Service account JSON file downloaded
- [ ] File saved as `config/service_account.json`
- [ ] Google Sheet created
- [ ] Sheet shared with service account email
- [ ] Sheet ID copied to config

### Gemini AI
- [ ] API key generated
- [ ] Key copied to config
- [ ] Starts with `AIza...`

### Gmail
- [ ] 2-Step Verification enabled
- [ ] App Password generated
- [ ] Password copied to config (no spaces)
- [ ] Gmail address added to config

---

## 🧪 Test Your Setup

```bash
python test_free_system.py
```

Ye script check karega:
- ✅ All dependencies installed
- ✅ Playwright browsers ready
- ✅ Config file valid
- ✅ API keys working
- ✅ Scraper functional
- ✅ AI generating content

---

## 🐛 Common Issues

### "Service account not found"
- JSON file path check karo
- File name exactly `service_account.json` hona chahiye

### "Permission denied" (Google Sheets)
- Sheet ko service account email ke saath share karo
- Editor permission do (Viewer nahi)

### "Invalid API key" (Gemini)
- API key copy-paste properly karo
- Spaces ya extra characters nahi hone chahiye

### "Authentication failed" (Gmail)
- 2-Step Verification enable hai?
- App Password use kar rahe ho (regular password nahi)
- Spaces remove karo password se

---

## 💡 Pro Tips

1. **Keep Keys Safe:**
   - Config file ko git mein commit mat karo
   - `.gitignore` already setup hai

2. **Test Individually:**
   - Pehle Google Sheets test karo
   - Phir Gemini AI
   - Phir Gmail

3. **Backup Keys:**
   - API keys ko safe jagah save karo
   - Service account JSON ka backup rakho

4. **Monitor Usage:**
   - Gemini: https://makersuite.google.com/
   - Gmail: Daily 500 limit yaad rakho
   - Google Sheets: Unlimited hai

---

## 🎯 Ready to Go!

Sab keys setup ho gaye? Test karo:

```bash
python test_free_system.py
```

Agar sab ✅ hai, to run karo:

```bash
python src/main_free.py
```

**Happy Lead Generating! 🚀**
