"""
A/B Testing Framework - LEVEL 2
Test different email templates, subject lines, and strategies
"""

import logging
import random
from typing import Dict, List, Optional
from datetime import datetime
from sqlalchemy import func
from src.database import get_db, Template, Lead, Interaction, Campaign

logger = logging.getLogger(__name__)


class ABTestingFramework:
    """Manage A/B tests for templates and strategies"""
    
    def __init__(self):
        logger.info("A/B Testing framework initialized")
    
    def create_test(self, name: str, template_a_id: int, template_b_id: int,
                   description: str = '', target_size: int = 100) -> Dict:
        """Create a new A/B test"""
        session = get_db()
        
        try:
            # Verify templates exist
            template_a = session.query(Template).get(template_a_id)
            template_b = session.query(Template).get(template_b_id)
            
            if not template_a or not template_b:
                return {'error': 'Templates not found'}
            
            # Create campaign for tracking
            campaign = Campaign(
                name=f"A/B Test: {name}",
                description=f"{description}\nTemplate A: {template_a.name}\nTemplate B: {template_b.name}",
                channel='Email',
                status='Active',
                total_leads=target_size
            )
            
            session.add(campaign)
            session.commit()
            
            logger.info(f"Created A/B test: {name} (Campaign ID: {campaign.id})")
            
            return {
                'success': True,
                'test_id': campaign.id,
                'name': name,
                'template_a': template_a.name,
                'template_b': template_b.name,
                'target_size': target_size,
                'status': 'Active'
            }
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating A/B test: {e}")
            return {'error': str(e)}
        finally:
            session.close()
    
    def assign_variant(self, test_id: int, lead_id: int) -> str:
        """Assign a variant (A or B) to a lead"""
        # Simple 50/50 split
        variant = random.choice(['A', 'B'])
        
        # Store assignment in lead notes or custom field
        session = get_db()
        try:
            lead = session.query(Lead).get(lead_id)
            if lead:
                if not lead.notes:
                    lead.notes = ''
                lead.notes += f"\nA/B Test {test_id}: Variant {variant}"
                session.commit()
        finally:
            session.close()
        
        return variant
    
    def get_test_results(self, test_id: int) -> Dict:
        """Get results of an A/B test"""
        session = get_db()
        
        try:
            campaign = session.query(Campaign).get(test_id)
            if not campaign:
                return {'error': 'Test not found'}
            
            # Parse template IDs from description
            # In real implementation, store these properly
            
            # Get interactions for this campaign
            # For now, use all recent interactions as proxy
            variant_a_interactions = session.query(Interaction).filter(
                Interaction.type == 'Email',
                Interaction.direction == 'Outbound'
            ).limit(50).all()
            
            # Calculate metrics
            total_a = len([i for i in variant_a_interactions if 'Variant A' in (i.lead.notes or '')])
            total_b = len([i for i in variant_a_interactions if 'Variant B' in (i.lead.notes or '')])
            
            replied_a = len([i for i in variant_a_interactions 
                           if 'Variant A' in (i.lead.notes or '') and i.replied])
            replied_b = len([i for i in variant_a_interactions 
                           if 'Variant B' in (i.lead.notes or '') and i.replied])
            
            # Calculate rates
            reply_rate_a = (replied_a / total_a * 100) if total_a > 0 else 0
            reply_rate_b = (replied_b / total_b * 100) if total_b > 0 else 0
            
            # Determine winner
            if total_a < 30 or total_b < 30:
                winner = 'Insufficient data'
                confidence = 'low'
            elif reply_rate_a > reply_rate_b * 1.1:
                winner = 'Variant A'
                confidence = 'high' if total_a >= 50 else 'medium'
            elif reply_rate_b > reply_rate_a * 1.1:
                winner = 'Variant B'
                confidence = 'high' if total_b >= 50 else 'medium'
            else:
                winner = 'No clear winner'
                confidence = 'medium'
            
            return {
                'test_id': test_id,
                'name': campaign.name,
                'status': campaign.status,
                'variant_a': {
                    'sent': total_a,
                    'replied': replied_a,
                    'reply_rate': round(reply_rate_a, 1)
                },
                'variant_b': {
                    'sent': total_b,
                    'replied': replied_b,
                    'reply_rate': round(reply_rate_b, 1)
                },
                'winner': winner,
                'confidence': confidence,
                'improvement': round(abs(reply_rate_a - reply_rate_b), 1),
                'recommendation': self._get_test_recommendation(winner, reply_rate_a, reply_rate_b)
            }
            
        finally:
            session.close()
    
    def _get_test_recommendation(self, winner: str, rate_a: float, rate_b: float) -> str:
        """Get recommendation based on test results"""
        if winner == 'Insufficient data':
            return "Continue test - need more data (minimum 30 per variant)"
        elif winner == 'No clear winner':
            return "Both variants perform similarly - choose based on other factors"
        elif winner == 'Variant A':
            improvement = ((rate_a - rate_b) / rate_b * 100) if rate_b > 0 else 0
            return f"Use Variant A - {improvement:.0f}% better performance"
        else:
            improvement = ((rate_b - rate_a) / rate_a * 100) if rate_a > 0 else 0
            return f"Use Variant B - {improvement:.0f}% better performance"
    
    def stop_test(self, test_id: int, winner: str) -> Dict:
        """Stop a test and apply winner"""
        session = get_db()
        
        try:
            campaign = session.query(Campaign).get(test_id)
            if not campaign:
                return {'error': 'Test not found'}
            
            campaign.status = 'Completed'
            campaign.completed_at = datetime.utcnow()
            
            # Update description with winner
            campaign.description += f"\n\nWinner: {winner}"
            
            session.commit()
            
            logger.info(f"Stopped A/B test {test_id}, winner: {winner}")
            
            return {
                'success': True,
                'test_id': test_id,
                'winner': winner,
                'status': 'Completed'
            }
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error stopping test: {e}")
            return {'error': str(e)}
        finally:
            session.close()
    
    def get_active_tests(self) -> List[Dict]:
        """Get all active A/B tests"""
        session = get_db()
        
        try:
            campaigns = session.query(Campaign).filter(
                Campaign.name.like('A/B Test:%'),
                Campaign.status == 'Active'
            ).all()
            
            tests = []
            for campaign in campaigns:
                tests.append({
                    'test_id': campaign.id,
                    'name': campaign.name,
                    'created_at': campaign.created_at.isoformat() if campaign.created_at else None,
                    'total_leads': campaign.total_leads,
                    'sent_count': campaign.sent_count,
                    'status': campaign.status
                })
            
            return tests
            
        finally:
            session.close()
    
    def create_template_variant(self, original_id: int, variant_name: str,
                               changes: Dict) -> Dict:
        """Create a variant of an existing template"""
        session = get_db()
        
        try:
            original = session.query(Template).get(original_id)
            if not original:
                return {'error': 'Original template not found'}
            
            # Create variant
            variant = Template(
                name=f"{original.name} - {variant_name}",
                type=original.type,
                subject=changes.get('subject', original.subject),
                content=changes.get('content', original.content),
                variant=variant_name,
                parent_template_id=original_id,
                is_active=True
            )
            
            session.add(variant)
            session.commit()
            
            logger.info(f"Created template variant: {variant.name}")
            
            return {
                'success': True,
                'variant_id': variant.id,
                'name': variant.name,
                'parent_id': original_id
            }
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating variant: {e}")
            return {'error': str(e)}
        finally:
            session.close()
    
    def get_template_performance(self, template_id: int) -> Dict:
        """Get detailed performance of a template"""
        session = get_db()
        
        try:
            template = session.query(Template).get(template_id)
            if not template:
                return {'error': 'Template not found'}
            
            return {
                'template_id': template_id,
                'name': template.name,
                'type': template.type,
                'times_used': template.times_used,
                'open_rate': round(template.open_rate * 100, 1),
                'reply_rate': round(template.reply_rate * 100, 1),
                'conversion_rate': round(template.conversion_rate * 100, 1),
                'is_variant': template.variant is not None,
                'parent_id': template.parent_template_id
            }
            
        finally:
            session.close()
    
    def compare_templates(self, template_ids: List[int]) -> Dict:
        """Compare multiple templates"""
        session = get_db()
        
        try:
            templates = session.query(Template).filter(
                Template.id.in_(template_ids)
            ).all()
            
            comparison = []
            for template in templates:
                comparison.append({
                    'id': template.id,
                    'name': template.name,
                    'times_used': template.times_used,
                    'reply_rate': round(template.reply_rate * 100, 1),
                    'conversion_rate': round(template.conversion_rate * 100, 1)
                })
            
            # Sort by reply rate
            comparison.sort(key=lambda x: x['reply_rate'], reverse=True)
            
            # Determine best
            best = comparison[0] if comparison else None
            
            return {
                'templates': comparison,
                'best_template': best,
                'recommendation': f"Use '{best['name']}' - highest reply rate" if best else "No data"
            }
            
        finally:
            session.close()


def create_ab_testing_framework():
    """Create A/B testing framework instance"""
    return ABTestingFramework()


if __name__ == '__main__':
    # Test A/B framework
    from src.database import init_database
    
    print("Initializing...")
    init_database()
    
    framework = create_ab_testing_framework()
    
    print("\n🧪 A/B Testing Framework Ready")
    
    # Get active tests
    tests = framework.get_active_tests()
    print(f"\n📊 Active Tests: {len(tests)}")
    
    for test in tests:
        print(f"  • {test['name']} - {test['sent_count']} sent")
