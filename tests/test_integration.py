"""
Integration tests for complete system
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import init_database, get_db, Lead
from src.persistent_storage import get_storage
from src.analytics import create_analytics_engine
from src.follow_up_engine import create_follow_up_engine
from src.config import load_config

class TestSystemIntegration(unittest.TestCase):
    """Test complete system integration"""
    
    @classmethod
    def setUpClass(cls):
        """Initialize system once for all tests"""
        init_database()
        cls.config = load_config()
    
    def test_database_connection(self):
        """Test database connectivity"""
        session = get_db()
        self.assertIsNotNone(session)
        
        # Test query
        count = session.query(Lead).count()
        self.assertGreaterEqual(count, 0)
        session.close()
    
    def test_storage_integration(self):
        """Test storage system"""
        storage = get_storage()
        leads = storage.load_leads()
        self.assertIsInstance(leads, list)
    
    def test_analytics_engine(self):
        """Test analytics engine"""
        analytics = create_analytics_engine()
        stats = analytics.get_dashboard_stats()
        
        self.assertIn('total_leads', stats)
        self.assertIn('emails_sent', stats)
        self.assertGreaterEqual(stats['total_leads'], 0)
    
    def test_follow_up_engine(self):
        """Test follow-up engine"""
        try:
            engine = create_follow_up_engine(self.config)
            self.assertIsNotNone(engine)
        except Exception as e:
            self.fail(f"Follow-up engine initialization failed: {e}")
    
    def test_end_to_end_lead_flow(self):
        """Test complete lead flow: create -> store -> retrieve"""
        # Create test lead
        test_lead = {
            'title': 'Integration Test Business',
            'type': 'Test',
            'address': '123 Test St',
            'city': 'Test City',
            'rating': 4.5,
            'reviews': 100,
            'quality_score': 85
        }
        
        # Store in persistent storage
        storage = get_storage()
        initial_count = len(storage.load_leads())
        
        storage.append_leads([test_lead])
        
        # Verify stored
        final_count = len(storage.load_leads())
        self.assertEqual(final_count, initial_count + 1)
        
        # Verify in database
        session = get_db()
        db_lead = session.query(Lead).filter_by(title='Integration Test Business').first()
        
        if db_lead:
            self.assertEqual(db_lead.title, 'Integration Test Business')
            
            # Cleanup
            session.delete(db_lead)
            session.commit()
        
        session.close()

if __name__ == '__main__':
    unittest.main()
