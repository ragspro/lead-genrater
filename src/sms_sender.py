"""
SMS Sender - FREE implementation using email-to-SMS gateways
No Twilio needed for basic SMS
"""

import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

logger = logging.getLogger(__name__)


class SMSSender:
    """Free SMS sender using email-to-SMS gateways"""
    
    # Email-to-SMS gateways (FREE!)
    CARRIERS = {
        'verizon': '@vtext.com',
        'tmobile': '@tmomail.net',
        'att': '@txt.att.net',
        'sprint': '@messaging.sprintpcs.com',
        'boost': '@sms.myboostmobile.com',
        'cricket': '@sms.cricketwireless.net',
        'uscellular': '@email.uscc.net',
        
        # India
        'airtel': '@airtelmail.com',
        'vodafone': '@vodafone.com',
        'jio': '@jio.com',
        'bsnl': '@bsnl.com',
    }
    
    def __init__(self, gmail_address: str, gmail_password: str):
        """
        Initialize SMS sender using Gmail SMTP.
        
        Args:
            gmail_address: Your Gmail address
            gmail_password: Gmail app password
        """
        self.gmail_address = gmail_address
        self.gmail_password = gmail_password
        logger.info("SMS sender initialized (free email-to-SMS mode)")
    
    def send_sms(self, phone: str, message: str, carrier: str = 'airtel') -> bool:
        """
        Send SMS using email-to-SMS gateway (FREE!).
        
        Args:
            phone: Phone number (10 digits)
            message: SMS message (keep under 160 chars)
            carrier: Carrier name (airtel, verizon, tmobile, etc.)
        
        Returns:
            True if sent successfully
        """
        try:
            # Clean phone number
            phone_clean = ''.join(filter(str.isdigit, phone))
            
            # Get carrier gateway
            gateway = self.CARRIERS.get(carrier.lower())
            if not gateway:
                logger.error(f"Unknown carrier: {carrier}")
                return False
            
            # Create email address
            to_email = phone_clean + gateway
            
            # Truncate message to 160 chars
            if len(message) > 160:
                message = message[:157] + '...'
            
            # Create email
            msg = MIMEMultipart()
            msg['From'] = self.gmail_address
            msg['To'] = to_email
            msg['Subject'] = ''  # No subject for SMS
            
            msg.attach(MIMEText(message, 'plain'))
            
            # Send via Gmail SMTP
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(self.gmail_address, self.gmail_password)
                server.send_message(msg)
            
            logger.info(f"✅ SMS sent to {phone} via {carrier}")
            return True
            
        except Exception as e:
            logger.error(f"SMS send error: {e}")
            return False
    
    def send_sms_auto_detect(self, phone: str, message: str, country: str = 'india') -> bool:
        """
        Send SMS with auto-detected carrier.
        
        Args:
            phone: Phone number
            message: SMS message
            country: Country (india, usa)
        
        Returns:
            True if sent successfully
        """
        # Try common carriers for country
        carriers = {
            'india': ['airtel', 'vodafone', 'jio', 'bsnl'],
            'usa': ['verizon', 'tmobile', 'att', 'sprint']
        }
        
        carrier_list = carriers.get(country.lower(), ['airtel'])
        
        # Try first carrier (most common)
        return self.send_sms(phone, message, carrier_list[0])


def create_sms_sender(gmail_address: str, gmail_password: str) -> SMSSender:
    """Factory function to create SMS sender"""
    return SMSSender(gmail_address, gmail_password)


if __name__ == '__main__':
    # Test SMS sender
    import os
    
    gmail = os.getenv('GMAIL_ADDRESS', 'your@gmail.com')
    password = os.getenv('GMAIL_APP_PASSWORD', 'your-app-password')
    
    sender = SMSSender(gmail, password)
    
    print("SMS Sender initialized")
    print("Supported carriers:", list(sender.CARRIERS.keys()))
    print("\nNote: Email-to-SMS is FREE but requires knowing the carrier")
