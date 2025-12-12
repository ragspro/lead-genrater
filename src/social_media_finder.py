"""Social Media Finder - Extract social media links from business data"""

import logging
import re
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def find_social_media_links(business_name: str, website: str = None, phone: str = None) -> dict:
    """
    Find social media links for a business.
    
    Args:
        business_name: Name of the business
        website: Business website URL
        phone: Business phone number
    
    Returns:
        Dictionary with social media links
    """
    social_links = {
        'linkedin': None,
        'facebook': None,
        'instagram': None,
        'twitter': None,
        'youtube': None
    }
    
    try:
        # If website exists, try to scrape social links from it
        if website:
            try:
                logger.info(f"🔍 Searching social media for: {business_name}")
                
                # Add timeout and headers
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                response = requests.get(website, timeout=5, headers=headers)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Find all links
                    for link in soup.find_all('a', href=True):
                        href = link['href'].lower()
                        
                        # LinkedIn
                        if 'linkedin.com' in href and not social_links['linkedin']:
                            social_links['linkedin'] = link['href']
                        
                        # Facebook
                        elif 'facebook.com' in href and not social_links['facebook']:
                            social_links['facebook'] = link['href']
                        
                        # Instagram
                        elif 'instagram.com' in href and not social_links['instagram']:
                            social_links['instagram'] = link['href']
                        
                        # Twitter/X
                        elif ('twitter.com' in href or 'x.com' in href) and not social_links['twitter']:
                            social_links['twitter'] = link['href']
                        
                        # YouTube
                        elif 'youtube.com' in href and not social_links['youtube']:
                            social_links['youtube'] = link['href']
                    
                    found_count = sum(1 for v in social_links.values() if v)
                    if found_count > 0:
                        logger.info(f"✅ Found {found_count} social media links")
                
            except Exception as e:
                logger.debug(f"Could not scrape website: {e}")
        
        # Generate likely social media URLs based on business name
        # Clean business name for URL
        clean_name = re.sub(r'[^a-zA-Z0-9]', '', business_name.lower())
        
        # If no links found, generate likely URLs
        if not any(social_links.values()):
            # These are guesses - may or may not exist
            social_links['linkedin'] = f"https://linkedin.com/company/{clean_name}"
            social_links['facebook'] = f"https://facebook.com/{clean_name}"
            social_links['instagram'] = f"https://instagram.com/{clean_name}"
            social_links['twitter'] = f"https://twitter.com/{clean_name}"
            
            logger.info(f"💡 Generated likely social media URLs")
    
    except Exception as e:
        logger.error(f"Error finding social media: {e}")
    
    return social_links


def extract_email_from_website(website: str) -> str:
    """
    Try to extract email from website.
    
    Args:
        website: Business website URL
    
    Returns:
        Email address or None
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(website, timeout=5, headers=headers)
        
        if response.status_code == 200:
            # Find email patterns
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, response.text)
            
            if emails:
                # Filter out common non-business emails
                filtered = [e for e in emails if not any(x in e.lower() for x in ['example', 'test', 'noreply', 'admin'])]
                if filtered:
                    logger.info(f"✅ Found email: {filtered[0]}")
                    return filtered[0]
    
    except Exception as e:
        logger.debug(f"Could not extract email: {e}")
    
    return None


def enrich_lead_with_social_media(lead: dict) -> dict:
    """
    Enrich lead with social media links and email.
    
    Args:
        lead: Lead dictionary
    
    Returns:
        Enriched lead with social media
    """
    try:
        # Find social media links
        social_links = find_social_media_links(
            lead.get('title', ''),
            lead.get('website'),
            lead.get('phone')
        )
        
        lead['social_media'] = social_links
        
        # Try to extract email if not present
        if not lead.get('email') and lead.get('website'):
            email = extract_email_from_website(lead['website'])
            if email:
                lead['email'] = email
        
        logger.info(f"✅ Enriched: {lead.get('title')} with social media")
        
    except Exception as e:
        logger.error(f"Error enriching lead: {e}")
        lead['social_media'] = {
            'linkedin': None,
            'facebook': None,
            'instagram': None,
            'twitter': None,
            'youtube': None
        }
    
    return lead
