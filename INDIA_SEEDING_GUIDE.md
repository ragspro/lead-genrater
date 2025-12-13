# 🇮🇳 India Database Seeding with AI Analysis

## Overview

Complete database seeding for **ALL major Indian cities** with **AI analysis** for every lead.

**Features:**
- ✅ 50 major Indian cities (Tier 1 + Tier 2)
- ✅ 20 business categories
- ✅ AI analysis for every lead
- ✅ Pain points, solutions, scripts stored in DB
- ✅ 100% REAL verified data

## What Gets Seeded

### Cities (50):

**Tier 1 (8):**
- Mumbai, Delhi, Bangalore, Hyderabad
- Chennai, Kolkata, Pune, Ahmedabad

**Tier 2 (42):**
- Jaipur, Surat, Lucknow, Kanpur, Nagpur, Indore
- Thane, Bhopal, Visakhapatnam, Patna, Vadodara
- Ghaziabad, Ludhiana, Agra, Nashik, Faridabad
- Meerut, Rajkot, Varanasi, Srinagar, Aurangabad
- Dhanbad, Amritsar, Navi Mumbai, Allahabad, Ranchi
- Howrah, Coimbatore, Jabalpur, Gwalior, Vijayawada
- Jodhpur, Madurai, Raipur, Kota, Chandigarh
- Guwahati, and more...

### Categories (20):
1. Dental clinic
2. Law firm
3. Chartered accountant
4. Real estate agent
5. Software company
6. Consulting firm
7. Medical clinic
8. Diagnostic center
9. Pathology lab
10. Physiotherapy clinic
11. Restaurant
12. Hotel
13. Cafe
14. Gym
15. Spa
16. Salon
17. Boutique
18. Jewelry store
19. Coaching center
20. Training institute

### Expected Results:
- **Queries:** 50 cities × 20 categories = 1,000
- **Leads:** ~12,000-15,000 verified
- **AI Analyzed:** 100% of leads
- **Time:** ~4-5 hours
- **Cost:** ~₹5,000-8,000 (SerpAPI + Gemini)

## AI Analysis Includes:

For EVERY lead:
1. **Pain Points** (3 specific problems)
2. **Solutions** (3 RagsPro solutions)
3. **Revenue Opportunity** (in INR)
4. **Quick Pitch** (compelling one-liner)
5. **Call Script** (30-second Hindi/English)
6. **Email Content** (full template)
7. **WhatsApp Message** (ready to send)

## Prerequisites

### 1. API Keys
```python
# In src/config.py:
SERPAPI_KEY = 'your-serpapi-key'
GEMINI_API_KEY = 'your-gemini-key'
```

### 2. Environment
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## Quick Test (Recommended First)

Test with 2 cities × 3 categories = 6 queries:

```bash
python3 test_seed_india.py
```

This will:
- Test Delhi + Mumbai
- Test 3 categories
- Verify AI analysis works
- Take ~5 minutes
- Cost ~₹50

**Check output:**
```bash
# Should show ~30-60 leads
python3 -c "import json; print(len(json.load(open('data/premium_leads.json'))))"

# Check AI analysis
python3 -c "import json; lead = json.load(open('data/premium_leads.json'))[0]; print('AI Analysis:', 'ai_analysis' in lead)"
```

## Full Seeding

After test succeeds:

```bash
python3 seed_india_with_ai.py
```

### Progress Output:
```
🏙️  Processing: Mumbai, India
   ============================================================

   [1/1000] 🔍 dental clinic in Mumbai, India
      ✅ Found 18 quality leads
      🤖 AI analyzing: Dr. Sharma Dental Clinic...
      🤖 AI analyzing: Mumbai Dental Care...
      ...
      💾 Total leads: 18 (18 AI analyzed)

   [2/1000] 🔍 law firm in Mumbai, India
      ✅ Found 20 quality leads
      🤖 AI analyzing: Sharma & Associates...
      ...
```

### What Happens:
1. **Scrapes** each city × category
2. **Filters** for quality (70+ score)
3. **AI analyzes** each lead individually
4. **Stores** everything in database
5. **Shows** progress in real-time

## Output Files

### 1. Main Database
```
data/premium_leads.json
```
Contains all leads with AI analysis.

### 2. History
```
data/history/leads_india_2025-12-12.json
```
Timestamped snapshot with metadata.

### 3. Backup
```
data/backups/india_seed_20251212_190000.json
```
Safety backup.

## Database Structure

Each lead includes:

