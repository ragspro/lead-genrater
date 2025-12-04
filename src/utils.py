"""
Shared utility functions used across multiple modules
Refactored to eliminate code duplication
"""

import logging
from datetime import datetime
from pathlib import Path
import json
from typing import Dict, Any


def setup_logging(log_dir: str = "logs", log_level: int = logging.INFO) -> logging.Logger:
    """
    Set up logging with ISO 8601 timestamps
    
    Args:
        log_dir: Directory to store log files
        log_level: Logging level (default: INFO)
    
    Returns:
        Configured logger instance
    """
    # Create logs directory if it doesn't exist
    Path(log_dir).mkdir(exist_ok=True)
    
    # Create log filename with date
    log_filename = f"{log_dir}/lead_gen_{datetime.now().strftime('%Y%m%d')}.log"
    
    # Configure logging
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s [%(levelname)s] %(name)s - %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized - {log_filename}")
    
    return logger


def save_ai_content(leads: list, content_type: str = "email", output_dir: str = "data") -> str:
    """
    Save AI-generated content to JSON file
    
    Args:
        leads: List of leads with AI content
        content_type: Type of content ("email" or "whatsapp")
        output_dir: Directory to save files
    
    Returns:
        Path to saved file
    """
    try:
        # Create output directory
        Path(output_dir).mkdir(exist_ok=True)
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{output_dir}/ai_{content_type}_{timestamp}.json"
        
        # Save to file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(leads, f, indent=2, ensure_ascii=False)
        
        logging.info(f"Saved {len(leads)} {content_type} contents to {filename}")
        return filename
        
    except Exception as e:
        logging.error(f"Error saving AI content: {str(e)}")
        raise


def save_whatsapp_conversations(conversations: list, output_dir: str = "data") -> str:
    """
    Save WhatsApp conversations to JSON file
    
    Args:
        conversations: List of WhatsApp conversations
        output_dir: Directory to save files
    
    Returns:
        Path to saved file
    """
    try:
        # Create output directory
        Path(output_dir).mkdir(exist_ok=True)
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{output_dir}/whatsapp_conversations_{timestamp}.json"
        
        # Save to file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(conversations, f, indent=2, ensure_ascii=False)
        
        logging.info(f"Saved {len(conversations)} WhatsApp conversations to {filename}")
        return filename
        
    except Exception as e:
        logging.error(f"Error saving WhatsApp conversations: {str(e)}")
        raise


def get_config(config_path: str = "config/settings.json") -> Dict[str, Any]:
    """
    Load configuration from JSON file
    
    Args:
        config_path: Path to configuration file
    
    Returns:
        Configuration dictionary
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        logging.error(f"Configuration file not found: {config_path}")
        raise
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON in configuration file: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"Error loading configuration: {str(e)}")
        raise


def format_timestamp(dt: datetime = None) -> str:
    """
    Format datetime as ISO 8601 timestamp
    
    Args:
        dt: Datetime object (default: now)
    
    Returns:
        ISO 8601 formatted timestamp string
    """
    if dt is None:
        dt = datetime.now()
    return dt.isoformat()


def ensure_directory(path: str) -> Path:
    """
    Ensure directory exists, create if it doesn't
    
    Args:
        path: Directory path
    
    Returns:
        Path object
    """
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def safe_get(dictionary: dict, key: str, default: Any = None) -> Any:
    """
    Safely get value from dictionary with default
    
    Args:
        dictionary: Dictionary to get value from
        key: Key to look up
        default: Default value if key not found
    
    Returns:
        Value or default
    """
    return dictionary.get(key, default)


def truncate_string(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate string to maximum length
    
    Args:
        text: String to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
    
    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix
