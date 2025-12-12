"""
User Authentication System - LEVEL 3
JWT-based authentication with role-based access control
"""

import logging
import jwt
import bcrypt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
from src.database import get_db, User

logger = logging.getLogger(__name__)

# Secret key for JWT (in production, use environment variable)
SECRET_KEY = "ragspro_secret_key_2024_change_in_production"
ALGORITHM = "HS256"
TOKEN_EXPIRY_HOURS = 24


class AuthManager:
    """Manage user authentication and authorization"""
    
    def __init__(self):
        logger.info("Auth manager initialized")
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def create_user(self, email: str, password: str, full_name: str,
                   company_name: str = '', role: str = 'user') -> dict:
        """Create new user"""
        session = get_db()
        
        try:
            # Check if user exists
            existing = session.query(User).filter_by(email=email).first()
            if existing:
                return {'error': 'User already exists'}
            
            # Hash password
            password_hash = self.hash_password(password)
            
            # Create user
            user = User(
                email=email,
                password_hash=password_hash,
                full_name=full_name,
                company_name=company_name,
                role=role,
                is_active=True,
                is_verified=False,
                plan='free',
                monthly_leads_limit=500,
                monthly_emails_limit=1000
            )
            
            session.add(user)
            session.commit()
            
            logger.info(f"User created: {email}")
            
            return {
                'success': True,
                'user_id': user.id,
                'email': user.email,
                'role': user.role
            }
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating user: {e}")
            return {'error': str(e)}
        finally:
            session.close()
    
    def authenticate(self, email: str, password: str) -> dict:
        """Authenticate user and return JWT token"""
        session = get_db()
        
        try:
            user = session.query(User).filter_by(email=email).first()
            
            if not user:
                return {'error': 'Invalid credentials'}
            
            if not user.is_active:
                return {'error': 'Account is inactive'}
            
            # Verify password
            if not self.verify_password(password, user.password_hash):
                return {'error': 'Invalid credentials'}
            
            # Update last login
            user.last_login_at = datetime.utcnow()
            session.commit()
            
            # Generate JWT token
            token = self.generate_token(user)
            
            logger.info(f"User authenticated: {email}")
            
            return {
                'success': True,
                'token': token,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'full_name': user.full_name,
                    'role': user.role,
                    'plan': user.plan
                }
            }
            
        finally:
            session.close()
    
    def generate_token(self, user: User) -> str:
        """Generate JWT token"""
        payload = {
            'user_id': user.id,
            'email': user.email,
            'role': user.role,
            'exp': datetime.utcnow() + timedelta(hours=TOKEN_EXPIRY_HOURS)
        }
        
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token
    
    def verify_token(self, token: str) -> dict:
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return {'success': True, 'payload': payload}
        except jwt.ExpiredSignatureError:
            return {'error': 'Token expired'}
        except jwt.InvalidTokenError:
            return {'error': 'Invalid token'}
    
    def get_current_user(self, token: str) -> User:
        """Get current user from token"""
        result = self.verify_token(token)
        
        if 'error' in result:
            return None
        
        session = get_db()
        try:
            user = session.query(User).get(result['payload']['user_id'])
            return user
        finally:
            session.close()
    
    def update_user(self, user_id: int, updates: dict) -> dict:
        """Update user details"""
        session = get_db()
        
        try:
            user = session.query(User).get(user_id)
            if not user:
                return {'error': 'User not found'}
            
            # Update allowed fields
            allowed_fields = ['full_name', 'company_name', 'phone', 'plan']
            for field in allowed_fields:
                if field in updates:
                    setattr(user, field, updates[field])
            
            session.commit()
            
            return {'success': True, 'message': 'User updated'}
            
        except Exception as e:
            session.rollback()
            return {'error': str(e)}
        finally:
            session.close()
    
    def change_password(self, user_id: int, old_password: str, new_password: str) -> dict:
        """Change user password"""
        session = get_db()
        
        try:
            user = session.query(User).get(user_id)
            if not user:
                return {'error': 'User not found'}
            
            # Verify old password
            if not self.verify_password(old_password, user.password_hash):
                return {'error': 'Invalid old password'}
            
            # Hash new password
            user.password_hash = self.hash_password(new_password)
            session.commit()
            
            return {'success': True, 'message': 'Password changed'}
            
        except Exception as e:
            session.rollback()
            return {'error': str(e)}
        finally:
            session.close()


def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'No token provided'}), 401
        
        # Remove 'Bearer ' prefix if present
        if token.startswith('Bearer '):
            token = token[7:]
        
        auth = AuthManager()
        result = auth.verify_token(token)
        
        if 'error' in result:
            return jsonify({'error': result['error']}), 401
        
        # Add user info to request
        request.current_user = result['payload']
        
        return f(*args, **kwargs)
    
    return decorated


def require_role(role: str):
    """Decorator to require specific role"""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not hasattr(request, 'current_user'):
                return jsonify({'error': 'Unauthorized'}), 401
            
            if request.current_user['role'] != role and request.current_user['role'] != 'admin':
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            return f(*args, **kwargs)
        
        return decorated
    return decorator


def create_auth_manager():
    """Create auth manager instance"""
    return AuthManager()


if __name__ == '__main__':
    # Test authentication
    from src.database import init_database
    
    print("Initializing...")
    init_database()
    
    auth = create_auth_manager()
    
    # Create test user
    print("\n📝 Creating test user...")
    result = auth.create_user(
        email='ragsproai@gmail.com',
        password='test123',
        full_name='Raghav Shah',
        company_name='RagsPro',
        role='admin'
    )
    
    if 'success' in result:
        print(f"✅ User created: {result['email']}")
        
        # Test authentication
        print("\n🔐 Testing authentication...")
        auth_result = auth.authenticate('ragsproai@gmail.com', 'test123')
        
        if 'success' in auth_result:
            print(f"✅ Authentication successful")
            print(f"   Token: {auth_result['token'][:50]}...")
            print(f"   User: {auth_result['user']['full_name']}")
            
            # Test token verification
            print("\n🔍 Verifying token...")
            verify_result = auth.verify_token(auth_result['token'])
            
            if 'success' in verify_result:
                print(f"✅ Token valid")
                print(f"   User ID: {verify_result['payload']['user_id']}")
                print(f"   Role: {verify_result['payload']['role']}")
        else:
            print(f"❌ Authentication failed: {auth_result.get('error')}")
    else:
        print(f"⚠️ User creation: {result.get('error')}")