```json
{
  "title": "Dr. Sharma Dental Clinic",
  "type": "Dental clinic",
  "rating": 4.8,
  "reviews": 245,
  "address": "Connaught Place, New Delhi, India",
  "phone": "+91-11-12345678",
  "website": "https://example.com",
  "quality_score": 85,
  "generated_at": "2025-12-12T19:00:00",
  "seed_city": "Delhi, India",
  "seed_category": "dental clinic",
  "seed_country": "India",
  
  "ai_analysis": {
    "pain_points": [
      "Strong reputation (4.8★) but limited online visibility",
      "No online booking system for 245+ satisfied patients",
      "Missing Hindi/English website for broader reach"
    ],
    "solutions": [
      "Bilingual website with online booking",
      "Local SEO for Delhi dental searches",
      "WhatsApp Business for patient support"
    ],
    "revenue_opportunity": "₹3-8 lakhs",
    "quick_pitch": "Transform Dr. Sharma's 4.8★ reputation into 3x more patients!",
    "call_script": "Namaste! Main Raghav, RagsPro se. Dr. Sharma Dental Clinic ki 4.8★ rating dekhi - bahut impressive! Hum dental clinics ko online grow karne mein help karte hain. 2 minute baat kar sakte hain?"
  },
  
  "ai_email": "[Full personalized email in English]",
  "ai_whatsapp": "[Short WhatsApp message]",
  "ai_analyzed_at": "2025-12-12T19:00:15"
}
```

## Verification

### 1. Check Count
```bash
python3 -c "import json; data = json.load(open('data/premium_leads.json')); print(f'Total: {len(data)}')"
```

### 2. Check AI Analysis
```bash
python3 -c "import json; data = json.load(open('data/premium_leads.json')); with_ai = sum(1 for l in data if 'ai_analysis' in l); print(f'AI Analyzed: {with_ai}/{len(data)}')"
```

### 3. View Sample Lead
```bash
python3 -c "import json; lead = json.load(open('data/premium_leads.json'))[0]; print(json.dumps(lead, indent=2))" | head -50
```

### 4. Start Dashboard
```bash
python3 dashboard_ragspro.py
```

Open: http://localhost:5002

**You should see:**
- All Indian cities' leads
- AI Analyze button shows pre-analyzed data
- Pain points, solutions already stored

## Statistics

After completion:

```
📈 Database Statistics:
   ============================================================

   Top 10 Cities:
      Mumbai, India: 892 leads
      Delhi, India: 845 leads
      Bangalore, India: 823 leads
      ...

   Top 10 Categories:
      dental clinic: 645 leads
      software company: 612 leads
      restaurant: 589 leads
      ...

   Quality Metrics:
      Average quality score: 82.3/100
      Average rating: 4.6★
      AI analyzed: 12,456 (100%)
      Leads with AI analysis: 12,456

✅ India database seeding complete!
   Total verified leads: 12,456
   AI analyzed leads: 12,456
```

## Cost Breakdown

### SerpAPI:
- Queries: 1,000
- Cost: ~₹3,000-5,000

### Gemini AI:
- Analyses: ~12,000
- Cost: ~₹2,000-3,000

### Total: ~₹5,000-8,000

**Worth it?** YES!
- 12,000+ verified leads
- 100% AI analyzed
- Ready for production
- Saves months of manual work

## Troubleshooting

### Problem: "SERPAPI_KEY not found"
```bash
# Set in src/config.py
SERPAPI_KEY = 'your-key-here'
```

### Problem: "GEMINI_API_KEY not found"
**Effect:** AI analysis uses fallback (basic templates)
**Solution:** Set key in src/config.py

### Problem: Slow progress
**Normal:** 2-3 seconds per query + 1 second per lead for AI
**Expected:** 4-5 hours for full seeding

### Problem: Some leads missing AI analysis
**Cause:** AI API errors or rate limits
**Solution:** Script continues with fallback analysis

## Next Steps

### After India Seeding:

1. **Verify Data:**
```bash
python3 dashboard_ragspro.py
# Check all cities/categories work
```

2. **Seed Other Countries:**
```bash
# Edit seed_database.py
# Change SEED_CITIES to other countries
python3 seed_database.py
```

3. **Deploy to Production:**
```bash
git add data/premium_leads.json
git commit -m "Add India seeded database"
git push origin main
```

## Production Deployment

### Option 1: Include in Git (if < 50MB)
```bash
git add data/premium_leads.json
git commit -m "Add seeded database"
git push
```

### Option 2: Upload to Cloud Storage
```bash
# Upload to S3/GCS/Azure
# Download on production server
```

### Option 3: Seed on Production
```bash
# Run seeding script on production
# (Uses production API quota)
python3 seed_india_with_ai.py
```

## Success Criteria

✅ Test run completes successfully  
✅ Full seeding completes without errors  
✅ 10,000+ leads in database  
✅ 90%+ leads have AI analysis  
✅ Average quality score > 80  
✅ All cities represented  
✅ All categories represented  
✅ Dashboard shows all leads  
✅ AI Analyze button shows stored data  

**India database is production-ready!** 🇮🇳🚀
