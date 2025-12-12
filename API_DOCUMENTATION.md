# 📚 API DOCUMENTATION - RAGSPRO LEAD GENERATION SYSTEM

## 🌐 Base URL

```
Local: http://localhost:5001
Production: https://yourdomain.com
```

---

## 🔐 Authentication

Most endpoints require JWT authentication.

### Get Token

```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "role": "user",
    "plan": "pro"
  }
}
```

### Use Token

```http
GET /api/leads
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 📋 ENDPOINTS

### 1. Dashboard

#### GET /
Main dashboard page

**Response:** HTML page

---

### 2. Leads Management

#### GET /api/leads
Get all leads

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `per_page` (optional): Items per page (default: 20)
- `sort` (optional): Sort field (default: created_at)
- `order` (optional): Sort order (asc/desc, default: desc)

**Response:**
```json
{
  "success": true,
  "leads": [
    {
      "id": 1,
      "title": "Tech Solutions Inc",
      "type": "Software Company",
      "address": "123 Main St, New York, NY",
      "city": "New York",
      "rating": 4.8,
      "reviews": 250,
      "phone": "+1234567890",
      "website": "https://example.com",
      "email": "contact@example.com",
      "quality_score": 95,
      "status": "New",
      "created_at": "2025-12-11T10:30:00Z"
    }
  ],
  "total": 472,
  "page": 1,
  "per_page": 20,
  "pages": 24
}
```

#### GET /api/lead/<id>
Get single lead with AI content

**Parameters:**
- `id`: Lead ID (integer)

**Response:**
```json
{
  "success": true,
  "lead": {
    "id": 1,
    "title": "Tech Solutions Inc",
    "type": "Software Company",
    "address": "123 Main St, New York, NY",
    "rating": 4.8,
    "reviews": 250,
    "quality_score": 95,
    "ai_content": {
      "email": "Hi Tech Solutions Inc team...",
      "whatsapp": "Hey! Noticed your business...",
      "call_script": "Hi, this is Raghav from RagsPro..."
    },
    "deep_analysis": {
      "online_presence": {...},
      "pain_points": [...],
      "opportunities": [...],
      "ragspro_solutions": {...}
    }
  }
}
```

#### POST /api/generate
Generate new leads

**Request Body:**
```json
{
  "target_countries": ["USA", "UK", "UAE"],
  "num_leads": 50,
  "quality_threshold": 70,
  "business_types": ["SaaS", "Fintech"],
  "target_cities": ["New York", "London"],
  "ai_prompt": "Custom AI prompt template (optional)"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Lead generation started",
  "job_id": "gen_123456"
}
```

#### POST /api/stop-generation
Stop ongoing generation

**Response:**
```json
{
  "success": true,
  "message": "Generation stopped"
}
```

#### GET /api/status
Get generation status

**Response:**
```json
{
  "success": true,
  "status": {
    "running": true,
    "progress": 45,
    "current_query": "SaaS companies in New York",
    "leads_found": 23,
    "message": "Searching...",
    "latest_leads": [...]
  }
}
```

---

### 3. Statistics & Analytics

#### GET /api/stats
Get dashboard statistics

**Response:**
```json
{
  "success": true,
  "stats": {
    "total_leads": 472,
    "avg_quality": 87.5,
    "avg_rating": 4.69,
    "total_countries": 5,
    "total_categories": 8,
    "last_generation": "2025-12-11T10:30:00Z"
  }
}
```

#### GET /api/analytics/dashboard
Get complete analytics

**Query Parameters:**
- `days` (optional): Time period in days (default: 30)

**Response:**
```json
{
  "success": true,
  "analytics": {
    "total_leads": 472,
    "new_leads_30d": 56,
    "emails_sent": 120,
    "whatsapp_sent": 85,
    "email_replies": 15,
    "email_reply_rate": 12.5,
    "hot_leads": 23,
    "warm_leads": 45
  }
}
```

#### GET /api/analytics/categories
Performance by category

**Response:**
```json
{
  "success": true,
  "categories": [
    {
      "category": "SaaS",
      "total_leads": 120,
      "reply_rate": 15.5,
      "avg_quality": 92.3
    }
  ]
}
```

#### GET /api/analytics/cities
Performance by city

**Response:**
```json
{
  "success": true,
  "cities": [
    {
      "city": "New York",
      "total_leads": 85,
      "reply_rate": 14.2,
      "avg_quality": 90.1
    }
  ]
}
```

---

### 4. Outreach

#### POST /api/send-whatsapp
Send WhatsApp message

**Request Body:**
```json
{
  "lead_id": 1,
  "message": "Custom message (optional)"
}
```

**Response:**
```json
{
  "success": true,
  "message": "WhatsApp message sent",
  "lead_id": 1
}
```

#### POST /api/send-email
Send email

**Request Body:**
```json
{
  "lead_id": 1,
  "subject": "Custom subject (optional)",
  "body": "Custom body (optional)"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Email sent",
  "lead_id": 1
}
```

#### POST /api/bulk-sender/start
Start bulk campaign

**Request Body:**
```json
{
  "lead_ids": [1, 2, 3, 4, 5],
  "subject_template": "Hi {business_name}",
  "body_template": "Dear {business_name} team..."
}
```

**Response:**
```json
{
  "success": true,
  "message": "Bulk campaign started",
  "total": 5
}
```

#### POST /api/bulk-sender/stop
Stop bulk campaign

**Response:**
```json
{
  "success": true,
  "message": "Bulk campaign stopped"
}
```

#### GET /api/bulk-sender/status
Get bulk campaign status

**Response:**
```json
{
  "success": true,
  "status": {
    "active": true,
    "total": 50,
    "sent": 23,
    "failed": 2,
    "current_lead": "Processing Tech Solutions Inc...",
    "logs": [...]
  }
}
```

---

### 5. Follow-ups

#### POST /api/follow-ups/schedule
Schedule follow-up sequence

**Request Body:**
```json
{
  "lead_id": 1,
  "channel": "Email"
}
```

**Response:**
```json
{
  "success": true,
  "follow_ups": [
    {
      "id": 1,
      "sequence_number": 1,
      "scheduled_at": "2025-12-13T10:00:00Z",
      "channel": "Email"
    }
  ]
}
```

#### GET /api/follow-ups/process
Process due follow-ups

**Response:**
```json
{
  "success": true,
  "stats": {
    "sent": 5,
    "failed": 0,
    "skipped": 2
  }
}
```

---

### 6. Reply Classification

#### POST /api/reply/classify
Classify a reply

**Request Body:**
```json
{
  "reply_text": "Yes, I'm interested! Can we schedule a call?",
  "lead_id": 1
}
```

**Response:**
```json
{
  "success": true,
  "classification": {
    "category": "Interested",
    "sentiment": "Positive",
    "priority": "HIGH",
    "action": "Schedule call immediately",
    "confidence": 0.95
  }
}
```

#### POST /api/reply/process
Process reply (classify + generate response)

**Request Body:**
```json
{
  "lead_id": 1,
  "reply_text": "Please send more details",
  "reply_type": "Email"
}
```

**Response:**
```json
{
  "success": true,
  "classification": {...},
  "suggested_response": "Hi there, thanks for your interest...",
  "lead_status": "Replied - SendDetails"
}
```

---

### 7. Recommendations

#### GET /api/recommendations
Get smart recommendations

**Response:**
```json
{
  "success": true,
  "recommendations": {
    "high_conversion_leads": [...],
    "best_categories": [...],
    "best_cities": [...],
    "best_time_to_send": {...},
    "template_recommendations": [...],
    "priority_leads": [...]
  }
}
```

---

### 8. A/B Testing

#### POST /api/ab-test/create
Create A/B test

**Request Body:**
```json
{
  "name": "Subject Line Test",
  "template_a_id": 1,
  "template_b_id": 2,
  "target_size": 100
}
```

**Response:**
```json
{
  "success": true,
  "test_id": 1,
  "name": "Subject Line Test",
  "status": "Active"
}
```

#### GET /api/ab-test/<id>/results
Get test results

**Response:**
```json
{
  "success": true,
  "test_id": 1,
  "variant_a": {
    "sent": 50,
    "replied": 8,
    "reply_rate": 16.0
  },
  "variant_b": {
    "sent": 50,
    "replied": 12,
    "reply_rate": 24.0
  },
  "winner": "Variant B",
  "confidence": "high",
  "recommendation": "Use Variant B - 50% better performance"
}
```

---

### 9. Authentication

#### POST /api/auth/register
Register new user

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "full_name": "John Doe",
  "company_name": "Tech Corp"
}
```

