"""
Database models and connection management
Supports both SQLite (dev) and PostgreSQL (production)
"""

import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, JSON
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, scoped_session
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)

Base = declarative_base()


# Database Models

class Lead(Base):
    """Lead model with all details"""
    __tablename__ = 'leads'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    type = Column(String(200))
    address = Column(Text)
    city = Column(String(200))
    rating = Column(Float)
    reviews = Column(Integer)
    phone = Column(String(50))
    website = Column(String(500))
    email = Column(String(200))
    quality_score = Column(Integer)
    status = Column(String(50), default='New')
    notes = Column(Text)
    
    # Tracking
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_contacted = Column(DateTime)
    
    # Outreach tracking
    email_sent = Column(Boolean, default=False)
    whatsapp_sent = Column(Boolean, default=False)
    email_opened = Column(Boolean, default=False)
    email_replied = Column(Boolean, default=False)
    
    # Metadata
    search_query = Column(String(500))
    search_city = Column(String(200))
    search_category = Column(String(200))
    raw_data = Column(JSON)  # Store original scraped data
    
    # Relationships
    follow_ups = relationship("FollowUp", back_populates="lead", cascade="all, delete-orphan")
    interactions = relationship("Interaction", back_populates="lead", cascade="all, delete-orphan")
    analytics = relationship("LeadAnalytics", back_populates="lead", uselist=False, cascade="all, delete-orphan")
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'type': self.type,
            'address': self.address,
            'city': self.city,
            'rating': self.rating,
            'reviews': self.reviews,
            'phone': self.phone,
            'website': self.website,
            'email': self.email,
            'quality_score': self.quality_score,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_contacted': self.last_contacted.isoformat() if self.last_contacted else None,
            'email_sent': self.email_sent,
            'whatsapp_sent': self.whatsapp_sent,
            'email_opened': self.email_opened,
            'email_replied': self.email_replied,
        }


class FollowUp(Base):
    """Follow-up schedule and tracking"""
    __tablename__ = 'follow_ups'
    
    id = Column(Integer, primary_key=True)
    lead_id = Column(Integer, ForeignKey('leads.id'), nullable=False)
    
    sequence_number = Column(Integer, default=1)  # 1st, 2nd, 3rd follow-up
    scheduled_at = Column(DateTime, nullable=False)
    sent_at = Column(DateTime)
    status = Column(String(50), default='Pending')  # Pending, Sent, Skipped
    
    channel = Column(String(50))  # Email, WhatsApp, SMS
    subject = Column(String(500))
    content = Column(Text)
    
    # Response tracking
    opened = Column(Boolean, default=False)
    replied = Column(Boolean, default=False)
    reply_content = Column(Text)
    reply_sentiment = Column(String(50))  # Positive, Neutral, Negative
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    lead = relationship("Lead", back_populates="follow_ups")


class Interaction(Base):
    """Track all interactions with leads"""
    __tablename__ = 'interactions'
    
    id = Column(Integer, primary_key=True)
    lead_id = Column(Integer, ForeignKey('leads.id'), nullable=False)
    
    type = Column(String(50))  # Email, WhatsApp, Call, Meeting
    direction = Column(String(20))  # Outbound, Inbound
    subject = Column(String(500))
    content = Column(Text)
    
    # Response tracking
    opened = Column(Boolean, default=False)
    clicked = Column(Boolean, default=False)
    replied = Column(Boolean, default=False)
    
    # AI Classification
    sentiment = Column(String(50))  # Positive, Neutral, Negative
    intent = Column(String(50))  # Interested, NotNow, Budget, SendDetails, Spam
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    lead = relationship("Lead", back_populates="interactions")


class LeadAnalytics(Base):
    """Analytics data per lead"""
    __tablename__ = 'lead_analytics'
    
    id = Column(Integer, primary_key=True)
    lead_id = Column(Integer, ForeignKey('leads.id'), nullable=False, unique=True)
    
    # Engagement metrics
    total_emails_sent = Column(Integer, default=0)
    total_emails_opened = Column(Integer, default=0)
    total_emails_clicked = Column(Integer, default=0)
    total_emails_replied = Column(Integer, default=0)
    
    total_whatsapp_sent = Column(Integer, default=0)
    total_whatsapp_replied = Column(Integer, default=0)
    
    # Conversion tracking
    first_contact_date = Column(DateTime)
    last_contact_date = Column(DateTime)
    response_time_hours = Column(Float)  # Time to first response
    
    # AI Scoring
    engagement_score = Column(Integer, default=0)  # 0-100
    conversion_probability = Column(Float, default=0.0)  # 0.0-1.0
    predicted_value = Column(Float)  # Predicted deal value
    
    # Status
    is_hot_lead = Column(Boolean, default=False)
    is_warm_lead = Column(Boolean, default=False)
    is_cold_lead = Column(Boolean, default=True)
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    lead = relationship("Lead", back_populates="analytics")


class Campaign(Base):
    """Email/WhatsApp campaigns"""
    __tablename__ = 'campaigns'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Campaign settings
    channel = Column(String(50))  # Email, WhatsApp, Multi
    template_id = Column(Integer)
    
    # Targeting
    target_cities = Column(JSON)
    target_categories = Column(JSON)
    min_quality_score = Column(Integer)
    
    # Status
    status = Column(String(50), default='Draft')  # Draft, Active, Paused, Completed
    
    # Stats
    total_leads = Column(Integer, default=0)
    sent_count = Column(Integer, default=0)
    opened_count = Column(Integer, default=0)
    replied_count = Column(Integer, default=0)
    converted_count = Column(Integer, default=0)
    
    # Timing
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    
    created_by = Column(Integer)  # User ID (for multi-user support)


