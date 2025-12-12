"""
AI Reply Classifier - Automatically classify and respond to replies
Converts 1 person into 5 salespeople
"""

import logging
from typing import Dict, Optional
from src.database import get_db, Lead, Interaction
from datetime import datetime

logger = logging.getLogger(__name__)


class ReplyClassifier:
    """Classify email/WhatsApp replies using AI"""
    
    # Reply categories
    CATEGORIES = {
        'Interested': {
            'keywords': ['interested', 'yes', 'tell me more', 'sounds good', 'lets talk', 'call me'],
            'sentiment': 'Positive',
            'priority': 'High',
            'action': 'Schedule call immediately'
        },
        'SendDetails': {
            'keywords': ['send details', 'more information', 'portfolio', 'pricing', 'case study'],
            'sentiment': 'Neutral',
            'priority': 'Medium',
            'action': 'Send detailed proposal'
        },
        'Budget': {
            'keywords': ['expensive', 'cost', 'budget', 'price', 'affordable', 'cheaper'],
            'sentiment': 'Neutral',
            'priority': 'Medium',
            'action': 'Discuss pricing options'
        },
        'NotNow': {
            'keywords': ['not now', 'later', 'busy', 'next month', 'next quarter', 'future'],
            'sentiment': 'Neutral',
            'priority': 'Low',
            'action': 'Follow up in 30 days'
        },
        'NotInterested': {
            'keywords': ['not interested', 'no thanks', 'unsubscribe', 'stop', 'remove'],
            'sentiment': 'Negative',
            'priority': 'Low',
            'action': 'Mark as cold, stop outreach'
        },
        'Spam': {
            'keywords': ['spam', 'scam', 'fraud', 'fake', 'report'],
            'sentiment': 'Negative',
            'priority': 'Low',
            'action': 'Blacklist and stop'
        }
    }
    
    def __init__(self, ai_assistant):
        """Initialize classifier"""
        self.ai = ai_assistant
        logger.info("Reply classifier initialized")
    
    def classify_reply(self, reply_text: str, lead_id: Optional[int] = None) -> Dict:
        """
        Classify a reply using AI and keywords.
        
        Args:
            reply_text: The reply content
            lead_id: Optional lead ID for context
        
        Returns:
            Classification dict with category, sentiment, suggested_response
        """
        reply_lower = reply_text.lower()
        
        # First try keyword matching (fast)
        for category, info in self.CATEGORIES.items():
            for keyword in info['keywords']:
                if keyword in reply_lower:
                    logger.info(f"Classified as {category} (keyword match)")
                    return {
                        'category': category,
                        'sentiment': info['sentiment'],
                        'priority': info['priority'],
                        'action': info['action'],
                        'confidence': 0.8,
                        'method': 'keyword'
                    }
        
        # If no keyword match, use AI
        try:
            classification = self._classify_with_ai(reply_text)
            logger.info(f"Classified as {classification['category']} (AI)")
            return classification
        except Exception as e:
            logger.error(f"AI classification failed: {e}")
            # Default to neutral
            return {
                'category': 'SendDetails',
                'sentiment': 'Neutral',
                'priority': 'Medium',
                'action': 'Manual review needed',
                'confidence': 0.3,
                'method': 'fallback'
            }
    
    def _classify_with_ai(self, reply_text: str) -> Dict:
        """Classify using Gemini AI"""
        
        prompt = f"""Classify this business reply into ONE category:

Reply: "{reply_text}"

Categories:
1. Interested - They want to know more, ready to talk
2. SendDetails - They want more information, portfolio, pricing
3. Budget - They're concerned about cost
4. NotNow - They're busy, want to talk later
5. NotInterested - They're not interested at all
6. Spam - Spam or angry response

Respond with ONLY the category name and confidence (0-1).
Format: Category|Confidence|Sentiment

Example: Interested|0.9|Positive"""
        
        try:
            response = self.ai.model.generate_content(prompt).text.strip()
            
            # Parse response
            parts = response.split('|')
            category = parts[0].strip()
            confidence = float(parts[1].strip()) if len(parts) > 1 else 0.7
            sentiment = parts[2].strip() if len(parts) > 2 else 'Neutral'
            
            # Validate category
            if category not in self.CATEGORIES:
                category = 'SendDetails'
            
            info = self.CATEGORIES[category]
            
            return {
                'category': category,
                'sentiment': sentiment,
                'priority': info['priority'],
                'action': info['action'],
                'confidence': confidence,
                'method': 'ai'
            }
            
        except Exception as e:
            logger.error(f"AI parsing error: {e}")
            raise
    
    def generate_response(self, reply_text: str, classification: Dict, 
                         lead: Optional[Lead] = None) -> str:
        """
        Generate appropriate response based on classification.
        
        Args:
            reply_text: Original reply
            classification: Classification result
            lead: Lead object for context
        
        Returns:
            Suggested response text
        """
        category = classification['category']
        business_name = lead.title if lead else "there"
        
        # Response templates by category
        if category == 'Interested':
            prompt = f"""Generate a response to this interested lead.

Their reply: "{reply_text}"
Business: {business_name}

Response should:
- Thank them for interest
- Suggest booking a call (calendly.com/ragsproai)
- Keep it under 60 words
- Be enthusiastic but professional"""
            
        elif category == 'SendDetails':
            prompt = f"""Generate a response to send details.

Their reply: "{reply_text}"
Business: {business_name}

Response should:
- Acknowledge their request
- Mention you'll send detailed info
- Include Ragspro portfolio link
- Suggest a quick call
- Under 80 words"""
            
        elif category == 'Budget':
            prompt = f"""Generate a response about budget concerns.

Their reply: "{reply_text}"
Business: {business_name}

Response should:
- Acknowledge budget concerns
- Mention flexible pricing
- Emphasize ROI (3-5x revenue increase)
- Offer free consultation
- Under 80 words"""
            
        elif category == 'NotNow':
            prompt = f"""Generate a response for "not now".

Their reply: "{reply_text}"
Business: {business_name}

Response should:
- Respect their timing
- Ask when would be better
- Offer to follow up later
- Keep door open
- Under 60 words"""
            
        elif category == 'NotInterested':
            return f"""Hi {business_name},

No problem at all - I understand.

If anything changes in the future, feel free to reach out.

Best regards,
Raghav Shah
Ragspro.com"""
            
        else:  # Spam or unknown
            return None  # Don't respond
        
        try:
            response = self.ai.model.generate_content(prompt).text.strip()
            return response
        except Exception as e:
            logger.error(f"Response generation failed: {e}")
            return self._get_fallback_response(category, business_name)
    
    def _get_fallback_response(self, category: str, business_name: str) -> str:
        """Fallback responses if AI fails"""
        
        responses = {
            'Interested': f"""Hi {business_name},

Great to hear you're interested!

Let's schedule a quick 15-minute call to discuss how we can help.

Book here: calendly.com/ragsproai

Looking forward to it!

Best,
Raghav Shah
+918700048490""",
            
            'SendDetails': f"""Hi {business_name},

Thanks for your interest!

I'll send you:
- Our portfolio with case studies
- Pricing options
- Recent client results

Meanwhile, here's our website: ragspro.com

Would you like to schedule a quick call?

Best,
Raghav""",
            
            'Budget': f"""Hi {business_name},

I understand budget is important.

Good news: We have flexible pricing and payment plans.

Plus, our clients typically see 3-5x ROI within 6 months.

Let's discuss options that work for you: calendly.com/ragsproai

Best,
Raghav""",
            
            'NotNow': f"""Hi {business_name},

No problem - I understand timing is important.

When would be a better time to reconnect?

I'll follow up then.

Best,
Raghav Shah"""
        }
        
        return responses.get(category, responses['SendDetails'])
    
    def process_reply(self, lead_id: int, reply_text: str, 
                     reply_type: str = 'Email') -> Dict:
        """
        Complete reply processing: classify + generate response + save.
        
        Args:
            lead_id: Lead ID
            reply_text: Reply content
            reply_type: Email or WhatsApp
        
        Returns:
            Processing result with classification and suggested response
        """
        session = get_db()
        
        try:
            lead = session.query(Lead).get(lead_id)
            if not lead:
                return {'error': 'Lead not found'}
            
            # Classify reply
            classification = self.classify_reply(reply_text, lead_id)
            
            # Generate response
            suggested_response = self.generate_response(
                reply_text, classification, lead
            )
            
            # Save interaction
            interaction = Interaction(
                lead_id=lead_id,
                type=reply_type,
                direction='Inbound',
                content=reply_text,
                replied=True,
                sentiment=classification['sentiment'],
                intent=classification['category']
            )
            session.add(interaction)
            
            # Update lead
            lead.email_replied = True
            lead.status = f"Replied - {classification['category']}"
            
            # Update analytics
            if lead.analytics:
                if reply_type == 'Email':
                    lead.analytics.total_emails_replied += 1
                else:
                    lead.analytics.total_whatsapp_replied += 1
                
                # Update lead temperature
                if classification['category'] == 'Interested':
                    lead.analytics.is_hot_lead = True
                    lead.analytics.is_warm_lead = False
                    lead.analytics.is_cold_lead = False
                elif classification['category'] in ['SendDetails', 'Budget']:
                    lead.analytics.is_warm_lead = True
                    lead.analytics.is_cold_lead = False
            
            session.commit()
            
            logger.info(f"Processed reply for lead {lead_id}: {classification['category']}")
            
            return {
                'success': True,
                'classification': classification,
                'suggested_response': suggested_response,
                'lead_status': lead.status
            }
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error processing reply: {e}")
            return {'error': str(e)}
        finally:
            session.close()


def create_reply_classifier(ai_assistant):
    """Create reply classifier instance"""
    return ReplyClassifier(ai_assistant)


if __name__ == '__main__':
    # Test reply classifier
    from src.ai_gemini import create_ai_assistant
    from src.config import load_config
    from src.database import init_database
    
    print("Initializing...")
    init_database()
    config = load_config()
    ai = create_ai_assistant(config['GEMINI_API_KEY'])
    
    classifier = create_reply_classifier(ai)
    
    # Test classifications
    test_replies = [
        "Yes, I'm interested! Can we schedule a call?",
        "Please send me more details and pricing",
        "Sounds expensive. What's your budget range?",
        "Not interested right now, maybe next month",
        "No thanks, not interested",
    ]
    
    print("\nTesting classifications:")
    for reply in test_replies:
        result = classifier.classify_reply(reply)
        print(f"\nReply: {reply}")
        print(f"Category: {result['category']}")
        print(f"Sentiment: {result['sentiment']}")
        print(f"Action: {result['action']}")
