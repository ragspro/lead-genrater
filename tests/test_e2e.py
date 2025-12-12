"""
End-to-End tests for dashboard and API
"""

import unittest
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dashboard_premium import app

class TestEndToEnd(unittest.TestCase):
    """End-to-end tests for complete system"""
    
    @classmethod
    def setUpClass(cls):
        """Setup test client"""
        app.config['TESTING'] = True
        cls.client = app.test_client()
    
    def test_dashboard_loads(self):
        """Test dashboard page loads"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_api_leads_endpoint(self):
        """Test /api/leads endpoint"""
        response = self.client.get('/api/leads')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('success', data)
        self.assertIn('leads', data)
        self.assertIn('total', data)
    
    def test_api_stats_endpoint(self):
        """Test /api/stats endpoint"""
        response = self.client.get('/api/stats')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('success', data)
        self.assertIn('stats', data)
    
    def test_api_status_endpoint(self):
        """Test /api/status endpoint"""
        response = self.client.get('/api/status')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('success', data)
        self.assertIn('status', data)
    
    def test_api_analytics_dashboard(self):
        """Test /api/analytics/dashboard endpoint"""
        response = self.client.get('/api/analytics/dashboard')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('success', data)
    
    def test_lead_detail_endpoint(self):
        """Test /api/lead/<id> endpoint"""
        # First get leads
        response = self.client.get('/api/leads')
        data = json.loads(response.data)
        
        if data['total'] > 0:
            # Test first lead
            response = self.client.get('/api/lead/0')
            self.assertEqual(response.status_code, 200)
            
            lead_data = json.loads(response.data)
            self.assertIn('success', lead_data)

if __name__ == '__main__':
    unittest.main()
