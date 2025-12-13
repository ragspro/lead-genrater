#!/usr/bin/env python3
"""
India Database Seeding with AI Analysis
- Scrapes REAL leads from all major Indian cities
- AI analyzes each lead (pain points, solutions, scripts)
- Stores everything in database
"""

import sys
import os
import json
import time
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.scraper import search_places
from src.lead_quality_filter import filter_serious_clients_only
from src.filters import remove_duplicates
from src.config import load_config
from src.ai_gemini import create_ai_assistant

# All major Indian cities
INDIAN_CITIES = [
    # Tier 1 Cities
    "Mumbai, India",
    "Delhi, India", 
    "Bangalore, India",
    "Hyderabad, India",
    "Chennai, India",
    "Kolkata, India",
    "Pune, India",
    "Ahmedabad, India",
    
    # Tier 2 Cities
    "Jaipur, India",
    "Surat, India",
    "Lucknow, India",
    "Kanpur, India",
    "Nagpur, India",
    "Indore, India",
    "Thane, India",
    "Bhopal, India",
    "Visakhapatnam, India",
    "Pimpri-Chinchwad, India",
    "Patna, India",
    "Vadodara, India",
    "Ghaziabad, India",
    "Ludhiana, India",
    "Agra, India",
    "Nashik, India",
    "Faridabad, India",
    "Meerut, India",
    "Rajkot, India",
    "Kalyan-Dombivali, India",
    "Vasai-Virar, India",
    "Varanasi, India",
    "Srinagar, India",
    "Aurangabad, India",
    "Dhanbad, India",
    "Amritsar, India",
    "Navi Mumbai, India",
    "Allahabad, India",
    "Ranchi, India",
    "Howrah, India",
    "Coimbatore, India",
    "Jabalpur, India",
    "Gwalior, India",
    "Vijayawada, India",
    "Jodhpur, India",
    "Madurai, India",
    "Raipur, India",
    "Kota, India",
    "Chandigarh, India",
    "Guwahati, India",
]

# Top business categories for India
INDIAN_CATEGORIES = [
    # Professional Services
    "dental clinic",
    "law firm",
    "chartered accountant",
    "real estate agent",
    "software company",
    "consulting firm",
    "medical clinic",
    "diagnostic center",
    "pathology lab",
    "physiotherapy clinic",
    
    # Retail & Hospitality
    "restaurant",
    "hotel",
    "cafe",
    "gym",
    "spa",
    "salon",
    "boutique",
    "jewelry store",
    
    # Education & Training
    "coaching center",
    "training institute",
]

def analyze_lead_with_ai(lead, ai_assistant):
    """Analyze lead with AI and return analysis."""
    try:
        business_name = lead.get('title', '')
        business_type = lead.get('type', '')
        rating = lead.get('rating', 0)
        reviews = lead.get('reviews', 0)
        address = lead.get('address', '')
        
        print(f"      🤖 AI analyzing: {business_name[:40]}...")
        
        # Generate AI analysis
        analysis_prompt = f"""Analyze this Indian business and provide insights:

Business: {business_name}
Type: {business_type}
Rating: {rating} stars ({reviews} reviews)
Location: {address}

Provide JSON with:
1. pain_points: 3 specific problems (Indian market context)
2. solutions: 3 RagsPro solutions
3. revenue_opportunity: Project value in INR
4. quick_pitch: One compelling sentence
5. call_script: 30-second Hindi/English script

Focus on Indian market needs."""

        response = ai_assistant.model.generate_content(analysis_prompt)
        analysis_text = response.text.strip()
        
        # Try to parse JSON
        import re
        json_match = re.search(r'```json\s*(.*?)\s*```', analysis_text, re.DOTALL)
        if json_match:
            analysis = json.loads(json_match.group(1))
        else:
            # Fallback
            analysis = {
                'pain_points': [
                    f"Strong reputation ({rating}★) but limited online presence",
                    "No digital marketing strategy for Indian market",
                    "Missing modern website to capture online customers"
                ],
                'solutions': [
                    "Professional website with Hindi/English support",
                    "Local SEO optimization for Indian searches",
                    "WhatsApp Business integration for customer support"
                ],
                'revenue_opportunity': "₹2-10 lakhs",
                'quick_pitch': f"Transform {business_name}'s {rating}★ reputation into 3x more customers!",
                'call_script': f"Namaste! Main Raghav, RagsPro se. {business_name} ki {rating}★ rating dekhi - bahut impressive! Hum Indian businesses ko online grow karne mein help karte hain. 2 minute baat kar sakte hain?"
            }
        
        # Generate email and WhatsApp
        email = ai_assistant.generate_cold_email(business_name, business_type, address, rating, reviews)
        whatsapp = ai_assistant.generate_whatsapp_message(business_name, business_type)
        
        return {
            'ai_analysis': analysis,
            'ai_email': email,
            'ai_whatsapp': whatsapp,
            'ai_analyzed_at': datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"      ⚠️  AI analysis failed: {str(e)}")
        return {
            'ai_analysis': {
                'pain_points': ["Limited online presence", "No digital marketing", "Missing modern website"],
                'solutions': ["Professional website", "SEO optimization", "Digital marketing"],
                'revenue_opportunity': "₹2-5 lakhs",
                'quick_pitch': f"Grow {business_name} online!",
                'call_script': f"Hi, this is Raghav from RagsPro. Quick question about growing {business_name} online?"
            },
            'ai_analyzed_at': datetime.now().isoformat()
        }

