# 🚀 RAGSPRO - Lead Generation System

**AI-Powered Client Acquisition Dashboard**

---

## ⚡ Quick Start

```bash
# Start the dashboard
python3 dashboard.py

# Or use the script
./START_DASHBOARD.sh
```

**Dashboard URL:** http://localhost:5002

---

## 📊 Current Status

- ✅ **529 Premium Leads** loaded
- ✅ **310 Hot Leads** (quality > 85)
- ✅ **Dark Theme UI** with glassmorphism
- ✅ **Real-time Generation** with progress tracking
- ✅ **AI Content Generation** (Gemini)
- ✅ **WhatsApp & Email** integration
- ✅ **Export to CSV** functionality

---

## 📁 Project Structure

```
lead-genrater/
├── dashboard.py                    # ⭐ Main entry point (USE THIS)
├── dashboard_ragspro.py            # Backend Flask app
├── templates/
│   └── ragspro_dashboard.html      # Dark theme UI
├── src/                            # All Python modules
│   ├── scraper.py                  # SerpAPI scraper
│   ├── ai_gemini.py                # AI content generation
│   ├── lead_quality_filter.py      # Quality scoring
│   ├── filters.py                  # Lead filtering
│   ├── storage.py                  # Data persistence
│   └── ...
├── config/
│   └── settings.json               # API keys & settings
├── data/
│   ├── premium_leads.json          # Main leads database
│   └── history/                    # Date-wise backups
├── tests/                          # Unit tests
└── _archive/                       # Old files (archived)
```

---

## 🎯 Features

### **1. Lead Generation**
- 🌍 Multi-country targeting (USA, UK, UAE, etc.)
- 🏙️ City-specific search
- 💼 289 business categories
- 🎯 Quality threshold (50-100)
- 🤖 Custom AI prompts

### **2. Lead Management**
- 🔍 Real-time search
- 🎛️ Advanced filters (category, city, rating)
- 📊 Export (CSV, Excel, PDF)
- 💬 WhatsApp integration
- 📧 Email integration

### **3. AI Features**
- 📧 Cold email generation
- 💬 WhatsApp message generation
- 📞 Call script generation
- 💡 Solution recommendations
- ⚠️ Pain point analysis

---

## 🔧 Configuration

Edit `config/settings.json`:

```json
{
  "SERPAPI_KEY": "your_key_here",
  "GEMINI_API_KEY": "your_key_here",
  "GMAIL_ADDRESS": "your_email@gmail.com",
  "GMAIL_APP_PASSWORD": "your_app_password",
  "MAX_LEADS_PER_RUN": 10,
  "MIN_RATING": 4.0,
  "MIN_REVIEWS": 20
}
```

---

## 📖 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Dashboard home |
| `/api/stats` | GET | Get statistics |
| `/api/leads` | GET | Get all leads |
| `/api/leads/hot` | GET | Get hot leads |
| `/api/leads/today` | GET | Get today's leads |
| `/api/search?q=` | GET | Search leads |
| `/api/generate` | POST | Start generation |
| `/api/stop` | POST | Stop generation |
| `/api/export/csv` | GET | Export to CSV |
| `/api/send-whatsapp` | POST | Send WhatsApp |
| `/api/send-email` | POST | Send email |

---

## 🧪 Testing

```bash
# Test the dashboard
python3 TEST_RAGSPRO_DASHBOARD.py

# Run unit tests
pytest tests/
```

---

## 📦 Dependencies

```bash
pip install -r requirements.txt
```

**Main packages:**
- Flask 3.0.0
- google-generativeai 0.8.3
- beautifulsoup4 4.12.3
- requests 2.32.5
- serpapi 0.1.5

---

## 🚀 Deployment

### **Local Development**
```bash
python3 dashboard.py
```

### **Production (Gunicorn)**
```bash
gunicorn -w 4 -b 0.0.0.0:5002 dashboard:app
```

### **Docker**
```bash
docker build -t ragspro-dashboard .
docker run -p 5002:5002 ragspro-dashboard
```

---

## 📞 Support

- **Dashboard:** http://localhost:5002
- **Documentation:** See `API_DOCUMENTATION.md`
- **Quick Start:** See `RAGSPRO_QUICK_START.md`

---

## 📝 License

MIT License - See LICENSE file for details

---

**Made with ❤️ by RagsPro Team**