class Template(Base):
    """Email/WhatsApp templates"""
    __tablename__ = 'templates'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    type = Column(String(50))  # Email, WhatsApp, SMS
    
    subject = Column(String(500))  # For emails
    content = Column(Text, nullable=False)
    
    # A/B Testing
    variant = Column(String(10))  # A, B, C
    parent_template_id = Column(Integer)  # For variants
    
    # Performance
    times_used = Column(Integer, default=0)
    open_rate = Column(Float, default=0.0)
    reply_rate = Column(Float, default=0.0)
    conversion_rate = Column(Float, default=0.0)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_default = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class User(Base):
    """User accounts (for multi-user support)"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(200), unique=True, nullable=False)
    password_hash = Column(String(500))
    
    # Profile
    full_name = Column(String(200))
    company_name = Column(String(200))
    phone = Column(String(50))
    
    # Role & Permissions
    role = Column(String(50), default='user')  # admin, user, viewer
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Subscription (for SaaS)
    plan = Column(String(50), default='free')  # free, starter, pro, agency
    subscription_status = Column(String(50), default='active')
    subscription_ends_at = Column(DateTime)
    
    # Limits
    monthly_leads_limit = Column(Integer, default=500)
    monthly_emails_limit = Column(Integer, default=1000)
    
    # Tracking
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login_at = Column(DateTime)


# Database Connection Management

class DatabaseManager:
    """Manage database connections"""
    
    def __init__(self, database_url=None):
        """Initialize database connection"""
        if database_url is None:
            # Default to SQLite for development
            database_url = os.getenv('DATABASE_URL', 'sqlite:///data/rcas.db')
        
        # Handle PostgreSQL URL format
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        
        self.engine = create_engine(
            database_url,
            echo=False,
            pool_pre_ping=True,
            pool_recycle=3600
        )
        
        self.Session = scoped_session(sessionmaker(bind=self.engine))
        logger.info(f"Database initialized: {database_url.split('@')[-1] if '@' in database_url else database_url}")
    
    def create_tables(self):
        """Create all tables"""
        Base.metadata.create_all(self.engine)
        logger.info("Database tables created")
    
    def drop_tables(self):
        """Drop all tables (use with caution!)"""
        Base.metadata.drop_all(self.engine)
        logger.info("Database tables dropped")
    
    @contextmanager
    def session_scope(self):
        """Provide a transactional scope"""
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            session.close()
    
    def get_session(self):
        """Get a new session"""
        return self.Session()


# Global database instance
db_manager = None


def init_database(database_url=None):
    """Initialize global database"""
    global db_manager
    db_manager = DatabaseManager(database_url)
    db_manager.create_tables()
    return db_manager


def get_db():
    """Get database session"""
    if db_manager is None:
        init_database()
    return db_manager.get_session()


# Migration utilities

def migrate_json_to_db(json_file='data/premium_leads.json'):
    """Migrate existing JSON data to database"""
    import json
    
    if not os.path.exists(json_file):
        logger.warning(f"JSON file not found: {json_file}")
        return 0
    
    with open(json_file, 'r', encoding='utf-8') as f:
        leads_data = json.load(f)
    
    session = get_db()
    migrated = 0
    
    try:
        for lead_data in leads_data:
            # Check if lead already exists
            existing = session.query(Lead).filter_by(
                title=lead_data.get('title'),
                address=lead_data.get('address')
            ).first()
            
            if existing:
                continue
            
            # Create new lead
            lead = Lead(
                title=lead_data.get('title'),
                type=lead_data.get('type'),
                address=lead_data.get('address'),
                city=lead_data.get('search_city'),
                rating=lead_data.get('rating'),
                reviews=lead_data.get('reviews'),
                phone=lead_data.get('phone'),
                website=lead_data.get('website'),
                email=lead_data.get('email'),
                quality_score=lead_data.get('quality_score'),
                status=lead_data.get('status', 'New'),
                notes=lead_data.get('notes'),
                email_sent=lead_data.get('email_sent', False),
                whatsapp_sent=lead_data.get('whatsapp_sent', False),
                search_query=lead_data.get('search_query'),
                search_city=lead_data.get('search_city'),
                search_category=lead_data.get('search_category'),
                raw_data=lead_data
            )
            
            session.add(lead)
            
            # Create analytics record
            analytics = LeadAnalytics(lead=lead)
            session.add(analytics)
            
            migrated += 1
        
        session.commit()
        logger.info(f"Migrated {migrated} leads from JSON to database")
        return migrated
        
    except Exception as e:
        session.rollback()
        logger.error(f"Migration error: {e}")
        raise
    finally:
        session.close()


if __name__ == '__main__':
    # Test database setup
    print("Initializing database...")
    init_database()
    print("✅ Database initialized")
    
    # Test migration
    print("\nMigrating JSON data...")
    count = migrate_json_to_db()
    print(f"✅ Migrated {count} leads")
    
    # Test query
    session = get_db()
    total_leads = session.query(Lead).count()
    print(f"\n📊 Total leads in database: {total_leads}")
    session.close()
