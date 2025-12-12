# 📁 RAGSPRO Project Structure

## ✅ Active Files (Use These)

```
lead-genrater/
│
├── 🚀 MAIN ENTRY POINTS
│   ├── dashboard.py                    ⭐ START HERE - Main dashboard
│   ├── dashboard_ragspro.py            Backend Flask application
│   └── START_DASHBOARD.sh              Quick start script
│
├── 📄 TEMPLATES
│   └── templates/
│       └── ragspro_dashboard.html      Dark theme UI (ACTIVE)
│
├── 🐍 SOURCE CODE
│   └── src/
│       ├── scraper.py                  SerpAPI lead scraper
│       ├── ai_gemini.py                AI content generation
│       ├── lead_quality_filter.py      Quality scoring system
│       ├── filters.py                  Lead filtering
│       ├── storage.py                  Data persistence
│       ├── config.py                   Configuration loader
│       ├── queries.py                  Search queries
│       ├── email_sender.py             Email integration
│       ├── whatsapp_sender.py          WhatsApp integration
│       └── ... (other modules)
│
├── ⚙️ CONFIGURATION
│   └── config/
│       └── settings.json               API keys & settings
│
├── 💾 DATA
│   └── data/
│       ├── premium_leads.json          Main database (529 leads)
│       └── history/                    Date-wise backups
│
├── 🧪 TESTS
│   ├── tests/                          Unit tests
│   └── TEST_RAGSPRO_DASHBOARD.py       Dashboard test suite
│
├── 📚 DOCUMENTATION
│   ├── README.md                       Main documentation
│   ├── API_DOCUMENTATION.md            API reference
│   └── RAGSPRO_QUICK_START.md          Quick start guide
│
└── 📦 ARCHIVED (Old Files)
    └── _archive/
        ├── old_dashboards/             Old dashboard versions
        ├── old_tests/                  Old test files
        ├── old_docs/                   Old documentation
        ├── old_scripts/                Old utility scripts
        └── old_templates/              Old HTML templates
```

---

## 🎯 How to Use

### **Start Dashboard**
```bash
python3 dashboard.py
# OR
./START_DASHBOARD.sh
```

### **Access Dashboard**
Open browser: http://localhost:5002

### **Generate Leads**
1. Click "Generate" button
2. Select country, city, business type
3. Set quality threshold
4. Click "Generate"

### **View Leads**
- All leads load automatically
- Use search box to filter
- Click on lead cards for details

### **Export Leads**
- Click "CSV" button to download

---

## 📊 Current Stats

- **Total Leads:** 529
- **Hot Leads:** 310 (quality > 85)
- **Avg Quality:** 87.2/100
- **Avg Rating:** 4.7⭐

---

## 🔧 Configuration

Edit `config/settings.json`:
- SERPAPI_KEY: For lead scraping
- GEMINI_API_KEY: For AI content
- GMAIL credentials: For email sending

---

## 🚫 Don't Use These (Archived)

All files in `_archive/` folder are old versions and should NOT be used.
They are kept for reference only.

---

**Last Updated:** 2025-12-12
**Status:** ✅ Production Ready
