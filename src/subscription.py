"""
Subscription & Payment System - LEVEL 3
Stripe integration for SaaS monetization
"""

import logging
from datetime import datetime, timedelta
from typing import Dict
from src.database import get_db, User

logger = logging.getLogger(__name__)

# Subscription plans
PLANS = {
    'free': {
        'name': 'Free',
        'price': 0,
        'monthly_leads_limit': 500,
        'monthly_emails_limit': 1000,
        'features': ['Basic scraping', 'Email templates', 'CSV export']
    },
    'starter': {
        'name': 'Starter',
        'price': 999,  # ₹999/month
        'monthly_leads_limit': 2000,
        'monthly_emails_limit': 5000,
        'features': ['Everything in Free', 'Follow-ups', 'Analytics', 'WhatsApp']
    },
    'pro': {
        'name': 'Pro',
        'price': 2499,  # ₹2499/month
        'monthly_leads_limit': 10000,
        'monthly_emails_limit': 25000,
        'features': ['Everything in Starter', 'A/B Testing', 'Smart Recommendations', 'Priority Support']
    },
    'agency': {
        'name': 'Agency',
        'price': 5999,  # ₹5999/month
        'monthly_leads_limit': 50000,
        'monthly_emails_limit': 100000,
        'features': ['Everything in Pro', 'Multi-user', 'White-label', 'API Access', 'Dedicated Support']
    }
}


class SubscriptionManager:
    """Manage subscriptions and payments"""
    
    def __init__(self):
        logger.info("Subscription manager initialized")
    
    def get_plans(self) -> Dict:
        """Get all available plans"""
        return PLANS
    
    def get_user_subscription(self, user_id: int) -> Dict:
        """Get user's current subscription"""
        session = get_db()
        
        try:
            user = session.query(User).get(user_id)
            if not user:
                return {'error': 'User not found'}
            
            plan_info = PLANS.get(user.plan, PLANS['free'])
            
            return {
                'success': True,
                'plan': user.plan,
                'plan_info': plan_info,
                'status': user.subscription_status,
                'ends_at': user.subscription_ends_at.isoformat() if user.subscription_ends_at else None,
                'monthly_leads_limit': user.monthly_leads_limit,
                'monthly_emails_limit': user.monthly_emails_limit
            }
            
        finally:
            session.close()
    
    def upgrade_plan(self, user_id: int, new_plan: str) -> Dict:
        """Upgrade user to new plan"""
        session = get_db()
        
        try:
            user = session.query(User).get(user_id)
            if not user:
                return {'error': 'User not found'}
            
            if new_plan not in PLANS:
                return {'error': 'Invalid plan'}
            
            plan_info = PLANS[new_plan]
            
            # Update user subscription
            user.plan = new_plan
            user.subscription_status = 'active'
            user.subscription_ends_at = datetime.utcnow() + timedelta(days=30)
            user.monthly_leads_limit = plan_info['monthly_leads_limit']
            user.monthly_emails_limit = plan_info['monthly_emails_limit']
            
            session.commit()
            
            logger.info(f"User {user_id} upgraded to {new_plan}")
            
            return {
                'success': True,
                'message': f'Upgraded to {plan_info["name"]} plan',
                'plan': new_plan,
                'price': plan_info['price']
            }
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error upgrading plan: {e}")
            return {'error': str(e)}
        finally:
            session.close()
    
    def cancel_subscription(self, user_id: int) -> Dict:
        """Cancel user subscription"""
        session = get_db()
        
        try:
            user = session.query(User).get(user_id)
            if not user:
                return {'error': 'User not found'}
            
            # Downgrade to free at end of period
            user.subscription_status = 'cancelled'
            
            session.commit()
            
            logger.info(f"User {user_id} cancelled subscription")
            
            return {
                'success': True,
                'message': 'Subscription cancelled. Will downgrade to Free at end of period.',
                'ends_at': user.subscription_ends_at.isoformat() if user.subscription_ends_at else None
            }
            
        except Exception as e:
            session.rollback()
            return {'error': str(e)}
        finally:
            session.close()
    
    def check_usage_limits(self, user_id: int) -> Dict:
        """Check if user is within usage limits"""
        session = get_db()
        
        try:
            user = session.query(User).get(user_id)
            if not user:
                return {'error': 'User not found'}
            
            # In real implementation, track actual usage
            # For now, return limits
            
            return {
                'success': True,
                'leads_limit': user.monthly_leads_limit,
                'emails_limit': user.monthly_emails_limit,
                'leads_used': 0,  # TODO: Track actual usage
                'emails_used': 0,  # TODO: Track actual usage
                'within_limits': True
            }
            
        finally:
            session.close()
    
    def create_stripe_checkout(self, user_id: int, plan: str) -> Dict:
        """Create Stripe checkout session (placeholder)"""
        # In production, integrate with Stripe API
        # For now, return mock checkout URL
        
        if plan not in PLANS:
            return {'error': 'Invalid plan'}
        
        plan_info = PLANS[plan]
        
        # Mock checkout URL
        checkout_url = f"https://checkout.stripe.com/pay/mock_{plan}_{user_id}"
        
        return {
            'success': True,
            'checkout_url': checkout_url,
            'plan': plan,
            'price': plan_info['price']
        }
    
    def handle_webhook(self, event_type: str, data: Dict) -> Dict:
        """Handle Stripe webhook events (placeholder)"""
        # In production, verify webhook signature and process events
        
        logger.info(f"Webhook received: {event_type}")
        
        if event_type == 'payment_success':
            user_id = data.get('user_id')
            plan = data.get('plan')
            
            if user_id and plan:
                return self.upgrade_plan(user_id, plan)
        
        return {'success': True, 'message': 'Webhook processed'}


def create_subscription_manager():
    """Create subscription manager instance"""
    return SubscriptionManager()


if __name__ == '__main__':
    # Test subscription system
    from src.database import init_database
    
    print("Initializing...")
    init_database()
    
    manager = create_subscription_manager()
    
    # Get plans
    print("\n💰 Available Plans:")
    plans = manager.get_plans()
    for plan_id, plan_info in plans.items():
        print(f"\n{plan_info['name']} - ₹{plan_info['price']}/month")
        print(f"  Leads: {plan_info['monthly_leads_limit']}")
        print(f"  Emails: {plan_info['monthly_emails_limit']}")
        print(f"  Features: {', '.join(plan_info['features'])}")
    
    print("\n✅ Subscription system ready")
