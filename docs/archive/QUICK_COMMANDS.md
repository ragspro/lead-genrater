# ⚡ QUICK COMMANDS REFERENCE

## 🚀 Start System

```bash
# Test integration
python test_quick_integration.py

# Start dashboard
python dashboard_premium.py

# Open browser
open http://localhost:5001
```

---

## 📊 API Commands

### Analytics
```bash
# Dashboard stats
curl http://localhost:5001/api/analytics/dashboard

# Category performance
curl http://localhost:5001/api/analytics/categories

# City performance
curl http://localhost:5001/api/analytics/cities
```

### Follow-ups
```bash
# View all follow-ups
curl http://localhost:5001/api/follow-ups

# Schedule follow-up for lead #1
curl -X POST http://localhost:5001/api/follow-ups/schedule \
  -H "Content-Type: application/json" \
  -d '{"lead_id": 1, "channel": "Email"}'

# Process due follow-ups
curl -X POST http://localhost:5001/api/follow-ups/process
```

### Reply Classification
```bash
# View pending replies
curl http://localhost:5001/api/replies

# Classify a reply
curl -X POST http://localhost:5001/api/replies/classify \
  -H "Content-Type: application/json" \
  -d '{
    "lead_id": 1,
    "reply_text": "Yes, interested!",
    "reply_type": "Email"
  }'
```

### Leads
```bash
# Get all leads
curl http://localhost:5001/api/leads

# Get leads from database
curl http://localhost:5001/api/leads/db

# Get hot leads only
curl http://localhost:5001/api/leads/hot

# Get lead stats
curl http://localhost:5001/api/stats
```

### Export
```bash
# Download CSV
curl http://localhost:5001/api/export/csv -o leads.csv

# Download Excel
curl http://localhost:5001/api/export/excel -o leads.xlsx

# Download PDF
curl http://localhost:5001/api/export/pdf -o leads.pdf
```

---

## 🗄️ Database Commands

```bash
# Check database
sqlite3 data/rcas.db "SELECT COUNT(*) FROM leads;"

# View tables
sqlite3 data/rcas.db ".tables"

# View lead sample
sqlite3 data/rcas.db "SELECT title, quality_score, city FROM leads LIMIT 5;"

# Count follow-ups
sqlite3 data/rcas.db "SELECT COUNT(*) FROM follow_ups;"

# View hot leads
sqlite3 data/rcas.db "SELECT l.title FROM leads l JOIN lead_analytics a ON l.id = a.lead_id WHERE a.is_hot_lead = 1;"
```

---

## 🧪 Testing Commands

```bash
# Quick test (recommended)
python test_quick_integration.py

# Full test (with AI - slower)
python test_advanced_features.py

# Test specific module
python -m pytest tests/

# Check diagnostics
python -c "from src.database import init_database; init_database(); print('✅ OK')"
```

---

## 🔄 Maintenance Commands

```bash
# Backup database
cp data/rcas.db data/rcas_backup_$(date +%Y%m%d).db

# Reset database (CAUTION!)
rm data/rcas.db
python dashboard_premium.py  # Will recreate

# Re-migrate JSON data
python -c "from src.database import init_database, migrate_json_to_db; init_database(); print(f'Migrated: {migrate_json_to_db()}')"

# Check disk usage
du -sh data/
```

---

## 📦 Installation Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Upgrade dependencies
pip install --upgrade -r requirements.txt

# Install specific package
pip install sqlalchemy>=2.0.35
```

---

## 🤖 Automation Commands

### Cron Job (Linux/Mac)
```bash
# Edit crontab
crontab -e

# Add daily follow-up processing (9 AM)
0 9 * * * curl -X POST http://localhost:5001/api/follow-ups/process

# Add hourly analytics update
0 * * * * curl http://localhost:5001/api/analytics/dashboard > /dev/null
```

### Python Scheduler
```python
# Create auto_tasks.py
import requests
import schedule
import time

def process_follow_ups():
    r = requests.post('http://localhost:5001/api/follow-ups/process')
    print(f"Follow-ups: {r.json()}")

schedule.every().day.at("09:00").do(process_follow_ups)

while True:
    schedule.run_pending()
    time.sleep(60)
```

Run it:
```bash
python auto_tasks.py
```

---

## 🐛 Troubleshooting Commands

```bash
# Check if dashboard is running
curl http://localhost:5001/api/stats

# Check database connection
python -c "from src.database import get_db; session = get_db(); print(f'✅ Connected'); session.close()"

