"""
LinkedIn Scraper - FREE implementation using requests + BeautifulSoup
No Selenium needed for basic scraping
"""

import requests
import logging
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import time
import re

logger = logging.getLogger(__name__)


class LinkedInScraper:
    """Free LinkedIn scraper using public profiles"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        logger.info("LinkedIn scraper initialized (free mode)")
    
    def search_profiles(self, keywords: str, location: str = '', limit: int = 10) -> List[Dict]:
        """
        Search LinkedIn profiles using Google search (free method).
        
        Args:
            keywords: Search keywords (e.g., "CEO tech startup")
            location: Location filter
            limit: Max results
        
        Returns:
            List of profile dictionaries
        """
        try:
            # Use Google to find LinkedIn profiles (free!)
            query = f'site:linkedin.com/in {keywords}'
            if location:
                query += f' {location}'
            
            # Google search URL
            url = f'https://www.google.com/search?q={requests.utils.quote(query)}&num={limit}'
            
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            profiles = []
            for result in soup.select('.g')[:limit]:
                try:
                    link_elem = result.select_one('a')
                    title_elem = result.select_one('h3')
                    snippet_elem = result.select_one('.VwiC3b')
                    
                    if link_elem and 'linkedin.com/in/' in link_elem.get('href', ''):
                        profile_url = link_elem['href']
                        
                        # Extract name from title
                        title = title_elem.text if title_elem else ''
                        name = title.split('-')[0].strip() if '-' in title else title
                        
                        # Extract info from snippet
                        snippet = snippet_elem.text if snippet_elem else ''
                        
                        profiles.append({
                            'name': name,
                            'profile_url': profile_url,
                            'title': title,
                            'snippet': snippet,
                            'source': 'google_search'
                        })
                except Exception as e:
                    logger.debug(f"Error parsing result: {e}")
                    continue
            
            logger.info(f"Found {len(profiles)} LinkedIn profiles for '{keywords}'")
            return profiles
            
        except Exception as e:
            logger.error(f"LinkedIn search error: {e}")
            return []
    
    def enrich_lead_with_linkedin(self, business_name: str, location: str = '') -> Optional[Dict]:
        """
        Find LinkedIn profile for a business.
        
        Args:
            business_name: Business name
            location: Location
        
        Returns:
            LinkedIn profile data or None
        """
        try:
            # Search for company page
            query = f'site:linkedin.com/company {business_name}'
            if location:
                query += f' {location}'
            
            url = f'https://www.google.com/search?q={requests.utils.quote(query)}&num=3'
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Get first result
            first_result = soup.select_one('.g')
            if first_result:
                link = first_result.select_one('a')
                if link and 'linkedin.com/company/' in link.get('href', ''):
                    return {
                        'company_url': link['href'],
                        'found': True
                    }
            
            return None
            
        except Exception as e:
            logger.error(f"LinkedIn enrichment error: {e}")
            return None
    
    def extract_email_from_profile(self, profile_url: str) -> Optional[str]:
        """
        Try to extract email from LinkedIn profile (limited success).
        
        Note: LinkedIn doesn't expose emails publicly, this is best-effort.
        """
        # This is a placeholder - LinkedIn doesn't expose emails
        # In production, you'd need LinkedIn API or Sales Navigator
        logger.info("Email extraction from LinkedIn requires API access")
        return None


def create_linkedin_scraper() -> LinkedInScraper:
    """Factory function to create LinkedIn scraper"""
    return LinkedInScraper()


if __name__ == '__main__':
    # Test LinkedIn scraper
    scraper = LinkedInScraper()
    
    print("Testing LinkedIn scraper...")
    profiles = scraper.search_profiles("CEO tech startup", "San Francisco", limit=5)
    
    print(f"\nFound {len(profiles)} profiles:")
    for profile in profiles:
        print(f"- {profile['name']}: {profile['profile_url']}")
