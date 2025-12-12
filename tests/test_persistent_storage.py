"""
Unit tests for persistent storage
"""

import unittest
import os
import json
import tempfile
import shutil
from src.persistent_storage import PersistentStorage

class TestPersistentStorage(unittest.TestCase):
    """Test persistent storage functionality"""
    
    def setUp(self):
        """Create temporary directory for tests"""
        self.test_dir = tempfile.mkdtemp()
        self.json_path = os.path.join(self.test_dir, "test_leads.json")
        self.storage = PersistentStorage(json_path=self.json_path)
    
    def tearDown(self):
        """Clean up temporary directory"""
        shutil.rmtree(self.test_dir)
    
    def test_save_and_load_leads(self):
        """Test saving and loading leads"""
        test_leads = [
            {'title': 'Test Business 1', 'address': '123 Main St'},
            {'title': 'Test Business 2', 'address': '456 Oak Ave'}
        ]
        
        # Save
        success = self.storage.save_leads(test_leads)
        self.assertTrue(success)
        
        # Load
        loaded = self.storage.load_leads()
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0]['title'], 'Test Business 1')
    
    def test_append_leads_no_duplicates(self):
        """Test appending leads without duplicates"""
        initial = [
            {'title': 'Business A', 'address': 'Address A'}
        ]
        self.storage.save_leads(initial)
        
        new_leads = [
            {'title': 'Business A', 'address': 'Address A'},  # Duplicate
            {'title': 'Business B', 'address': 'Address B'}   # New
        ]
        
        self.storage.append_leads(new_leads)
        
        all_leads = self.storage.load_leads()
        self.assertEqual(len(all_leads), 2)  # Should have 2, not 3
    
    def test_backup_creation(self):
        """Test backup creation"""
        test_leads = [{'title': 'Test', 'address': 'Test'}]
        self.storage.save_leads(test_leads, create_backup=True)
        
        # Check backup exists
        backup_dir = os.path.join(self.test_dir, "backups")
        backups = list(os.listdir(backup_dir)) if os.path.exists(backup_dir) else []
        self.assertGreater(len(backups), 0)
    
    def test_atomic_write(self):
        """Test atomic write prevents corruption"""
        test_leads = [{'title': 'Test', 'address': 'Test'}]
        
        # Should succeed
        success = self.storage._atomic_write(test_leads)
        self.assertTrue(success)
        
        # File should exist and be valid JSON
        self.assertTrue(os.path.exists(self.json_path))
        with open(self.json_path, 'r') as f:
            data = json.load(f)
        self.assertEqual(len(data), 1)
    
    def test_get_stats(self):
        """Test storage statistics"""
        test_leads = [{'title': 'Test', 'address': 'Test'}]
        self.storage.save_leads(test_leads)
        
        stats = self.storage.get_stats()
        self.assertEqual(stats['total_leads'], 1)
        self.assertGreater(stats['file_size_mb'], 0)
        self.assertIsNotNone(stats['last_modified'])

if __name__ == '__main__':
    unittest.main()
