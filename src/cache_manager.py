"""
Cache Manager - Speed up dashboard with intelligent caching
"""

import json
import time
from pathlib import Path
from typing import Any, Optional
import hashlib

class CacheManager:
    """Simple file-based cache with TTL"""
    
    def __init__(self, cache_dir: str = "data/cache", default_ttl: int = 3600):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.default_ttl = default_ttl
    
    def _get_cache_path(self, key: str) -> Path:
        """Get cache file path for key"""
        # Hash the key to create safe filename
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{key_hash}.json"
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired"""
        cache_path = self._get_cache_path(key)
        
        if not cache_path.exists():
            return None
        
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            # Check if expired
            if time.time() > cache_data['expires_at']:
                cache_path.unlink()  # Delete expired cache
                return None
            
            return cache_data['value']
        except Exception:
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache with TTL"""
        cache_path = self._get_cache_path(key)
        ttl = ttl or self.default_ttl
        
        try:
            cache_data = {
                'key': key,
                'value': value,
                'created_at': time.time(),
                'expires_at': time.time() + ttl
            }
            
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2)
            
            return True
        except Exception:
            return False
    
    def delete(self, key: str) -> bool:
        """Delete cache entry"""
        cache_path = self._get_cache_path(key)
        
        try:
            if cache_path.exists():
                cache_path.unlink()
            return True
        except Exception:
            return False
    
    def clear(self) -> int:
        """Clear all cache entries"""
        count = 0
        try:
            for cache_file in self.cache_dir.glob('*.json'):
                cache_file.unlink()
                count += 1
        except Exception:
            pass
        return count
    
    def clear_expired(self) -> int:
        """Clear only expired cache entries"""
        count = 0
        try:
            for cache_file in self.cache_dir.glob('*.json'):
                try:
                    with open(cache_file, 'r', encoding='utf-8') as f:
                        cache_data = json.load(f)
                    
                    if time.time() > cache_data['expires_at']:
                        cache_file.unlink()
                        count += 1
                except Exception:
                    pass
        except Exception:
            pass
        return count


# Global cache instance
_cache = CacheManager()

def get_cache() -> CacheManager:
    """Get global cache instance"""
    return _cache