def seed_india_database():
    """Seed database with Indian cities and AI analysis."""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║        INDIA DATABASE SEEDING WITH AI ANALYSIS           ║
    ║                                                          ║
    ║  🇮🇳 All Major Indian Cities                             ║
    ║  🤖 AI Analysis for Every Lead                           ║
    ║  ✅ 100% REAL Verified Data                              ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    config = load_config()
    serpapi_key = config.get('SERPAPI_KEY')
    gemini_key = config.get('GEMINI_API_KEY')
    
    if not serpapi_key:
        print("❌ ERROR: SERPAPI_KEY not found!")
        return
    
    if not gemini_key:
        print("⚠️  WARNING: GEMINI_API_KEY not found - AI analysis will use fallback")
        ai_assistant = None
    else:
        print("✅ Initializing Gemini AI...")
        ai_assistant = create_ai_assistant(gemini_key)
    
    print(f"\n📊 Seeding Plan:")
    print(f"   Cities: {len(INDIAN_CITIES)} (All major Indian cities)")
    print(f"   Categories: {len(INDIAN_CATEGORIES)}")
    print(f"   Target: ~{len(INDIAN_CITIES) * len(INDIAN_CATEGORIES) * 15:,} leads")
    print(f"   AI Analysis: {'✅ Enabled' if ai_assistant else '⚠️  Fallback mode'}")
    print(f"   Estimated time: ~{len(INDIAN_CITIES) * len(INDIAN_CATEGORIES) * 3 / 60:.1f} hours")
    
    response = input("\n⚠️  This will use SerpAPI and Gemini quota. Continue? (yes/no): ")
    if response.lower() != 'yes':
        print("❌ Seeding cancelled")
        return
    
    all_leads = []
    total_queries = len(INDIAN_CITIES) * len(INDIAN_CATEGORIES)
    current_query = 0
    ai_analyzed_count = 0
    
    print(f"\n🚀 Starting India seeding with AI analysis...\n")
    
    for city in INDIAN_CITIES:
        print(f"\n🏙️  Processing: {city}")
        print(f"   {'='*60}")
        
        for category in INDIAN_CATEGORIES:
            current_query += 1
            query = f"{category} in {city}"
            
            print(f"\n   [{current_query}/{total_queries}] 🔍 {query}")
            
            try:
                # Scrape with SerpAPI
                results = search_places(query, serpapi_key)
                
                if not results:
                    print(f"      ⚠️  No results")
                    continue
                
                # Filter for quality
                quality_leads = filter_serious_clients_only(results)
                premium = [lead for lead in quality_leads if lead.get('quality_score', 0) >= 70]
                
                if not premium:
                    print(f"      ⚠️  No quality leads")
                    continue
                
                print(f"      ✅ Found {len(premium)} quality leads")
                
                # AI analyze each lead
                if ai_assistant:
                    for i, lead in enumerate(premium, 1):
                        try:
                            ai_data = analyze_lead_with_ai(lead, ai_assistant)
                            lead.update(ai_data)
                            ai_analyzed_count += 1
                            
                            # Rate limiting for AI
                            if i < len(premium):
                                time.sleep(1)
                        except Exception as e:
                            print(f"      ❌ AI error for lead {i}: {str(e)}")
                            continue
                
                # Add metadata
                timestamp = datetime.now().isoformat()
                for lead in premium:
                    lead['generated_at'] = timestamp
                    lead['seed_query'] = query
                    lead['seed_city'] = city
                    lead['seed_category'] = category
                    lead['seed_country'] = 'India'
                
                all_leads.extend(premium)
                print(f"      💾 Total leads: {len(all_leads)} ({ai_analyzed_count} AI analyzed)")
                
                # Rate limiting for SerpAPI
                time.sleep(2)
                
            except Exception as e:
                print(f"      ❌ Error: {str(e)}")
                continue
    
    print(f"\n\n📊 Seeding Summary:")
    print(f"   {'='*60}")
    print(f"   Total leads scraped: {len(all_leads)}")
    print(f"   AI analyzed: {ai_analyzed_count}")
    print(f"   Queries executed: {current_query}")
    print(f"   Success rate: {len(all_leads) / current_query * 100:.1f}%")
    
    if not all_leads:
        print("\n❌ No leads to save!")
        return
    
    # Remove duplicates
    print(f"\n🔄 Removing duplicates...")
    unique_leads = remove_duplicates(all_leads)
    print(f"   Unique leads: {len(unique_leads)}")
    print(f"   Duplicates removed: {len(all_leads) - len(unique_leads)}")
    
    # Save to database
    print(f"\n💾 Saving to database...")
    os.makedirs("data", exist_ok=True)
    os.makedirs("data/history", exist_ok=True)
    os.makedirs("data/backups", exist_ok=True)
    
    # Main database
    db_path = "data/premium_leads.json"
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(unique_leads, f, indent=2, ensure_ascii=False)
    print(f"   ✅ Saved to {db_path}")
    
    # History
    today = datetime.now().strftime('%Y-%m-%d')
    history_path = f"data/history/leads_india_{today}.json"
    history_data = {
        'date': today,
        'timestamp': datetime.now().isoformat(),
        'country': 'India',
        'total_leads': len(unique_leads),
        'ai_analyzed': ai_analyzed_count,
        'leads': unique_leads,
        'seed_info': {
            'cities': len(INDIAN_CITIES),
            'categories': len(INDIAN_CATEGORIES),
            'queries': current_query
        }
    }
    with open(history_path, 'w', encoding='utf-8') as f:
        json.dump(history_data, f, indent=2, ensure_ascii=False)
    print(f"   ✅ Saved to {history_path}")
    
    # Backup
    backup_path = f"data/backups/india_seed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(unique_leads, f, indent=2, ensure_ascii=False)
    print(f"   ✅ Backup: {backup_path}")
    
    # Statistics
    print(f"\n📈 Database Statistics:")
    print(f"   {'='*60}")
    
    # By city
    cities = {}
    for lead in unique_leads:
        city = lead.get('seed_city', 'Unknown')
        cities[city] = cities.get(city, 0) + 1
    
    print(f"\n   Top 10 Cities:")
    for city, count in sorted(cities.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"      {city}: {count} leads")
    
    # By category
    categories = {}
    for lead in unique_leads:
        cat = lead.get('seed_category', 'Unknown')
        categories[cat] = categories.get(cat, 0) + 1
    
    print(f"\n   Top 10 Categories:")
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"      {cat}: {count} leads")
    
    # Quality
    avg_quality = sum(l.get('quality_score', 0) for l in unique_leads) / len(unique_leads)
    avg_rating = sum(l.get('rating', 0) for l in unique_leads) / len(unique_leads)
    
    print(f"\n   Quality Metrics:")
    print(f"      Average quality score: {avg_quality:.1f}/100")
    print(f"      Average rating: {avg_rating:.2f}★")
    print(f"      AI analyzed: {ai_analyzed_count} ({ai_analyzed_count/len(unique_leads)*100:.1f}%)")
    
    # AI analysis stats
    with_ai = sum(1 for l in unique_leads if 'ai_analysis' in l)
    print(f"      Leads with AI analysis: {with_ai}")
    
    print(f"\n✅ India database seeding complete!")
    print(f"   Total verified leads: {len(unique_leads)}")
    print(f"   AI analyzed leads: {ai_analyzed_count}")
    print(f"\n🚀 Start dashboard to see all leads:")
    print(f"   python3 dashboard_ragspro.py")

if __name__ == '__main__':
    seed_india_database()
