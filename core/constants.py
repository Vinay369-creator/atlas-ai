from enum import Enum
from datetime import timedelta


class ConversationStatusChoices(Enum):
    """Conversation status choices"""
    ACTIVE = 'active'
    CLOSED = 'closed'
    ARCHIVED = 'archived'


class UserRoleChoices(Enum):
    """User role choices"""
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'


# Message types
MESSAGE_TYPE_USER = 'user'
MESSAGE_TYPE_ASSISTANT = 'assistant'
MESSAGE_TYPE_SYSTEM = 'system'

# LLM Configuration
LLM_MAX_RETRIES = 3
LLM_RETRY_DELAY = 2  # seconds
LLM_REQUEST_TIMEOUT = 60  # seconds

# Cache configuration
CACHE_TIMEOUT_SHORT = 300  # 5 minutes
CACHE_TIMEOUT_MEDIUM = 1800  # 30 minutes
CACHE_TIMEOUT_LONG = 3600  # 1 hour
CACHE_TIMEOUT_DAILY = 86400  # 24 hours

# Pagination
PAGINATION_DEFAULT_LIMIT = 20
PAGINATION_MAX_LIMIT = 100

# Rate limiting
RATE_LIMIT_MESSAGES_PER_MINUTE = 10
RATE_LIMIT_REQUESTS_PER_HOUR = 100

# User activity
USER_ACTIVITY_TIMEOUT = timedelta(days=30)  # Mark as inactive after 30 days
LAST_ACTIVITY_UPDATE_THRESHOLD = timedelta(minutes=5)  # Update activity every 5 mins

# Briefing configuration
DEFAULT_BRIEFING_TIME = '09:00'  # 9 AM
BRIEFING_TIMEZONE = 'UTC'

# API limits
MAX_CONVERSATION_LENGTH = 10000  # messages per conversation
MAX_MESSAGE_LENGTH = 4096  # characters

# Financial data constants
DEFAULT_CURRENCY = 'USD'
DEFAULT_MARKET = 'US'
STOCK_DATA_CACHE_DURATION = 3600  # 1 hour
NEWS_DATA_CACHE_DURATION = 1800  # 30 minutes

# AI Model defaults
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 2048
DEFAULT_TOP_P = 0.9
