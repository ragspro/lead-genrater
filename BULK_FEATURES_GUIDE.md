# 🚀 RAGSPRO Bulk Features Guide

## ✅ How to Use Bulk Actions

### **Step 1: Select Leads**
1. Open dashboard: http://localhost:5002
2. Check the checkbox on each lead card you want to select
3. OR click "Select All" checkbox at the top

### **Step 2: Use Bulk Actions**
Once leads are selected, you'll see a floating action bar at the bottom with these buttons:

---

## 📊 **Export Features**

### **1. Export to Excel** 📊
- **Button:** "📊 EXPORT EXCEL"
- **What it does:** Downloads selected leads as `.xlsx` file
- **Features:**
  - Professional formatting
  - Color-coded headers
  - Auto-adjusted columns
  - All lead details included

### **2. Export to PDF** 📄
- **Button:** "📄 EXPORT PDF"
- **What it does:** Downloads selected leads as `.pdf` file
- **Features:**
  - Professional report format
  - RAGSPRO branding
  - Table with all details
  - Print-ready

### **3. Export to CSV** 📥
- **Button:** "📥 EXPORT CSV"
- **What it does:** Downloads selected leads as `.csv` file
- **Features:**
  - Compatible with Excel/Google Sheets
  - All lead data
  - Easy to import

---

## 💬 **Communication Features**

### **4. Bulk Email Campaign** 📧
- **Button:** "📧 BULK CAMPAIGN"
- **What it does:** 
  - Generates AI-powered emails for all selected leads
  - Opens email client with pre-filled content
  - Tracks sent status
- **No manual input needed!**

### **5. Bulk WhatsApp** 💬
- **Button:** "💬 WHATSAPP"
- **What it does:**
  - Generates WhatsApp messages for all selected leads
  - Opens WhatsApp Web for each lead
  - AI-personalized messages
- **No manual input needed!**

---

## 🔍 **Research Features**

### **6. LinkedIn Search** 🔗
- **Button:** "🔗 LINKEDIN"
- **What it does:**
  - Automatically searches each business on LinkedIn
  - Opens LinkedIn company search in new tabs
  - Finds decision makers
- **No manual input needed!**

### **7. Website Scanner** 🔍
- **Button:** "🔍 SCAN WEBSITE"
- **What it does:**
  - Analyzes each lead's website
  - Checks SEO score
  - Identifies improvement opportunities
- **No manual input needed!**

---

## 🔥 **Smart Filters**

### **8. Hot Leads** 🔥
- **Button:** "🔥 HOT LEADS"
- **What it does:** Shows only leads with quality score > 85
- **Auto-filtered, no input needed!**

### **9. Today's Leads** 📅
- **Button:** "📅 TODAY"
- **What it does:** Shows only leads generated today
- **Auto-filtered, no input needed!**

### **10. Analytics Dashboard** 📊
- **Button:** "📊 ANALYTICS"
- **What it does:**
  - Shows email/WhatsApp stats
  - Reply rates
  - Conversion metrics
- **Auto-generated, no input needed!**

---

## 🎯 **Example Workflow**

### **Scenario: Export 10 leads to Excel**

1. ✅ Open dashboard
2. ✅ Click checkboxes on 10 leads
3. ✅ Click "📊 EXPORT EXCEL" button
4. ✅ File downloads automatically
5. ✅ Done! No manual work!

### **Scenario: Send WhatsApp to 5 leads**

1. ✅ Select 5 leads
2. ✅ Click "💬 WHATSAPP" button
3. ✅ WhatsApp Web opens with pre-filled messages
4. ✅ Click send on each
5. ✅ Done! AI-generated content!

### **Scenario: Find leads on LinkedIn**

1. ✅ Select leads
2. ✅ Click "🔗 LINKEDIN" button
3. ✅ LinkedIn searches open in new tabs
4. ✅ Browse and connect
5. ✅ Done! Automatic search!

---

## ⚡ **Key Features**

✅ **No Manual Input** - Everything is automatic
✅ **AI-Powered** - Smart content generation
✅ **One-Click Actions** - Select and go
✅ **Real-time Updates** - Instant feedback
✅ **Professional Output** - High-quality exports
✅ **Bulk Processing** - Handle 100s of leads at once

---

## 🔧 **Technical Details**

### **Export Formats:**
- **Excel:** `.xlsx` with formatting
- **PDF:** Professional report with tables
- **CSV:** Plain text, universal format

### **API Endpoints:**
- `POST /api/export/excel` - Excel export
- `POST /api/export/pdf` - PDF export
- `POST /api/export/csv` - CSV export
- `POST /api/bulk/email` - Bulk email
- `POST /api/bulk/whatsapp` - Bulk WhatsApp
- `POST /api/bulk/linkedin` - Bulk LinkedIn

### **Data Sent:**
```json
{
  "lead_ids": [0, 1, 2, 3, 4]
}
```

---

## 📊 **Current Stats**

- **Total Leads:** 529
- **Hot Leads:** 310
- **Avg Quality:** 87.2/100
- **Ready for Export:** ✅

---

**Made with ❤️ by RagsPro Team**
