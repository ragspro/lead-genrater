"""
Follow-up Engine - Automatic follow-up sequences
Increases close rate by 3x
"""

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from src.database import get_db, Lead, FollowUp, Interaction
from src.ai_gemini import create_ai_assistant
from src.email_sender import create_gmail_sender
from src.whatsapp_sender import create_whatsapp_sender

logger = logging.getLogger(__name__)


class FollowUpEngine:
    """Manages automatic follow-up sequences"""
    
    # Follow-up schedule (days after initial contact)
    FOLLOW_UP_SCHEDULE = {
        1: 2,   # First follow-up after 2 days
        2: 4,   # Second follow-up after 4 days (total 6 days)
        3: 7,   # Third follow-up after 7 days (total 13 days)
    }
    
    def __init__(self, ai_assistant, email_sender, whatsapp_sender):
        """Initialize follow-up engine"""
        self.ai = ai_assistant
        self.email = email_sender
        self.whatsapp = whatsapp_sender
        logger.info("Follow-up engine initialized")
    
    def schedule_follow_ups(self, lead_id: int, channel: str = 'Email') -> List[FollowUp]:
        """
        Schedule follow-up sequence for a lead.
        
        Args:
            lead_id: Lead ID
            channel: Email or WhatsApp
        
        Returns:
            List of scheduled follow-ups
        """
        session = get_db()
        
        try:
            lead = session.query(Lead).get(lead_id)
            if not lead:
                logger.error(f"Lead {lead_id} not found")
                return []
            
            # Check if already has follow-ups
            existing = session.query(FollowUp).filter_by(
                lead_id=lead_id,
                status='Pending'
            ).count()
            
            if existing > 0:
                logger.info(f"Lead {lead_id} already has {existing} pending follow-ups")
                return []
            
            # Create follow-up sequence
            follow_ups = []
            base_date = lead.last_contacted or datetime.utcnow()
            
            for sequence, days_after in self.FOLLOW_UP_SCHEDULE.items():
                scheduled_at = base_date + timedelta(days=days_after)
                
                # Generate content
                content = self._generate_follow_up_content(
                    lead=lead,
                    sequence_number=sequence,
                    channel=channel
                )
                
                follow_up = FollowUp(
                    lead_id=lead_id,
                    sequence_number=sequence,
                    scheduled_at=scheduled_at,
                    channel=channel,
                    subject=content['subject'],
                    content=content['body'],
                    status='Pending'
                )
                
                session.add(follow_up)
                follow_ups.append(follow_up)
            
            session.commit()
            logger.info(f"Scheduled {len(follow_ups)} follow-ups for lead {lead_id}")
            return follow_ups
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error scheduling follow-ups: {e}")
            return []
        finally:
            session.close()
    
    def _generate_follow_up_content(self, lead: Lead, sequence_number: int, 
                                    channel: str) -> Dict[str, str]:
        """Generate personalized follow-up content"""
        
        business_name = lead.title
        business_type = lead.type or 'business'
        
        # Different approach for each follow-up
        if sequence_number == 1:
            # Gentle reminder
            subject = f"Following up - {business_name}"
            prompt = f"""Generate a gentle follow-up email for {business_name} ({business_type}).
            
This is the first follow-up after initial contact. Keep it:
- Short and friendly
- Reference the previous email
- Add value (share a quick tip or insight)
- Soft CTA (just checking if they saw the email)

Under 80 words."""
            
        elif sequence_number == 2:
            # Value-add content
            subject = f"Quick resource for {business_name}"
            prompt = f"""Generate a value-add follow-up email for {business_name} ({business_type}).
            
This is the second follow-up. Include:
- A helpful resource (case study, guide, or tip)
- Show expertise without being pushy
- Mention Ragspro's recent success
- Medium CTA (offer free consultation)

Under 100 words."""
            
        else:
            # Last chance
            subject = f"Last call - {business_name}"
            prompt = f"""Generate a final follow-up email for {business_name} ({business_type}).
            
This is the last follow-up. Make it:
- Direct but respectful
- Create urgency (limited slots, special offer)
- Clear CTA (book call or reply)
- Easy opt-out option

Under 80 words."""
        
        try:
            # Generate with AI
            body = self.ai.model.generate_content(prompt).text.strip()
        except:
            # Fallback template
            body = self._get_fallback_template(business_name, sequence_number)
        
        return {
            'subject': subject,
            'body': body
        }
    
    def _get_fallback_template(self, business_name: str, sequence: int) -> str:
        """Fallback templates if AI fails"""
        
        templates = {
            1: f"""Hi {business_name} team,

Just following up on my previous email about helping you grow online.

Quick question: Are you currently looking to improve your digital presence?

If yes, I'd love to share how we've helped similar businesses increase revenue by 3-5x.

Best regards,
Raghav Shah
Ragspro.com""",
            
            2: f"""Hi {business_name},

I wanted to share a quick case study that might interest you.

We recently helped a {business_name.split()[0]} business increase their online leads by 300% in just 3 months.

Would you like to see how we did it?

Free consultation available: calendly.com/ragsproai

Best,
Raghav""",
            
            3: f"""Hi {business_name},

This is my last email - I don't want to be pushy!

We have 2 slots left this month for new clients. If you're interested in growing your business online, let me know.

Otherwise, I'll assume it's not the right time and won't bother you again.

Thanks,
Raghav Shah
+918700048490"""
        }
        
        return templates.get(sequence, templates[1])
    
    def process_due_follow_ups(self) -> Dict[str, int]:
        """
        Process all due follow-ups.
        Should be run daily via cron/scheduler.
        
        Returns:
            Stats dict with sent/failed counts
        """
        session = get_db()
        stats = {'sent': 0, 'failed': 0, 'skipped': 0}
        
        try:
            # Get all pending follow-ups that are due
            now = datetime.utcnow()
            due_follow_ups = session.query(FollowUp).filter(
                FollowUp.status == 'Pending',
                FollowUp.scheduled_at <= now
            ).all()
            
            logger.info(f"Processing {len(due_follow_ups)} due follow-ups")
            
            for follow_up in due_follow_ups:
                try:
                    # Check if lead has replied (skip if yes)
                    if follow_up.lead.email_replied:
                        follow_up.status = 'Skipped'
                        stats['skipped'] += 1
                        continue
                    
                    # Send follow-up
                    if follow_up.channel == 'Email':
                        success = self._send_email_follow_up(follow_up)
                    elif follow_up.channel == 'WhatsApp':
                        success = self._send_whatsapp_follow_up(follow_up)
                    else:
                        success = False
                    
                    if success:
                        follow_up.status = 'Sent'
                        follow_up.sent_at = datetime.utcnow()
                        stats['sent'] += 1
                        
                        # Update lead
                        follow_up.lead.last_contacted = datetime.utcnow()
                    else:
                        stats['failed'] += 1
                    
                except Exception as e:
                    logger.error(f"Error processing follow-up {follow_up.id}: {e}")
                    stats['failed'] += 1
            
            session.commit()
            logger.info(f"Follow-up processing complete: {stats}")
            return stats
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error processing follow-ups: {e}")
            return stats
        finally:
            session.close()
    
    def _send_email_follow_up(self, follow_up: FollowUp) -> bool:
        """Send email follow-up"""
        try:
            lead = follow_up.lead
            
            if not lead.email:
                logger.warning(f"No email for lead {lead.id}")
                return False
            
            success = self.email.send_email(
                to_email=lead.email,
                subject=follow_up.subject,
                body=follow_up.content,
                business_name=lead.title
            )
            
            if success:
                # Track interaction
                session = get_db()
                interaction = Interaction(
                    lead_id=lead.id,
                    type='Email',
                    direction='Outbound',
                    subject=follow_up.subject,
                    content=follow_up.content
                )
                session.add(interaction)
                session.commit()
                session.close()
            
            return success
            
        except Exception as e:
            logger.error(f"Error sending email follow-up: {e}")
            return False
    
    def _send_whatsapp_follow_up(self, follow_up: FollowUp) -> bool:
        """Send WhatsApp follow-up"""
        try:
            lead = follow_up.lead
            
            if not lead.phone:
                logger.warning(f"No phone for lead {lead.id}")
                return False
            
            success = self.whatsapp.send_message(
                phone_number=lead.phone,
                message=follow_up.content,
                business_name=lead.title
            )
            
            if success:
                # Track interaction
                session = get_db()
                interaction = Interaction(
                    lead_id=lead.id,
                    type='WhatsApp',
                    direction='Outbound',
                    content=follow_up.content
                )
                session.add(interaction)
                session.commit()
                session.close()
            
            return success
            
        except Exception as e:
            logger.error(f"Error sending WhatsApp follow-up: {e}")
            return False
    
    def cancel_follow_ups(self, lead_id: int, reason: str = 'Lead responded') -> int:
        """
        Cancel all pending follow-ups for a lead.
        
        Args:
            lead_id: Lead ID
            reason: Cancellation reason
        
        Returns:
            Number of cancelled follow-ups
        """
        session = get_db()
        
        try:
            cancelled = session.query(FollowUp).filter(
                FollowUp.lead_id == lead_id,
                FollowUp.status == 'Pending'
            ).update({
                'status': 'Skipped',
                'notes': reason
            })
            
            session.commit()
            logger.info(f"Cancelled {cancelled} follow-ups for lead {lead_id}: {reason}")
            return cancelled
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error cancelling follow-ups: {e}")
            return 0
        finally:
            session.close()


def create_follow_up_engine(config: dict):
    """Create follow-up engine instance"""
    from src.config import load_config
    
    if not config:
        config = load_config()
    
    ai = create_ai_assistant(config['GEMINI_API_KEY'])
    email = create_gmail_sender(config['GMAIL_ADDRESS'], config['GMAIL_APP_PASSWORD'])
    whatsapp = create_whatsapp_sender(auto_mode=True)
    
    return FollowUpEngine(ai, email, whatsapp)


if __name__ == '__main__':
    # Test follow-up engine
    from src.config import load_config
    from src.database import init_database
    
    print("Initializing...")
    init_database()
    config = load_config()
    
    engine = create_follow_up_engine(config)
    
    # Test scheduling
    print("\nTesting follow-up scheduling...")
    # Assuming lead ID 1 exists
    follow_ups = engine.schedule_follow_ups(lead_id=1, channel='Email')
    print(f"✅ Scheduled {len(follow_ups)} follow-ups")
    
    # Test processing
    print("\nTesting follow-up processing...")
    stats = engine.process_due_follow_ups()
    print(f"✅ Processed: {stats}")
