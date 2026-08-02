"""Utility functions for Atlas AI application"""

import logging
import hashlib
import hmac
import json
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple
import requests
from django.conf import settings
from core.constants import API_TIMEOUT_SECONDS

logger = logging.getLogger(__name__)


def sanitize_input(text: str, max_length: int = 4096) -> str:
    """Sanitize user input"""
    if not isinstance(text, str):
        return ""
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    # Limit length
    if len(text) > max_length:
        text = text[:max_length]
    
    return text


def truncate_text(text: str, max_length: int = 4096) -> str:
    """Truncate text to maximum length"""
    if len(text) > max_length:
        return text[:max_length-3] + '...'
    return text


def format_currency(amount: float, currency: str = 'USD') -> str:
    """Format amount as currency"""
    if currency.upper() == 'USD':
        return f'${amount:,.2f}'
    return f'{amount:,.2f} {currency}'


def calculate_time_ago(date: datetime) -> str:
    """Calculate human-readable time difference"""
    now = datetime.now()
    diff = now - date
    
    seconds = int(diff.total_seconds())
    
    if seconds < 60:
        return f'{seconds}s ago'
    elif seconds < 3600:
        minutes = seconds // 60
        return f'{minutes}m ago'
    elif seconds < 86400:
        hours = seconds // 3600
        return f'{hours}h ago'
    else:
        days = seconds // 86400
        return f'{days}d ago'


def verify_telegram_webhook_signature(token: str, body: bytes) -> bool:
    """Verify Telegram webhook signature"""
    secret_key = hashlib.sha256(token.encode()).digest()
    signature = hmac.new(
        secret_key,
        body,
        hashlib.sha256
    ).hexdigest()
    return signature


def parse_telegram_update(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Parse Telegram update data"""
    try:
        if 'message' in data:
            return {
                'type': 'message',
                'update_id': data.get('update_id'),
                'data': data.get('message')
            }
        elif 'callback_query' in data:
            return {
                'type': 'callback_query',
                'update_id': data.get('update_id'),
                'data': data.get('callback_query')
            }
    except Exception as e:
        logger.error(f'Error parsing Telegram update: {str(e)}')
    
    return None


def make_api_request(
    method: str,
    url: str,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Any]] = None,
    json_data: Optional[Dict[str, Any]] = None,
    timeout: int = API_TIMEOUT_SECONDS,
    retries: int = 3
) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
    """Make HTTP API request with retry logic"""
    
    for attempt in range(retries):
        try:
            if method.upper() == 'GET':
                response = requests.get(
                    url,
                    headers=headers,
                    params=params,
                    timeout=timeout
                )
            elif method.upper() == 'POST':
                response = requests.post(
                    url,
                    headers=headers,
                    params=params,
                    json=json_data,
                    timeout=timeout
                )
            else:
                return False, None, f'Unsupported HTTP method: {method}'
            
            response.raise_for_status()
            return True, response.json(), None
            
        except requests.exceptions.Timeout:
            error = f'Request timeout (attempt {attempt + 1}/{retries})'
            logger.warning(error)
            if attempt == retries - 1:
                return False, None, error
        except requests.exceptions.RequestException as e:
            error = f'Request failed: {str(e)}'
            logger.error(error)
            if attempt == retries - 1:
                return False, None, error
        except json.JSONDecodeError as e:
            error = f'Invalid JSON response: {str(e)}'
            logger.error(error)
            return False, None, error
    
    return False, None, 'Max retries exceeded'


def chunk_text(text: str, chunk_size: int = 4096) -> List[str]:
    """Split text into chunks"""
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])
    return chunks


def format_markdown(text: str) -> str:
    """Format text for Telegram markdown"""
    # Escape special characters
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    return text


def parse_json_safe(json_str: str, default: Dict[str, Any] = None) -> Dict[str, Any]:
    """Safely parse JSON string"""
    if default is None:
        default = {}
    
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError) as e:
        logger.warning(f'Failed to parse JSON: {str(e)}')
        return default


def get_greeting_message() -> str:
    """Get appropriate greeting based on time of day"""
    hour = datetime.now().hour
    
    if hour < 12:
        return "Good morning! 🌅"
    elif hour < 17:
        return "Good afternoon! 🌤️"
    else:
        return "Good evening! 🌙"


def format_conversation_context(messages: List[Dict[str, str]]) -> str:
    """Format conversation context for LLM"""
    context = ""
    for msg in messages:
        role = msg.get('role', 'user').upper()
        content = msg.get('content', '')
        context += f"{role}: {content}\n\n"
    return context.strip()
