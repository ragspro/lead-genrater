# 🔑 Kaha API Keys Daalni Hai? (Exact Locations)

## 📍 Sirf Ek File Edit Karni Hai!

**File:** `config/settings.json`

---

## 🎯 Step-by-Step

### 1. File Open Karo
```bash
nano config/settings.json
# Ya koi bhi editor use karo
```

### 2. Ye Dikhega:
```json
{
  "GOOGLE_SHEET_ID": "YOUR_GOOGLE_SHEET_ID_HERE",
  "GOOGLE_SERVICE_ACCOUNT_JSON": "config/service_account.json",
  "GEMINI_API_KEY": "YOUR_GEMINI_API_KEY_HERE",
  "GMAIL_ADDRESS": "your.email@gmail.com",
  "GMAIL_APP_PASSWORD": "YOUR_GMAIL_APP_PASSWORD_HERE",
  "MIN_RATING": 4.0,
  "MIN_REVIEWS": 20,
  "MAX_LEADS_PER_RUN": 50
}
```

### 3. Replace Karo:

#### A. Google Sheet ID
```json
"GOOGLE_SHEET_ID": "1abc...xyz"
```
**Kaha se milega?**
- Google Sheet URL: `https://docs.google.com/spreadsheets/d/1abc...xyz/edit`
- Copy karo: `1abc...xyz` part

#### B. Service Account JSON
```json
"GOOGLE_SERVICE_ACCOUNT_JSON": "config/service_account.json"
```
**Kya karna hai?**
- Google Cloud se download kiya hua JSON file
- Save karo as: `config/service_account.json`
- Ye line change mat karo!

#### C. Gemini API Key
```json
"GEMINI_API_KEY": "AIzaSyAbc123...xyz789"
```
**Kaha se milega?**
- https://makersuite.google.com/app/apikey
- Copy full key (starts with `AIza...`)

#### D. Gmail Address
```json
"GMAIL_ADDRESS": "your.actual.email@gmail.com"
```
**Kya daalna hai?**
- Tumhara Gmail address

#### E. Gmail App Password
```json
"GMAIL_APP_PASSWORD": "abcdefghijklmnop"
```
**Kaha se milega?**
- https://myaccount.google.com/apppasswords
- 16-character password (spaces remove karo)

---

## ✅ Final File Example

```json
{
  "GOOGLE_SHEET_ID": "1a2b3c4d5e6f7g8h9i0j",
  "GOOGLE_SERVICE_ACCOUNT_JSON": "config/service_account.json",
  "GEMINI_API_KEY": "AIzaSyAbc123def456ghi789jkl012mno345pqr678",
  "GMAIL_ADDRESS": "myemail@gmail.com",
  "GMAIL_APP_PASSWORD": "abcdefghijklmnop",
  "MIN_RATING": 4.0,
  "MIN_REVIEWS": 20,
  "MAX_LEADS_PER_RUN": 50
}
```

---

## 🎯 Aur Kuch Files?

### Service Account JSON
**Location:** `config/service_account.json`

**Content:** Google Cloud se download kiya hua file
```json
{
  "type": "service_account",
  "project_id": "your-project",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...",
  "client_email": "lead-bot@your-project.iam.gserviceaccount.com",
  ...
}
```

**Kya karna hai?**
- Download from Google Cloud
- Save as `config/service_account.json`
- Kuch edit mat karo!

---

## ✅ Verification

### Test Karo:
```bash
python test_free_system.py
```

### Should Show:
```
✅ Dependencies
✅ Playwright
✅ Configuration
  ✅ Google Sheet ID
  ✅ Service Account JSON path
  ✅ Gemini AI (optional but recommended)
  ✅ Gmail address (optional)
  ✅ Gmail app password (optional)
✅ Scraper
✅ AI
```

---

## 🐛 Common Mistakes

### ❌ Wrong:
```json
"GOOGLE_SHEET_ID": "https://docs.google.com/spreadsheets/d/1abc...xyz/edit"
```
### ✅ Right:
```json
"GOOGLE_SHEET_ID": "1abc...xyz"
```

---

### ❌ Wrong:
```json
"GMAIL_APP_PASSWORD": "abcd efgh ijkl mnop"
```
### ✅ Right:
```json
"GMAIL_APP_PASSWORD": "abcdefghijklmnop"
```

---

### ❌ Wrong:
```json
"GEMINI_API_KEY": "AIza... (with spaces or newlines)"
```
### ✅ Right:
```json
"GEMINI_API_KEY": "AIzaSyAbc123def456ghi789jkl012mno345pqr678"
```

---

## 🎯 Quick Checklist

- [ ] `config/settings.json` file edited
- [ ] Google Sheet ID added (just the ID, not full URL)
- [ ] `config/service_account.json` file saved
- [ ] Gemini API key added (starts with AIza...)
- [ ] Gmail address added
- [ ] Gmail app password added (no spaces)
- [ ] Test run: `python test_free_system.py`

---

## 🚀 Ready to Run!

```bash
# Test
python test_free_system.py

# If all ✅, run
python src/main_free.py
```

---

## 💡 Pro Tip

Agar koi key optional hai (Gemini, Gmail), to bhi system chalega!
- Without Gemini: No AI content generation
- Without Gmail: Manual email sending

But **recommended** hai sab keys add karo for full features!

---

## 📞 Need Help?

Check these files:
- `API_KEYS_GUIDE.md` - Detailed key generation
- `SETUP_GUIDE_HINDI.md` - Complete setup
- `QUICK_START.md` - 5-minute setup

---

**Bas ye ek file edit karo aur ready! 🎉**
