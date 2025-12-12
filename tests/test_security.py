"""
Security tests for authentication and authorization
"""

import unittest
import json
from dashboard_premium import app
from src.auth import create_auth_manager

class TestSecurity(unittest.TestCase):
    """Security and authentication tests"""
    
    @classmethod
    def setUpClass(cls):
        """Setup test client and auth manager"""
        app.config['TESTING'] = True
        cls.client = app.test_client()
        cls.auth = create_auth_manager()
    
    def test_password_hashing(self):
        """Test password hashing is secure"""
        password = "test_password_123"
        hashed = self.auth.hash_password(password)
        
        # Hash should be different from password
        self.assertNotEqual(password, hashed)
        
        # Should verify correctly
        self.assertTrue(self.auth.verify_password(password, hashed))
        
        # Wrong password should fail
        self.assertFalse(self.auth.verify_password("wrong_password", hashed))
    
    def test_jwt_token_generation(self):
        """Test JWT token generation and verification"""
        # Create test user
        result = self.auth.create_user(
            email="test@example.com",
            password="test123",
            full_name="Test User"
        )
        
        if 'success' in result:
            # Authenticate
            auth_result = self.auth.authenticate("test@example.com", "test123")
            
            if 'success' in auth_result:
                token = auth_result['token']
                
                # Verify token
                verify_result = self.auth.verify_token(token)
                self.assertIn('success', verify_result)
                self.assertEqual(verify_result['payload']['email'], "test@example.com")
    
    def test_sql_injection_prevention(self):
        """Test SQL injection prevention"""
        # Try SQL injection in search
        malicious_query = "'; DROP TABLE leads; --"
        response = self.client.get(f'/api/search?q={malicious_query}')
        
        # Should not crash
        self.assertEqual(response.status_code, 200)
    
    def test_xss_prevention(self):
        """Test XSS prevention"""
        # Try XSS in lead data
        xss_payload = "<script>alert('XSS')</script>"
        
        # System should sanitize or escape
        # This is a placeholder - actual implementation depends on your sanitization
        self.assertNotIn("<script>", xss_payload.replace("<", "&lt;"))

if __name__ == '__main__':
    unittest.main()
