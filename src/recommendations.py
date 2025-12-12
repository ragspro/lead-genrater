"""
Smart Recommendations Engine - LEVEL 2
AI-powered recommendations for best leads, categories, and strategies
"""

import logging
from typing import Dict, List
from datetime import datetime, timedelta
from sqlalchemy import func, and_, or_
from src.database import get_db, Lead, Interaction, LeadAnalytics, Template

logger = logging.getLogger(__name__)


class RecommendationsEngine:
    """Generate smart recommendations based on historical data"""
    
    def __init__(self):
        logger.info("Recommendations engine initialized")
    
    def get_daily_recommendations(self) -> Dict:
        """Get daily recommendations for outreach"""
        session = get_db()
        
        try:
            recommendations = {
                'high_conversion_leads': self._get_high_conversion_leads(session),
                'best_categories': self._get_best_categories(session),
                'best_cities': self._get_best_cities(session),
                'best_time_to_send': self._get_best_send_time(session),
                'template_recommendations': self._get_template_recommendations(session),
                'priority_leads': self._get_priority_leads(session)
            }
            
            return recommendations
            
        finally:
            session.close()
    
    def _get_high_conversion_leads(self, session) -> List[Dict]:
        """Find leads most likely to convert"""
        # Get leads with high engagement but not yet contacted
        leads = session.query(Lead).join(LeadAnalytics).filter(
            and_(
                Lead.quality_score >= 80,
                Lead.email_sent == False,
                or_(
                    LeadAnalytics.conversion_probability >= 0.7,
                    Lead.rating >= 4.5
                )
            )
        ).order_by(
            LeadAnalytics.conversion_probability.desc()
        ).limit(10).all()
        
        result = []
        for lead in leads:
            result.append({
                'id': lead.id,
                'title': lead.title,
                'city': lead.city,
                'quality_score': lead.quality_score,
                'rating': lead.rating,
                'conversion_probability': lead.analytics.conversion_probability if lead.analytics else 0,
                'reason': self._get_recommendation_reason(lead)
            })
        
        return result
    
    def _get_recommendation_reason(self, lead: Lead) -> str:
        """Generate reason for recommendation"""
        reasons = []
        
        if lead.quality_score >= 90:
            reasons.append("Excellent quality score")
        if lead.rating >= 4.5:
            reasons.append("High customer rating")
        if lead.reviews >= 100:
            reasons.append("Many reviews (established business)")
        if not lead.website:
            reasons.append("No website (opportunity!)")
        
        return " • ".join(reasons) if reasons else "Good potential"
    
    def _get_best_categories(self, session) -> List[Dict]:
        """Find categories with best performance"""
        # Calculate reply rate by category
        from sqlalchemy import Integer
        results = session.query(
            Lead.search_category,
            func.count(Lead.id).label('total'),
            func.sum(func.cast(Lead.email_sent, Integer)).label('sent'),
            func.sum(func.cast(Lead.email_replied, Integer)).label('replied'),
            func.avg(Lead.quality_score).label('avg_quality')
        ).filter(
            Lead.search_category.isnot(None),
            Lead.email_sent == True
        ).group_by(
            Lead.search_category
        ).having(
            func.count(Lead.id) >= 5  # At least 5 leads
        ).all()
        
        categories = []
        for row in results:
            reply_rate = (row.replied / row.sent * 100) if row.sent > 0 else 0
            categories.append({
                'category': row.search_category,
                'total_leads': row.total,
                'reply_rate': round(reply_rate, 1),
                'avg_quality': round(row.avg_quality or 0, 1),
                'score': round(reply_rate * (row.avg_quality or 0) / 100, 1)
            })
        
        # Sort by score (reply_rate * quality)
        categories.sort(key=lambda x: x['score'], reverse=True)
        return categories[:5]
    
    def _get_best_cities(self, session) -> List[Dict]:
        """Find cities with best performance"""
        from sqlalchemy import Integer
        results = session.query(
            Lead.search_city,
            func.count(Lead.id).label('total'),
            func.sum(func.cast(Lead.email_sent, Integer)).label('sent'),
            func.sum(func.cast(Lead.email_replied, Integer)).label('replied'),
            func.avg(Lead.quality_score).label('avg_quality')
        ).filter(
            Lead.search_city.isnot(None),
            Lead.email_sent == True
        ).group_by(
            Lead.search_city
        ).having(
            func.count(Lead.id) >= 3
        ).all()
        
        cities = []
        for row in results:
            reply_rate = (row.replied / row.sent * 100) if row.sent > 0 else 0
            cities.append({
                'city': row.search_city,
                'total_leads': row.total,
                'reply_rate': round(reply_rate, 1),
                'avg_quality': round(row.avg_quality or 0, 1),
                'score': round(reply_rate * (row.avg_quality or 0) / 100, 1)
            })
        
        cities.sort(key=lambda x: x['score'], reverse=True)
        return cities[:5]
    
    def _get_best_send_time(self, session) -> Dict:
        """Analyze best time to send emails"""
        # Get interactions with timestamps
        interactions = session.query(Interaction).filter(
            Interaction.type == 'Email',
            Interaction.direction == 'Outbound',
            Interaction.replied == True
        ).all()
        
        if not interactions:
            return {
                'best_hour': 9,
                'best_day': 'Tuesday',
                'confidence': 'low',
                'reason': 'Not enough data yet'
            }
        
        # Analyze by hour
        hour_stats = {}
        for interaction in interactions:
            hour = interaction.created_at.hour
            hour_stats[hour] = hour_stats.get(hour, 0) + 1
        
        best_hour = max(hour_stats, key=hour_stats.get) if hour_stats else 9
        
        # Analyze by day
        day_stats = {}
        for interaction in interactions:
            day = interaction.created_at.strftime('%A')
            day_stats[day] = day_stats.get(day, 0) + 1
        
        best_day = max(day_stats, key=day_stats.get) if day_stats else 'Tuesday'
        
        return {
            'best_hour': best_hour,
            'best_day': best_day,
            'confidence': 'high' if len(interactions) >= 20 else 'medium',
            'reason': f'Based on {len(interactions)} successful replies'
        }
    
    def _get_template_recommendations(self, session) -> List[Dict]:
        """Recommend best performing templates"""
        templates = session.query(Template).filter(
            Template.is_active == True,
            Template.times_used >= 5
        ).order_by(
            Template.reply_rate.desc()
        ).limit(3).all()
        
        result = []
        for template in templates:
            result.append({
                'id': template.id,
                'name': template.name,
                'type': template.type,
                'reply_rate': round(template.reply_rate * 100, 1),
                'times_used': template.times_used,
                'recommendation': 'Use this template' if template.reply_rate > 0.15 else 'Consider A/B testing'
            })
        
        return result
    
    def _get_priority_leads(self, session) -> List[Dict]:
        """Get leads that need immediate attention"""
        # Leads that replied but not followed up
        replied_leads = session.query(Lead).filter(
            Lead.email_replied == True,
            Lead.last_contacted < datetime.utcnow() - timedelta(days=2)
        ).order_by(Lead.last_contacted.asc()).limit(5).all()
        
        # Hot leads not contacted recently
        hot_leads = session.query(Lead).join(LeadAnalytics).filter(
            LeadAnalytics.is_hot_lead == True,
            or_(
                Lead.last_contacted.is_(None),
                Lead.last_contacted < datetime.utcnow() - timedelta(days=3)
            )
        ).limit(5).all()
        
        priority = []
        
        for lead in replied_leads:
            priority.append({
                'id': lead.id,
                'title': lead.title,
                'priority': 'URGENT',
                'reason': 'Replied but not followed up',
                'days_ago': (datetime.utcnow() - lead.last_contacted).days if lead.last_contacted else 0
            })
        
        for lead in hot_leads:
            priority.append({
                'id': lead.id,
                'title': lead.title,
                'priority': 'HIGH',
                'reason': 'Hot lead needs attention',
                'days_ago': (datetime.utcnow() - lead.last_contacted).days if lead.last_contacted else 999
            })
        
        return priority
    
    def get_lead_score(self, lead_id: int) -> Dict:
        """Calculate detailed score for a lead"""
        session = get_db()
        
        try:
            lead = session.query(Lead).get(lead_id)
            if not lead:
                return {'error': 'Lead not found'}
            
            # Calculate various scores
            quality_score = lead.quality_score or 0
            rating_score = (lead.rating / 5.0 * 100) if lead.rating else 0
            reviews_score = min((lead.reviews or 0) / 100 * 100, 100)
            
            # Engagement score
            engagement_score = 0
            if lead.analytics:
                engagement_score = lead.analytics.engagement_score
            
            # Calculate final score
            final_score = (
                quality_score * 0.3 +
                rating_score * 0.2 +
                reviews_score * 0.2 +
                engagement_score * 0.3
            )
            
            return {
                'lead_id': lead_id,
                'lead_name': lead.title,
                'final_score': round(final_score, 1),
                'breakdown': {
                    'quality': quality_score,
                    'rating': round(rating_score, 1),
                    'reviews': round(reviews_score, 1),
                    'engagement': engagement_score
                },
                'recommendation': self._get_action_recommendation(final_score),
                'priority': 'HIGH' if final_score >= 80 else 'MEDIUM' if final_score >= 60 else 'LOW'
            }
            
        finally:
            session.close()
    
    def _get_action_recommendation(self, score: float) -> str:
        """Get action recommendation based on score"""
        if score >= 85:
            return "Contact immediately - High conversion potential"
        elif score >= 70:
            return "Contact soon - Good potential"
        elif score >= 50:
            return "Add to nurture campaign"
        else:
            return "Low priority - Consider later"


def create_recommendations_engine():
    """Create recommendations engine instance"""
    return RecommendationsEngine()


if __name__ == '__main__':
    # Test recommendations
    from src.database import init_database
    
    print("Initializing...")
    init_database()
    
    engine = create_recommendations_engine()
    
    print("\n📊 Daily Recommendations:")
    recommendations = engine.get_daily_recommendations()
    
    print(f"\n🎯 High Conversion Leads: {len(recommendations['high_conversion_leads'])}")
    for lead in recommendations['high_conversion_leads'][:3]:
        print(f"  • {lead['title']} - Score: {lead['quality_score']}")
    
    print(f"\n📈 Best Categories:")
    for cat in recommendations['best_categories']:
        print(f"  • {cat['category']}: {cat['reply_rate']}% reply rate")
    
    print(f"\n🌍 Best Cities:")
    for city in recommendations['best_cities']:
        print(f"  • {city['city']}: {city['reply_rate']}% reply rate")
    
    print(f"\n⏰ Best Send Time:")
    time_rec = recommendations['best_time_to_send']
    print(f"  • {time_rec['best_day']} at {time_rec['best_hour']}:00")
    print(f"  • Confidence: {time_rec['confidence']}")
