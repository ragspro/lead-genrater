"""Google Sheets Integration for RagsPro Lead Generator."""

import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from typing import List, Dict
import os

logger = logging.getLogger(__name__)

class GoogleSheetsSync:
    """Handles syncing leads to Google Sheets."""
    
    def __init__(self, credentials_path: str, sheet_id: str):
        """
        Initialize Google Sheets connection.
        
        Args:
            credentials_path: Path to service account JSON
            sheet_id: Google Sheet ID (from URL)
        """
        self.credentials_path = credentials_path
        self.sheet_id = sheet_id
        self.client = None
        self.sheet = None
        
        # Scope required for API access
        self.scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"
        ]
        
    def connect(self) -> bool:
        """Connect to Google Sheets API."""
        try:
            if not os.path.exists(self.credentials_path):
                logger.error(f"Credentials file not found: {self.credentials_path}")
                return False
                
            creds = ServiceAccountCredentials.from_json_keyfile_name(
                self.credentials_path, self.scope
            )
            self.client = gspread.authorize(creds)
            self.sheet = self.client.open_by_key(self.sheet_id)
            logger.info("✅ Connected to Google Sheets")
            return True
        except Exception as e:
            logger.error(f"❌ Google Sheets connection error: {e}")
            return False
            
    def get_or_create_daily_worksheet(self):
        """Get today's worksheet or create it if missing."""
        if not self.client:
            if not self.connect():
                return None
                
        today_str = datetime.now().strftime('%Y-%m-%d')
        worksheet_title = f"Leads_{today_str}"
        
        try:
            # Try to open existing worksheet
            worksheet = self.sheet.worksheet(worksheet_title)
            return worksheet
        except gspread.WorksheetNotFound:
            # Create new worksheet
            try:
                worksheet = self.sheet.add_worksheet(title=worksheet_title, rows=1000, cols=10)
                # Add headers
                headers = [
                    "Business Name", "Type", "Location", "Rating", 
                    "Reviews", "Phone", "Website", "Quality Score", 
                    "Status", "AI Email", "AI WhatsApp"
                ]
                worksheet.append_row(headers)
                # Format headers (bold)
                worksheet.format('A1:K1', {'textFormat': {'bold': True}})
                logger.info(f"Created new worksheet: {worksheet_title}")
                return worksheet
            except Exception as e:
                logger.error(f"Error creating worksheet: {e}")
                return None
        except Exception as e:
            logger.error(f"Error accessing worksheet: {e}")
            return None

    def sync_leads(self, leads: List[Dict]) -> bool:
        """
        Sync new leads to today's worksheet.
        
        Args:
            leads: List of lead dictionaries
            
        Returns:
            True if successful
        """
        worksheet = self.get_or_create_daily_worksheet()
        if not worksheet:
            return False
            
        try:
            # Get existing business names to avoid duplicates
            existing_records = worksheet.get_all_records()
            existing_names = {str(row.get('Business Name', '')).lower() for row in existing_records}
            
            new_rows = []
            for lead in leads:
                name = lead.get('title', '').strip()
                if not name or name.lower() in existing_names:
                    continue
                    
                row = [
                    name,
                    lead.get('type', ''),
                    lead.get('address', ''),
                    lead.get('rating', 0),
                    lead.get('reviews', 0),
                    lead.get('phone', ''),
                    lead.get('website', ''),
                    lead.get('quality_score', 0),
                    lead.get('status', 'New'),
                    lead.get('ai_content', {}).get('email', '')[:500], # Truncate if too long
                    lead.get('ai_content', {}).get('whatsapp', '')[:500]
                ]
                new_rows.append(row)
                existing_names.add(name.lower()) # Add to set to prevent dupes in same batch
            
            if new_rows:
                worksheet.append_rows(new_rows)
                logger.info(f"✅ Synced {len(new_rows)} new leads to Google Sheets")
            else:
                logger.info("No new leads to sync to Google Sheets")
                
            return True
            
        except Exception as e:
            logger.error(f"Error syncing to Google Sheets: {e}")
            return False

def sync_leads_background(leads: List[Dict]):
    """Helper to run sync in background thread."""
    try:
        # Load config to get paths
        from src.config import load_config
        config = load_config()
        
        creds_path = config.get('GOOGLE_SERVICE_ACCOUNT_JSON', 'config/credentials.json')
        sheet_id = config.get('GOOGLE_SHEET_ID')
        
        if not sheet_id:
            logger.warning("Google Sheet ID not configured. Skipping sync.")
            return
            
        syncer = GoogleSheetsSync(creds_path, sheet_id)
        syncer.sync_leads(leads)
        
    except Exception as e:
        logger.error(f"Background sync failed: {e}")
