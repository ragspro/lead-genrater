# 🚀 RagsPro Lead Generation Bot - Complete Setup

## ✅ System Status: FULLY WORKING

Your lead generation bot is now configured with **real RagsPro.com services** and ready to use!

---

## 📋 What's Configured

### 1. **Real Data Scraping** ✅
- Using SerpAPI for real Google Maps business data
- No fake/demo data
- API Key: Configured in `config/settings.json`

### 2. **AI Content Generation** ✅
- Using Google Gemini AI (FREE tier)
- Personalized emails and WhatsApp messages
- **Updated with RagsPro.com services:**
  - Mobile Apps (iOS/Android)
  - Web Applications & SaaS
  - E-commerce Solutions
  - UX/UI Design & Branding
  - AI Integration
  - Landing Pages
  - 3D Design
  - SEO & Digital Marketing

### 3. **RagsPro Contact Info** ✅
All generated content includes:
- **Name:** Raghav Shah
- **Company:** RagsPro.com
- **Location:** Delhi, India
- **Phone:** +918700048490
- **Email:** raghav@ragspro.com
- **Website:** ragspro.com
- **Portfolio:** LawAI, Glow, HimShakti

### 4. **Web Dashboard** ✅
- Modern Flask-based interface
- Real-time lead management
- Running on: **http://localhost:8080**

---

## 🎯 How to Use

### Option 1: Quick Test (Recommended First)
```bash
python test_real_quick.py
```
This will:
- Scrape 2 sample queries
- Find 5-10 qualified leads
- Save to `data/all_leads.csv`
- Show you sample data

### Option 2: Web Dashboard
```bash
python dashboard.py
```
Then open: **http://localhost:8080**

Features:
- View all leads in beautiful interface
- Search and filter leads
- Generate new leads with one click
- See statistics and analytics

### Option 3: Full Automation
```bash
python AUTO_OUTREACH.py
```
This will:
- Scrape leads from your queries
- Generate AI content for each lead
- Save everything to CSV
- Create outreach files

---

## 📁 Important Files

### Configuration
- `config/settings.json` - All API keys and settings

### Source Code
- `src/scraper.py` - Real data scraper (SerpAPI)
- `src/ai_gemini.py` - AI content generation (Updated with RagsPro services)
- `src/email_sender.py` - Email automation
- `dashboard.py` - Web interface

### Data
- `data/all_leads.csv` - All scraped leads
- `data/outreach_*.txt` - Generated outreach content

### Tests
- `test_real_quick.py` - Quick test with real data
- `test_ai_content.py` - Test AI content generation

---

## 🔑 API Keys Needed

### Already Configured ✅
1. **SerpAPI Key** - For real Google Maps data
2. **Gemini API Key** - For AI content generation
3. **Gmail Credentials** - For email sending

### Optional (Not Required)
- WhatsApp API - For automated WhatsApp messages
- Google Sheets API - For syncing leads

---

## 💡 What AI Generates

### Email Example:
```
Hi,

I noticed [Business Name] has an excellent reputation with 4.9 stars and 69 reviews!

I'm Raghav Shah from RagsPro.com - we're a development agency based in Delhi specializing in:
• Mobile Apps (iOS/Android)
• Web Applications & SaaS
• E-commerce Solutions
• UX/UI Design & Branding
• AI Integration

We've built successful products like LawAI (legal tech), Glow (AI photo editor), 
and HimShakti (e-commerce platform). 200+ projects delivered for 50+ happy clients.

For [Business Type] businesses like yours, we can create solutions that help you 
reach more customers and grow revenue.

Would you be interested in a FREE consultation? I can show you our portfolio 
and discuss how we can help.

Best regards,
Raghav Shah
RagsPro.com | +918700048490 | raghav@ragspro.com
```

### WhatsApp Example:
```
Hey! 👋 Raghav from RagsPro.com (Delhi)

Saw [Business Name] on Google - great business! 🌟

We build mobile apps, websites, SaaS for [Business Type] businesses. 
Built LawAI, Glow, HimShakti - 200+ projects delivered! 💻

Want to grow online? FREE consultation! ✅

Reply YES or call +918700048490 🚀
```

---

## 🎨 RagsPro Services in Pitches

The AI automatically suggests relevant services based on business type:

