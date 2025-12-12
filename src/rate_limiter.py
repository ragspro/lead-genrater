"""
Rate Limiter - Free tier friendly rate limiting
Prevents API abuse and respects free tier limits
"""

import time
import logging
from datetime import datetime, timedelta
from collections import defaultdict
from threading import Lock

logger = logging.getLogger(__name__)


class RateLimiter:
    """Simple in-memory rate limiter for free tier APIs"""
    
    def __init__(self):
        self.requests = defaultdict(list)
        self.lock = Lock()
        
        # Free tier limits (per minute)
        self.limits = {
            'gemini': 15,      # Gemini AI: 15 requests/min (free tier)
            'serpapi': 5,      # SerpAPI: 100/month = ~5/min safe
            'gmail': 1,        # Gmail: 500/day = 1 every 2 min safe
            'whatsapp': 1,     # WhatsApp: Manual, 1/min safe
            'default': 10      # Default: 10/min
        }
        
        logger.info("Rate limiter initialized with free tier limits")
    
    def check_limit(self, service: str = 'default') -> bool:
        """
        Check if request is allowed under rate limit.
        
        Args:
            service: Service name (gemini, serpapi, gmail, etc.)
        
        Returns:
            True if allowed, False if rate limited
        """
        with self.lock:
            now = datetime.now()
            minute_ago = now - timedelta(minutes=1)
            
            # Clean old requests
            self.requests[service] = [
                req_time for req_time in self.requests[service]
                if req_time > minute_ago
            ]
            
            # Check limit
            limit = self.limits.get(service, self.limits['default'])
            current_count = len(self.requests[service])
            
            if current_count >= limit:
                logger.warning(f"Rate limit reached for {service}: {current_count}/{limit}")
                return False
            
            # Record request
            self.requests[service].append(now)
            return True
    
    def wait_if_needed(self, service: str = 'default', max_wait: int = 60):
        """
        Wait if rate limit is reached.
        
        Args:
            service: Service name
            max_wait: Maximum seconds to wait
        """
        waited = 0
        while not self.check_limit(service) and waited < max_wait:
            wait_time = 2
            logger.info(f"Rate limited, waiting {wait_time}s for {service}...")
            time.sleep(wait_time)
            waited += wait_time
        
        if waited >= max_wait:
            logger.error(f"Max wait time reached for {service}")
            raise Exception(f"Rate limit exceeded for {service}")
    
    def get_stats(self) -> dict:
        """Get current rate limit stats"""
        with self.lock:
            stats = {}
            for service, requests in self.requests.items():
                limit = self.limits.get(service, self.limits['default'])
                stats[service] = {
                    'current': len(requests),
                    'limit': limit,
                    'available': limit - len(requests)
                }
            return stats


# Global rate limiter instance
_rate_limiter = None


def get_rate_limiter() -> RateLimiter:
    """Get global rate limiter instance"""
    global _rate_limiter
    if _rate_limiter is None:
        _rate_limiter = RateLimiter()
    return _rate_limiter


# Decorator for rate limiting
def rate_limit(service: str = 'default'):
    """Decorator to rate limit function calls"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            limiter = get_rate_limiter()
            limiter.wait_if_needed(service)
            return func(*args, **kwargs)
        return wrapper
    return decorator


if __name__ == '__main__':
    # Test rate limiter
    limiter = RateLimiter()
    
    print("Testing rate limiter...")
    
    # Test Gemini limit (15/min)
    for i in range(20):
        if limiter.check_limit('gemini'):
            print(f"✅ Gemini request {i+1} allowed")
        else:
            print(f"⚠️ Gemini request {i+1} rate limited")
    
    print("\nRate limit stats:")
    print(limiter.get_stats())
