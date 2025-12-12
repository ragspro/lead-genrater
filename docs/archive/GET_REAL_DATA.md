# 🎯 GET REAL DATA - NO FAKE/DEMO!

## ⚠️ IMPORTANT: API Keys Required for REAL Data

Raghav bhai, **REAL data** ke liye tumhe ek FREE API key chahiye. Main 3 options de raha hoon (sab FREE hain):

---

## 🚀 OPTION 1: Outscraper (RECOMMENDED)

### Why Outscraper?
- ✅ **100% REAL Google Maps data**
- ✅ **100 requests FREE/month**
- ✅ **Best quality data**
- ✅ **Easy to use**

### How to Get:

#### Step 1: Sign Up
1. Go to: https://outscraper.com/
2. Click "Sign Up" (FREE)
3. Verify email

#### Step 2: Get API Key
1. Go to: https://app.outscraper.com/api-keys
2. Click "Create New API Key"
3. Copy the key

#### Step 3: Add to Config
```bash
# Edit config file
nano config/settings.json
```

Add this line:
```json
{
  "OUTSCRAPER_API_KEY": "your_key_here",
  ...
}
```

#### Step 4: Update Scraper
```bash
# Edit scraper file
nano src/scraper_free.py
```

Find this line:
```python
OUTSCRAPER_API_KEY = "your_key_here"
```

Replace with your actual key:
```python
OUTSCRAPER_API_KEY = "YourActualKeyHere123"
```

---

## 🚀 OPTION 2: Serper.dev (BEST FREE TIER)

### Why Serper?
- ✅ **2,500 searches FREE/month** (Most generous!)
- ✅ **REAL Google Maps data**
- ✅ **Fast & reliable**
- ✅ **No credit card required**

### How to Get:

#### Step 1: Sign Up
1. Go to: https://serper.dev/
2. Click "Sign Up" (FREE)
3. Verify email

#### Step 2: Get API Key
1. Dashboard will show your API key
2. Copy it

#### Step 3: Update Scraper
```bash
nano src/scraper_free.py
```

Find this line:
```python
'X-API-KEY': 'your_serper_key_here'
```

Replace with your key:
```python
'X-API-KEY': 'YourActualKeyHere123'
```

---

## 🚀 OPTION 3: SerpAPI (PAID BUT RELIABLE)

### Why SerpAPI?
- ✅ **100 searches FREE/month**
- ✅ **Most reliable**
- ✅ **Best documentation**
- ✅ **Used by professionals**

### How to Get:

#### Step 1: Sign Up
1. Go to: https://serpapi.com/
2. Click "Register" (FREE)
3. Verify email

#### Step 2: Get API Key
1. Go to: https://serpapi.com/manage-api-key
2. Copy your API key

#### Step 3: Add to Config
```json
{
  "SERPAPI_KEY": "your_serpapi_key_here",
  ...
}
```

#### Step 4: Use SerpAPI Scraper
```bash
# Use the paid scraper (more reliable)
PYTHONPATH=. python src/main.py
```

---

## 📊 COMPARISON

| API | Free Tier | Quality | Speed | Recommended |
|-----|-----------|---------|-------|-------------|
| **Serper** | 2,500/month | ⭐⭐⭐⭐⭐ | Fast | ✅ BEST |
| **Outscraper** | 100/month | ⭐⭐⭐⭐⭐ | Medium | ✅ Good |
| **SerpAPI** | 100/month | ⭐⭐⭐⭐⭐ | Fast | Paid |

---

## 🎯 QUICK SETUP (5 Minutes)

### For Serper (RECOMMENDED):

```bash
# 1. Sign up at serper.dev
# 2. Copy API key
# 3. Edit scraper
nano src/scraper_free.py

# 4. Find and replace:
'X-API-KEY': 'your_serper_key_here'
# with:
'X-API-KEY': 'YourActualKey123'

# 5. Test
source .venv/bin/activate
PYTHONPATH=. python test_quick.py
```

---

## ✅ VERIFY REAL DATA

After adding API key, test:

```bash
source .venv/bin/activate
PYTHONPATH=. python test_quick.py
```

You should see:
```
🔍 Scraping REAL data for: baby care in Delhi, India
✅ Found: ABC Baby Care (4.5★)
✅ Found: XYZ Day Care (4.7★)
✅ Scraped 5 REAL businesses
```

**NOT this:**
```
⚠️  Returning MOCK data for demonstration
Demo Baby Care #1
```

---

## 🚀 FULL SYSTEM WITH REAL DATA

Once API key is added:

### Step 1: Start Dashboard
```bash
./START_DASHBOARD.sh
```

### Step 2: Generate REAL Leads
1. Open `http://localhost:5000`
2. Click "Generate New Leads"
3. Wait 2-3 minutes
4. ✅ 50 REAL leads!

### Step 3: Verify Data
```bash
cat data/all_leads.csv
```

You'll see REAL businesses:
- Real business names
- Real phone numbers
- Real addresses
- Real ratings
- Real reviews

---

## 💡 PRO TIPS

### Tip 1: Use Multiple APIs
```python
# Try Serper first (2,500 free)
# Fallback to Outscraper (100 free)
# Total: 2,600 free searches/month!
```

### Tip 2: Cache Results
```python
# Save results to avoid re-scraping
# Use deduplication (already built-in)
```

### Tip 3: Rate Limiting
```python
# Add delays between requests
time.sleep(2)  # 2 seconds between searches
```

### Tip 4: Optimize Queries
```python
# Be specific
"baby care in Gurgaon, India"  # Good
"baby care"  # Too broad
```

---

## 🐛 TROUBLESHOOTING

### Issue: Still seeing demo data
**Solution:**
1. Check API key is correct
2. Check API key is in right place
3. Check internet connection
4. Check API quota (not exceeded)

### Issue: API error 402
**Solution:** Out of free credits. Use another API or wait for reset.

### Issue: No results
**Solution:**
1. Check query is valid
2. Try different city
3. Check API status

### Issue: Slow scraping
**Solution:** Normal! Real scraping takes time (2-3 seconds per query)

---

## 📞 NEED HELP?

### Check Logs:
```bash
tail -f logs/*.log
```

### Test API:
```bash
# Test Serper
curl -X POST https://google.serper.dev/maps \
  -H 'X-API-KEY: your_key' \
  -H 'Content-Type: application/json' \
  -d '{"q":"baby care in Delhi"}'
```

---

## 🎉 READY FOR REAL DATA!

Once you add API key:
1. ✅ No more demo/fake data
2. ✅ 100% REAL businesses
3. ✅ REAL phone numbers
4. ✅ REAL addresses
5. ✅ REAL ratings
6. ✅ REAL leads!

---

## 🚀 RECOMMENDED SETUP

**Best FREE combination:**

1. **Serper.dev** - 2,500 searches/month (PRIMARY)
2. **Outscraper** - 100 searches/month (BACKUP)
3. **Total:** 2,600 FREE searches/month!

**That's 2,600 REAL leads per month for FREE! 🎉**

---

**Get your API key now:**
- Serper: https://serper.dev/ (2,500 free)
- Outscraper: https://outscraper.com/ (100 free)

**Then run:**
```bash
./START_DASHBOARD.sh
```

**LET'S GET REAL LEADS! 🚀**