**Response:**
```json
{
  "success": true,
  "user_id": 1,
  "email": "user@example.com"
}
```

#### POST /api/auth/login
Login user

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {...}
}
```

---

### 10. Subscriptions

#### GET /api/subscription/plans
Get subscription plans

**Response:**
```json
{
  "success": true,
  "plans": {
    "free": {
      "name": "Free",
      "price": 0,
      "monthly_leads_limit": 500,
      "features": [...]
    },
    "pro": {
      "name": "Pro",
      "price": 2499,
      "monthly_leads_limit": 10000,
      "features": [...]
    }
  }
}
```

#### POST /api/subscription/upgrade
Upgrade subscription

**Request Body:**
```json
{
  "user_id": 1,
  "new_plan": "pro"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Upgraded to Pro plan",
  "plan": "pro",
  "price": 2499
}
```

---

### 11. Advanced Features

#### POST /api/linkedin/search
Search LinkedIn profiles

**Request Body:**
```json
{
  "keywords": "CEO",
  "location": "New York",
  "limit": 50
}
```

**Response:**
```json
{
  "success": true,
  "profiles": [...]
}
```

#### POST /api/website/scan
Scan website

**Request Body:**
```json
{
  "url": "https://example.com"
}
```

**Response:**
```json
{
  "success": true,
  "analysis": {
    "seo_score": 65,
    "issues": [...],
    "opportunities": [...]
  }
}
```

#### POST /api/multichannel/send
Multi-channel outreach

**Request Body:**
```json
{
  "lead_ids": [1, 2, 3],
  "channels": ["email", "whatsapp"],
  "message": "Hi there..."
}
```

**Response:**
```json
{
  "success": true,
  "results": {
    "total": 3,
    "sent": 3,
    "failed": 0,
    "by_channel": {
      "email": 3,
      "whatsapp": 3
    }
  }
}
```

#### POST /api/proposal/generate
Generate proposal

**Request Body:**
```json
{
  "lead_id": 1,
  "service_type": "web_development"
}
```

**Response:**
```json
{
  "success": true,
  "proposal": "# PROPOSAL FOR TECH SOLUTIONS INC...",
  "service_type": "web_development"
}
```

---

## 🔴 Error Responses

All endpoints return errors in this format:

```json
{
  "success": false,
  "error": "Error message here",
  "code": "ERROR_CODE"
}
```

### Common Error Codes

- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `429` - Too Many Requests
- `500` - Internal Server Error

---

## 📊 Rate Limits

- **Free Plan:** 100 requests/hour
- **Starter Plan:** 500 requests/hour
- **Pro Plan:** 2000 requests/hour
- **Agency Plan:** Unlimited

---

## 🔧 SDKs & Libraries

### Python

```python
import requests

