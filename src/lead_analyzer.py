"""
AI Lead Analyzer - Analyze lead problems and suggest RagsPro solutions
"""

import logging
from typing import Dict, List
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import time

logger = logging.getLogger(__name__)


class LeadAnalyzer:
    """Analyze leads and suggest RagsPro solutions"""
    
    def __init__(self, ai_assistant):
        """Initialize with AI assistant"""
        self.ai = ai_assistant
        logger.info("Lead Analyzer initialized")
    
    def analyze_lead(self, lead: Dict) -> Dict:
        """
        Analyze a lead and identify problems + solutions.
        
        Args:
            lead: Lead dictionary with business details
        
        Returns:
            Analysis dictionary with problems and solutions
        """
        business_name = lead.get('title', 'Business')
        business_type = lead.get('type', 'business')
        rating = lead.get('rating', 0)
        reviews = lead.get('reviews', 0)
        website = lead.get('website', '')
        phone = lead.get('phone', '')
        
        # For now, use fallback analysis (fast and reliable)
        # AI analysis can be enabled later when Gemini API is more stable
        logger.info(f"🔍 Analyzing {business_name} with smart fallback")
        return self._get_fallback_analysis(lead)
    
    def _parse_analysis(self, text: str) -> Dict:
        """Parse AI analysis text into structured data"""
        analysis = {
            'problems': [],
            'solutions': [],
            'revenue_opportunity': '',
            'pain_points': []
        }
        
        try:
            # Extract problems
            if 'PROBLEMS:' in text:
                problems_section = text.split('PROBLEMS:')[1].split('RAGSPRO SOLUTIONS:')[0]
                problems = [p.strip() for p in problems_section.split('\n') if p.strip() and p.strip()[0].isdigit()]
                analysis['problems'] = problems[:3]
            
            # Extract solutions
            if 'RAGSPRO SOLUTIONS:' in text:
                solutions_section = text.split('RAGSPRO SOLUTIONS:')[1].split('REVENUE OPPORTUNITY:')[0]
                solutions = [s.strip() for s in solutions_section.split('\n') if s.strip() and s.strip()[0].isdigit()]
                analysis['solutions'] = solutions[:3]
            
            # Extract revenue opportunity
            if 'REVENUE OPPORTUNITY:' in text:
                revenue_section = text.split('REVENUE OPPORTUNITY:')[1].split('PAIN POINTS:')[0]
                analysis['revenue_opportunity'] = revenue_section.strip()
            
            # Extract pain points
            if 'PAIN POINTS:' in text:
                pain_section = text.split('PAIN POINTS:')[1]
                pain_points = [p.strip().lstrip('-').strip() for p in pain_section.split('\n') if p.strip() and '-' in p]
                analysis['pain_points'] = pain_points[:3]
        
        except Exception as e:
            logger.error(f"Parse error: {e}")
        
        return analysis
    
    def _get_fallback_analysis(self, lead: Dict) -> Dict:
        """Fallback analysis when AI fails"""
        business_name = lead.get('title', 'Business')
        business_type = lead.get('type', 'business')
        has_website = bool(lead.get('website'))
        
        problems = []
        solutions = []
        pain_points = []
        
        # Identify problems based on data
        if not has_website:
            problems.append("1. No website - losing 60% of potential customers online")
            solutions.append("1. Modern Website Development - ₹25,000-₹50,000")
            pain_points.append("Missing online presence")
        else:
            problems.append("1. Website may be outdated - not converting visitors")
            solutions.append("1. Website Redesign & Optimization - ₹30,000-₹75,000")
            pain_points.append("Low conversion rate")
        
        problems.append("2. No digital marketing - competitors are capturing market share")
        solutions.append("2. Digital Marketing Package - ₹30,000-₹75,000/month")
        pain_points.append("Limited online visibility")
        
        problems.append("3. Manual processes - wasting time and money")
        solutions.append("3. Business Automation System - ₹50,000-₹1,50,000")
        pain_points.append("Inefficient operations")
        
        # Calculate revenue opportunity
        revenue_opportunity = "₹1,00,000 - ₹3,00,000 (Complete Digital Transformation Package)"
        
        return {
            'problems': problems,
            'solutions': solutions,
            'revenue_opportunity': revenue_opportunity,
            'pain_points': pain_points,
            'analyzed': True,
            'fallback': True
        }
    
    def get_quick_pitch(self, lead: Dict) -> str:
        """Get a quick pitch for the lead"""
        business_name = lead.get('title', 'Business')
        business_type = lead.get('type', 'business')
        has_website = bool(lead.get('website'))
        
        if not has_website:
            return f"🎯 {business_name} needs a website! We can build a modern, high-converting site that brings 3-5x more customers. Quick ROI guaranteed."
        else:
            return f"🎯 {business_name} can grow faster with digital marketing! We help {business_type} businesses get 3-5x more customers through proven strategies."


def create_lead_analyzer(ai_assistant):
    """Factory function to create lead analyzer"""
    return LeadAnalyzer(ai_assistant)


if __name__ == '__main__':
    # Test lead analyzer
    from src.ai_gemini import create_ai_assistant
    from src.config import load_config
    
    config = load_config()
    ai = create_ai_assistant(config['GEMINI_API_KEY'])
    analyzer = create_lead_analyzer(ai)
    
    # Test lead
    test_lead = {
        'title': 'ABC Restaurant',
        'type': 'Restaurant',
        'rating': 4.5,
        'reviews': 250,
        'website': '',
        'phone': '+91-9876543210'
    }
    
    print("Testing Lead Analyzer...")
    analysis = analyzer.analyze_lead(test_lead)
    
    print("\n📊 ANALYSIS:")
    print("\nPROBLEMS:")
    for p in analysis['problems']:
        print(f"  {p}")
    
    print("\nSOLUTIONS:")
    for s in analysis['solutions']:
        print(f"  {s}")
    
    print(f"\nREVENUE: {analysis['revenue_opportunity']}")
    
    print("\nPAIN POINTS:")
    for pp in analysis['pain_points']:
        print(f"  - {pp}")
