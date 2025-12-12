"""
Hot Lead Scorer - Identifies high-priority leads
Integrates with existing system
"""

import logging
from datetime import datetime, timedelta
from typing import List, Dict

logger = logging.getLogger(__name__)


class HotLeadScorer:
    """Scores leads to identify hot opportunities"""
    
    def __init__(self):
        self.weights = {
            'quality_score': 0.25,
            'rating': 0.20,
            'reviews': 0.15,
            'no_website': 0.20,
            'recent': 0.10,
            'high_budget': 0.10
        }
        logger.info("Hot Lead Scorer initialized")
    
    def calculate_hot_score(self, lead: Dict) -> int:
        """
        Calculate hot lead score (0-100)
        
        Args:
            lead: Lead dictionary with business data
            
        Returns:
            int: Hot score (0-100)
        """
        score = 0
        
        # 1. Quality Score (25 points)
        quality = lead.get('quality_score', 0)
        if quality >= 95:
            score += 25
        elif quality >= 90:
            score += 20
        elif quality >= 85:
            score += 15
        elif quality >= 80:
            score += 10
        elif quality >= 70:
            score += 5
        
        # 2. Rating (20 points)
        rating = lead.get('rating', 0)
        if rating >= 4.8:
            score += 20
        elif rating >= 4.5:
            score += 15
        elif rating >= 4.0:
            score += 10
        elif rating >= 3.5:
            score += 5
        
        # 3. Reviews (15 points)
        reviews = lead.get('reviews', 0)
        if reviews >= 500:
            score += 15
        elif reviews >= 200:
            score += 12
        elif reviews >= 100:
            score += 10
        elif reviews >= 50:
            score += 7
        elif reviews >= 20:
            score += 5
        
        # 4. No Website = Opportunity (20 points)
        website = lead.get('website', '')
        if not website or website == 'None' or website == '':
            score += 20
        elif 'old' in website.lower() or 'blogspot' in website.lower():
            score += 15  # Outdated website
        
        # 5. Recent Lead (10 points)
        created_at = lead.get('created_at') or lead.get('generated_date')
        if created_at:
            if isinstance(created_at, str):
                try:
                    created_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                except:
                    created_date = datetime.now() - timedelta(days=30)
            else:
                created_date = created_at
            
            days_old = (datetime.now() - created_date).days
            if days_old == 0:
                score += 10  # Added today
            elif days_old <= 3:
                score += 7   # Added this week
            elif days_old <= 7:
                score += 5   # Added last week
        
        # 6. High Budget Potential (10 points)
        # Based on deep analysis if available
        analysis = lead.get('deep_analysis', {})
        if analysis:
            budget = analysis.get('estimated_budget', {})
            if budget.get('tier') == 'High':
                score += 10
            elif budget.get('tier') == 'Medium':
                score += 7
            elif budget.get('tier') == 'Low':
                score += 4
        else:
            # Estimate from quality and rating
            if quality >= 85 and rating >= 4.5:
                score += 10
            elif quality >= 75 and rating >= 4.0:
                score += 7
        
        return min(score, 100)
    
    def identify_hot_leads(self, leads: List[Dict], threshold: int = 70) -> List[Dict]:
        """
        Identify hot leads from a list
        
        Args:
            leads: List of lead dictionaries
            threshold: Minimum score to be considered hot (default: 70)
            
        Returns:
            List of hot leads with scores
        """
        hot_leads = []
        
        for lead in leads:
            score = self.calculate_hot_score(lead)
            
            if score >= threshold:
                lead['hot_score'] = score
                lead['is_hot_lead'] = True
                lead['priority'] = self._get_priority_level(score)
                lead['urgency'] = self._get_urgency_message(score)
                hot_leads.append(lead)
        
        # Sort by score (highest first)
        hot_leads.sort(key=lambda x: x['hot_score'], reverse=True)
        
        logger.info(f"Identified {len(hot_leads)} hot leads from {len(leads)} total")
        return hot_leads
    
    def _get_priority_level(self, score: int) -> str:
        """Get priority level from score"""
        if score >= 90:
            return 'URGENT'
        elif score >= 80:
            return 'HIGH'
        elif score >= 70:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def _get_urgency_message(self, score: int) -> str:
        """Get urgency message from score"""
        if score >= 90:
            return '🔥 Contact immediately! High conversion potential'
        elif score >= 80:
            return '⚡ Contact today! Strong opportunity'
        elif score >= 70:
            return '📞 Contact this week! Good potential'
        else:
            return '📋 Standard follow-up'
    
    def get_hot_lead_reasons(self, lead: Dict) -> List[str]:
        """
        Get reasons why a lead is hot
        
        Args:
            lead: Lead dictionary
            
        Returns:
            List of reason strings
        """
        reasons = []
        
        quality = lead.get('quality_score', 0)
        rating = lead.get('rating', 0)
        reviews = lead.get('reviews', 0)
        website = lead.get('website', '')
        
        if quality >= 90:
            reasons.append(f"✅ Excellent quality score ({quality}/100)")
        
        if rating >= 4.5:
            reasons.append(f"⭐ High rating ({rating}/5)")
        
        if reviews >= 100:
            reasons.append(f"💬 Many reviews ({reviews})")
        
        if not website or website == 'None':
            reasons.append("🌐 No website - High opportunity!")
        
        # Check if added today
        created_at = lead.get('created_at') or lead.get('generated_date')
        if created_at:
            if isinstance(created_at, str):
                try:
                    created_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                    if (datetime.now() - created_date).days == 0:
                        reasons.append("🆕 Added today - Fresh lead!")
                except:
                    pass
        
        # Check deep analysis
        analysis = lead.get('deep_analysis', {})
        if analysis:
            budget = analysis.get('estimated_budget', {})
            if budget.get('tier') == 'High':
                reasons.append(f"💰 High budget potential ({budget.get('range', 'N/A')})")
        
        return reasons


def create_hot_lead_scorer():
    """Factory function to create hot lead scorer"""
    return HotLeadScorer()


# Example usage
if __name__ == '__main__':
    scorer = create_hot_lead_scorer()
    
    # Test lead
    test_lead = {
        'title': 'TechStart Solutions',
        'type': 'Software company',
        'quality_score': 95,
        'rating': 4.8,
        'reviews': 250,
        'website': None,
        'created_at': datetime.now().isoformat()
    }
    
    score = scorer.calculate_hot_score(test_lead)
    print(f"Hot Score: {score}/100")
    
    reasons = scorer.get_hot_lead_reasons(test_lead)
    print("Reasons:")
    for reason in reasons:
        print(f"  - {reason}")
