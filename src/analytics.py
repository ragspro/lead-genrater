"""
Analytics Engine - Track performance and generate insights
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List
from sqlalchemy import func
from src.database import get_db, Lead, Interaction, Campaign, Template, LeadAnalytics

logger = logging.getLogger(__name__)


class AnalyticsEngine:
    """Generate analytics and insights"""
    
    def get_dashboard_stats(self, days: int = 30) -> Dict:
        """Get main dashboard statistics"""
        session = get_db()
        
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            # Total leads
            total_leads = session.query(Lead).count()
            new_leads = session.query(Lead).filter(
                Lead.created_at >= cutoff_date
            ).count()
            
            # Outreach stats
            emails_sent = session.query(Lead).filter(
                Lead.email_sent == True
            ).count()
            
            whatsapp_sent = session.query(Lead).filter(
                Lead.whatsapp_sent == True
            ).count()
            
            # Response stats
            email_replies = session.query(Lead).filter(
                Lead.email_replied == True
            ).count()
            
            # Lead temperature
            hot_leads = session.query(LeadAnalytics).filter(
                LeadAnalytics.is_hot_lead == True
            ).count()
            
            warm_leads = session.query(LeadAnalytics).filter(
                LeadAnalytics.is_warm_lead == True
            ).count()
            
            # Calculate rates
            email_reply_rate = (email_replies / emails_sent * 100) if emails_sent > 0 else 0
            
            return {
                'total_leads': total_leads,
                'new_leads_30d': new_leads,
                'emails_sent': emails_sent,
                'whatsapp_sent': whatsapp_sent,
                'email_replies': email_replies,
                'email_reply_rate': round(email_reply_rate, 1),
                'hot_leads': hot_leads,
                'warm_leads': warm_leads,
                'period_days': days
            }
            
        finally:
            session.close()
    
    def get_performance_by_category(self) -> List[Dict]:
        """Get performance metrics by business category"""
        session = get_db()
        
        try:
            results = session.query(
                Lead.search_category,
                func.count(Lead.id).label('total'),
                func.sum(func.cast(Lead.email_sent, Integer)).label('emails_sent'),
                func.sum(func.cast(Lead.email_replied, Integer)).label('replies'),
                func.avg(Lead.quality_score).label('avg_quality')
            ).filter(
                Lead.search_category.isnot(None)
            ).group_by(
                Lead.search_category
            ).all()
            
            categories = []
            for row in results:
                reply_rate = (row.replies / row.emails_sent * 100) if row.emails_sent else 0
                categories.append({
                    'category': row.search_category,
                    'total_leads': row.total,
                    'emails_sent': row.emails_sent or 0,
                    'replies': row.replies or 0,
                    'reply_rate': round(reply_rate, 1),
                    'avg_quality': round(row.avg_quality or 0, 1)
                })
            
            # Sort by reply rate
            categories.sort(key=lambda x: x['reply_rate'], reverse=True)
            return categories
            
        finally:
            session.close()
    
    def get_performance_by_city(self) -> List[Dict]:
        """Get performance metrics by city"""
        session = get_db()
        
        try:
            results = session.query(
                Lead.search_city,
                func.count(Lead.id).label('total'),
                func.sum(func.cast(Lead.email_sent, Integer)).label('emails_sent'),
                func.sum(func.cast(Lead.email_replied, Integer)).label('replies'),
                func.avg(Lead.quality_score).label('avg_quality')
            ).filter(
                Lead.search_city.isnot(None)
            ).group_by(
                Lead.search_city
            ).all()
            
            cities = []
            for row in results:
                reply_rate = (row.replies / row.emails_sent * 100) if row.emails_sent else 0
                cities.append({
                    'city': row.search_city,
                    'total_leads': row.total,
                    'emails_sent': row.emails_sent or 0,
                    'replies': row.replies or 0,
                    'reply_rate': round(reply_rate, 1),
                    'avg_quality': round(row.avg_quality or 0, 1)
                })
            
            # Sort by total leads
            cities.sort(key=lambda x: x['total_leads'], reverse=True)
            return cities
            
        finally:
            session.close()
    
    def get_template_performance(self) -> List[Dict]:
        """Get email template performance"""
        session = get_db()
        
        try:
            templates = session.query(Template).filter(
                Template.is_active == True,
                Template.times_used > 0
            ).all()
            
            performance = []
            for template in templates:
                performance.append({
                    'id': template.id,
                    'name': template.name,
                    'type': template.type,
                    'times_used': template.times_used,
                    'open_rate': round(template.open_rate * 100, 1),
                    'reply_rate': round(template.reply_rate * 100, 1),
                    'conversion_rate': round(template.conversion_rate * 100, 1)
                })
            
            # Sort by reply rate
            performance.sort(key=lambda x: x['reply_rate'], reverse=True)
            return performance
            
        finally:
            session.close()
    
    def get_timeline_data(self, days: int = 30) -> Dict:
        """Get timeline data for charts"""
        session = get_db()
        
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            # Leads created per day
            leads_timeline = session.query(
                func.date(Lead.created_at).label('date'),
                func.count(Lead.id).label('count')
            ).filter(
                Lead.created_at >= cutoff_date
            ).group_by(
                func.date(Lead.created_at)
            ).all()
            
            # Interactions per day
            interactions_timeline = session.query(
                func.date(Interaction.created_at).label('date'),
                func.count(Interaction.id).label('count')
            ).filter(
                Interaction.created_at >= cutoff_date
            ).group_by(
                func.date(Interaction.created_at)
            ).all()
            
            return {
                'leads': [{'date': str(row.date), 'count': row.count} for row in leads_timeline],
                'interactions': [{'date': str(row.date), 'count': row.count} for row in interactions_timeline]
            }
            
        finally:
            session.close()


def create_analytics_engine():
    """Create analytics engine instance"""
    return AnalyticsEngine()


if __name__ == '__main__':
    # Test analytics
    from src.database import init_database
    
    print("Initializing...")
    init_database()
    
    analytics = create_analytics_engine()
    
    print("\nDashboard Stats:")
    stats = analytics.get_dashboard_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\nTop Categories:")
    categories = analytics.get_performance_by_category()
    for cat in categories[:5]:
        print(f"  {cat['category']}: {cat['reply_rate']}% reply rate")