| Business Type | Suggested Services |
|--------------|-------------------|
| Restaurants/Cafes | Mobile App for orders + Website |
| Retail/Shops | E-commerce + Brand Design |
| Services | Professional Website + SEO |
| Healthcare | Web App + Patient Portal |
| Education | Learning Platform + Mobile App |
| Salons/Spas | Booking System + Mobile App |
| Real Estate | Property Portal + CRM |

---

## 📊 Dashboard Features

### Main Dashboard (http://localhost:8080)
- **Total Leads:** See all scraped leads
- **Search:** Filter by name, city, category
- **Statistics:** Average rating, top cities, status breakdown
- **Generate:** One-click lead generation
- **Export:** Download leads as CSV

### Lead Details
Each lead shows:
- Business name and category
- Rating and review count
- Phone number and address
- Google Maps place ID
- Status (New/Contacted/Qualified)

---

## 🔧 Customization

### Change Search Queries
Edit `src/config.py`:
```python
SEARCH_QUERIES = [
    "restaurants in Delhi",
    "cafes in Mumbai",
    "salons in Bangalore"
]
```

### Adjust Lead Filters
Edit `config/settings.json`:
```json
{
  "MIN_RATING": 4.0,
  "MIN_REVIEWS": 20,
  "MAX_LEADS_PER_RUN": 50
}
```

### Modify AI Prompts
Edit `src/ai_gemini.py` to customize:
- Email tone and style
- WhatsApp message format
- Service suggestions
- Call-to-action

---

## 🚨 Troubleshooting

### Dashboard Not Loading?
```bash
# Check if port 8080 is free
lsof -i :8080

# Use different port
python dashboard.py --port 8081
```

### No Leads Found?
- Check SerpAPI key in `config/settings.json`
- Verify search queries in `src/config.py`
- Lower MIN_RATING and MIN_REVIEWS filters

### AI Content Not Generating?
- Check Gemini API key
- Verify internet connection
- Fallback templates will be used automatically

### Email Not Sending?
- Verify Gmail credentials
- Enable "Less secure app access" in Gmail
- Use App Password instead of regular password

---

## 📈 Next Steps

### 1. Test Everything
```bash
# Test data scraping
python test_real_quick.py

# Test AI content
python test_ai_content.py

# Test dashboard
python dashboard.py
```

### 2. Generate Real Leads
```bash
# Run full automation
python AUTO_OUTREACH.py
```

### 3. Review Generated Content
- Check `data/outreach_*.txt` files
- Review AI-generated emails and messages
- Customize if needed

### 4. Start Outreach
- Use generated content to contact leads
- Track responses in dashboard
- Update lead status

---

## 💰 Cost Breakdown

### Current Setup (FREE/Low Cost)
- **SerpAPI:** $50/month (1000 searches)
- **Gemini AI:** FREE (60 requests/minute)
- **Gmail:** FREE
- **Dashboard:** FREE (local hosting)

### Total: ~$50/month for 1000 leads

---

## 🎯 Success Metrics

Track these in your dashboard:
- **Leads Generated:** Total businesses scraped
- **Qualified Leads:** Businesses meeting criteria
- **Response Rate:** % of leads that respond
- **Conversion Rate:** % that become clients
- **ROI:** Revenue vs. cost

---

## 📞 Support

### Need Help?
- Check documentation in project files
- Review error logs in console
- Test individual components first

### Want to Customize?
- All code is well-commented
- Modify prompts in `src/ai_gemini.py`
- Adjust filters in `config/settings.json`
- Customize dashboard in `templates/dashboard.html`

---

## ✅ Final Checklist

- [x] SerpAPI configured for real data
- [x] Gemini AI configured for content generation
- [x] RagsPro services added to AI prompts
- [x] Contact info (phone, email, website) included
- [x] Dashboard running on localhost:8080
- [x] Test scripts working
- [x] Sample leads generated
- [x] AI content tested

---

## 🚀 You're Ready!

Your lead generation bot is fully configured with:
✅ Real business data from Google Maps
✅ AI-powered personalized content
✅ RagsPro.com services and portfolio
✅ Professional contact information
✅ Modern web dashboard

**Start generating leads now:**
```bash
python dashboard.py
# Open http://localhost:8080
```

---

**Built for RagsPro.com**
*Raghav Shah | Delhi, India | +918700048490*
