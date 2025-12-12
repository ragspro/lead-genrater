"""
Load testing for dashboard performance
"""

import unittest
import time
import concurrent.futures
from dashboard_premium import app

class TestLoadPerformance(unittest.TestCase):
    """Load and performance tests"""
    
    @classmethod
    def setUpClass(cls):
        """Setup test client"""
        app.config['TESTING'] = True
        cls.client = app.test_client()
    
    def test_concurrent_requests(self):
        """Test handling concurrent requests"""
        def make_request():
            response = self.client.get('/api/leads')
            return response.status_code == 200
        
        # Simulate 10 concurrent users
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        # All requests should succeed
        self.assertEqual(sum(results), 10)
    
    def test_response_time(self):
        """Test API response time"""
        start = time.time()
        response = self.client.get('/api/leads')
        duration = time.time() - start
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(duration, 2.0, "Response time should be under 2 seconds")
    
    def test_large_dataset_performance(self):
        """Test performance with large dataset"""
        start = time.time()
        response = self.client.get('/api/stats')
        duration = time.time() - start
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(duration, 1.0, "Stats calculation should be under 1 second")

if __name__ == '__main__':
    unittest.main()
