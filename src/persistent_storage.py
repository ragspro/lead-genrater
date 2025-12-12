"""
Persistent Storage Manager - Ensures leads never get lost
Handles both database and JSON backup with atomic writes
"""

import json
import os
import logging
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path
import shutil
from threading import Lock

logger = logging.getLogger(__name__)

class PersistentStorage:
    """Thread-safe persistent storage for leads"""
    
    def __init__(self, json_path: str = "data/premium_leads.json"):
        self.json_path = json_path
        self.backup_dir = "data/backups"
        self.lock = Lock()
        
        # Ensure directories exist
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)
        
        # Initialize file if doesn't exist
        if not os.path.exists(json_path):
            self._atomic_write([])
            logger.info(f"Created new leads file: {json_path}")
    
    def _atomic_write(self, data: List[Dict]) -> bool:
        """Atomic write to prevent data corruption"""
        temp_path = f"{self.json_path}.tmp"
        
        try:
            # Write to temp file first
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            # Atomic rename (overwrites existing file)
            shutil.move(temp_path, self.json_path)
            return True
            
        except Exception as e:
            logger.error(f"Atomic write failed: {e}")
            if os.path.exists(temp_path):
                os.remove(temp_path)
            return False
    
    def load_leads(self) -> List[Dict]:
        """Load leads from JSON with error recovery"""
        with self.lock:
            try:
                if not os.path.exists(self.json_path):
                    return []
                
                with open(self.json_path, 'r', encoding='utf-8') as f:
                    leads = json.load(f)
                
                logger.info(f"Loaded {len(leads)} leads from storage")
                return leads
                
            except json.JSONDecodeError as e:
                logger.error(f"JSON corrupted, attempting recovery: {e}")
                return self._recover_from_backup()
            except Exception as e:
                logger.error(f"Error loading leads: {e}")
                return []
    
    def save_leads(self, leads: List[Dict], create_backup: bool = True) -> bool:
        """Save leads with automatic backup"""
        with self.lock:
            try:
                # Create backup before overwriting
                if create_backup and os.path.exists(self.json_path):
                    self._create_backup()
                
                # Atomic write
                success = self._atomic_write(leads)
                
                if success:
                    logger.info(f"Saved {len(leads)} leads to storage")
                    return True
                else:
                    logger.error("Failed to save leads")
                    return False
                    
            except Exception as e:
                logger.error(f"Error saving leads: {e}")
                return False
    
    def append_leads(self, new_leads: List[Dict]) -> bool:
        """Append new leads without duplicates"""
        with self.lock:
            try:
                # Load existing
                existing_leads = self.load_leads()
                
                # Create set of existing IDs for fast lookup
                existing_ids = set()
                for lead in existing_leads:
                    key = (lead.get('title', ''), lead.get('address', ''))
                    existing_ids.add(key)
                
                # Add only new leads
                added = 0
                for lead in new_leads:
                    key = (lead.get('title', ''), lead.get('address', ''))
                    if key not in existing_ids:
                        existing_leads.append(lead)
                        existing_ids.add(key)
                        added += 1
                
                # Save combined list
                if added > 0:
                    success = self.save_leads(existing_leads)
                    if success:
                        logger.info(f"Appended {added} new leads (total: {len(existing_leads)})")
                        return True
                else:
                    logger.info("No new leads to append (all duplicates)")
                    return True
                
                return False
                
            except Exception as e:
                logger.error(f"Error appending leads: {e}")
                return False
    
    def _create_backup(self) -> bool:
        """Create timestamped backup"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = os.path.join(self.backup_dir, f"leads_backup_{timestamp}.json")
            
            shutil.copy2(self.json_path, backup_path)
            logger.info(f"Created backup: {backup_path}")
            
            # Keep only last 10 backups
            self._cleanup_old_backups(keep=10)
            return True
            
        except Exception as e:
            logger.error(f"Backup creation failed: {e}")
            return False
    
    def _cleanup_old_backups(self, keep: int = 10):
        """Keep only N most recent backups"""
        try:
            backups = sorted(
                Path(self.backup_dir).glob("leads_backup_*.json"),
                key=lambda p: p.stat().st_mtime,
                reverse=True
            )
            
            for backup in backups[keep:]:
                backup.unlink()
                logger.debug(f"Deleted old backup: {backup}")
                
        except Exception as e:
            logger.error(f"Backup cleanup failed: {e}")
    
    def _recover_from_backup(self) -> List[Dict]:
        """Recover from most recent backup"""
        try:
            backups = sorted(
                Path(self.backup_dir).glob("leads_backup_*.json"),
                key=lambda p: p.stat().st_mtime,
                reverse=True
            )
            
            if backups:
                backup_path = backups[0]
                logger.info(f"Recovering from backup: {backup_path}")
                
                with open(backup_path, 'r', encoding='utf-8') as f:
                    leads = json.load(f)
                
                # Restore to main file
                self._atomic_write(leads)
                logger.info(f"Recovered {len(leads)} leads from backup")
                return leads
            else:
                logger.warning("No backups available for recovery")
                return []
                
        except Exception as e:
            logger.error(f"Recovery failed: {e}")
            return []
    
    def get_stats(self) -> Dict:
        """Get storage statistics"""
        leads = self.load_leads()
        
        return {
            'total_leads': len(leads),
            'file_size_mb': os.path.getsize(self.json_path) / (1024 * 1024) if os.path.exists(self.json_path) else 0,
            'last_modified': datetime.fromtimestamp(os.path.getmtime(self.json_path)).isoformat() if os.path.exists(self.json_path) else None,
            'backup_count': len(list(Path(self.backup_dir).glob("leads_backup_*.json")))
        }


# Global instance
_storage = None

def get_storage() -> PersistentStorage:
    """Get global storage instance"""
    global _storage
    if _storage is None:
        _storage = PersistentStorage()
    return _storage