BASE_URL = "http://localhost:5001"
TOKEN = "your_jwt_token"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Get leads
response = requests.get(f"{BASE_URL}/api/leads", headers=headers)
leads = response.json()

# Generate leads
data = {
    "target_countries": ["USA"],
    "num_leads": 50,
    "quality_threshold": 70
}
response = requests.post(f"{BASE_URL}/api/generate", json=data, headers=headers)
```

### JavaScript

```javascript
const BASE_URL = 'http://localhost:5001';
const TOKEN = 'your_jwt_token';

const headers = {
  'Authorization': `Bearer ${TOKEN}`,
  'Content-Type': 'application/json'
};

// Get leads
fetch(`${BASE_URL}/api/leads`, { headers })
  .then(res => res.json())
  .then(data => console.log(data));

// Generate leads
fetch(`${BASE_URL}/api/generate`, {
  method: 'POST',
  headers,
  body: JSON.stringify({
    target_countries: ['USA'],
    num_leads: 50,
    quality_threshold: 70
  })
})
  .then(res => res.json())
  .then(data => console.log(data));
```

---

## 📞 Support

**Raghav Shah**  
📧 ragsproai@gmail.com  
📞 +918700048490  
🌐 ragspro.com

---

**API Version:** 4.0.0  
**Last Updated:** December 11, 2025