# View logs
tail -f logs/dashboard.log  # If logging to file

# Check Python version
python --version  # Should be 3.8+

# Check installed packages
pip list | grep -E "sqlalchemy|flask|google-generativeai"

# Test API key
python -c "from src.config import load_config; c = load_config(); print('✅ Config loaded' if c.get('GEMINI_API_KEY') else '❌ No API key')"
```

---

## 📊 Monitoring Commands

```bash
# Watch dashboard logs
watch -n 5 'curl -s http://localhost:5001/api/stats | python -m json.tool'

# Monitor follow-ups
watch -n 60 'curl -s http://localhost:5001/api/follow-ups | python -m json.tool | head -20'

# Check hot leads
watch -n 300 'curl -s http://localhost:5001/api/leads/hot | python -m json.tool'

# System resources
top -p $(pgrep -f dashboard_premium.py)
```

---

## 🚀 Deployment Commands

### Local Development
```bash
python dashboard_premium.py
```

### Production (Gunicorn)
```bash
gunicorn -w 4 -b 0.0.0.0:5001 dashboard_premium:app
```

### Production (with logs)
```bash
gunicorn -w 4 -b 0.0.0.0:5001 \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log \
  dashboard_premium:app
```

### Background Process
```bash
nohup python dashboard_premium.py > logs/dashboard.log 2>&1 &
```

### Stop Background Process
```bash
pkill -f dashboard_premium.py
```

---

## 📈 Performance Commands

```bash
# Database size
ls -lh data/rcas.db

# Count records
sqlite3 data/rcas.db "SELECT 
  (SELECT COUNT(*) FROM leads) as leads,
  (SELECT COUNT(*) FROM follow_ups) as follow_ups,
  (SELECT COUNT(*) FROM interactions) as interactions;"

# Query performance
time sqlite3 data/rcas.db "SELECT * FROM leads WHERE quality_score > 80;"

# Optimize database
sqlite3 data/rcas.db "VACUUM;"
```

---

## 🔐 Security Commands

```bash
# Check file permissions
ls -la data/rcas.db
ls -la config/settings.json

# Secure files
chmod 600 config/settings.json
chmod 644 data/rcas.db

# Check for exposed secrets
grep -r "API_KEY\|PASSWORD" . --exclude-dir=.git --exclude-dir=.venv
```

---

## 📝 Git Commands

```bash
# Status
git status

# Add all changes
git add .

# Commit
git commit -m "✨ Added LEVEL 1 advanced features"

# Push to GitHub
git push origin main

# Create tag
git tag -a v2.0.0 -m "LEVEL 1 Complete"
git push origin v2.0.0
```

---

## 💡 Useful One-Liners

```bash
# Count total leads
curl -s http://localhost:5001/api/stats | python -c "import sys, json; print(json.load(sys.stdin)['stats']['total_leads'])"

# Get reply rate
curl -s http://localhost:5001/api/analytics/dashboard | python -c "import sys, json; print(f\"{json.load(sys.stdin)['stats']['email_reply_rate']}%\")"

# List hot leads
curl -s http://localhost:5001/api/leads/hot | python -c "import sys, json; [print(l['title']) for l in json.load(sys.stdin)['leads']]"

# Export all leads to JSON
curl -s http://localhost:5001/api/leads > all_leads.json

# Count pending follow-ups
curl -s http://localhost:5001/api/follow-ups | python -c "import sys, json; print(len([f for f in json.load(sys.stdin)['follow_ups'] if f['status'] == 'Pending']))"
```

---

## 🎯 Daily Workflow Commands

### Morning Routine
```bash
# 1. Check system
curl http://localhost:5001/api/stats

# 2. Process follow-ups
curl -X POST http://localhost:5001/api/follow-ups/process

# 3. Check hot leads
curl http://localhost:5001/api/leads/hot

# 4. View analytics
curl http://localhost:5001/api/analytics/dashboard
```

### Evening Routine
```bash
# 1. Export today's data
curl http://localhost:5001/api/export/csv -o leads_$(date +%Y%m%d).csv

# 2. Backup database
cp data/rcas.db data/backups/rcas_$(date +%Y%m%d).db

# 3. Check stats
curl http://localhost:5001/api/stats
```

---

## 📞 Support

**Raghav Shah**
- Email: ragsproai@gmail.com
- Phone: +918700048490
- Website: ragspro.com

---

**Save this file for quick reference!** 📌
