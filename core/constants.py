"""Core constants for Atlas AI application"""

from enum import Enum


class UserStatusChoices(str, Enum):
    """User status choices"""
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    BANNED = 'banned'
    ONBOARDING = 'onboarding'


class NotificationTypeChoices(str, Enum):
    """Notification type choices"""
    MORNING_BRIEFING = 'morning_briefing'
    EVENING_SUMMARY = 'evening_summary'
    WEEKLY_DIGEST = 'weekly_digest'
    BREAKING_NEWS = 'breaking_news'
    PRICE_ALERT = 'price_alert'
    CUSTOM = 'custom'


class BriefingFrequencyChoices(str, Enum):
    """Briefing frequency choices"""
    DAILY = 'daily'
    WEEKLY = 'weekly'
    NEVER = 'never'


class ConversationStatusChoices(str, Enum):
    """Conversation status choices"""
    ACTIVE = 'active'
    CLOSED = 'closed'
    ARCHIVED = 'archived'


# Telegram Bot Commands
TELEGRAM_COMMANDS = {
    'start': 'Onboarding and initialization',
    'help': 'Help and available commands',
    'brief': 'Get instant briefing',
    'add_interest': 'Add new interests',
    'settings': 'Manage preferences',
    'news': 'Get latest financial news',
    'insights': 'Get market insights',
    'portfolio': 'View tracked portfolio',
    'alerts': 'Manage price alerts',
    'about': 'About the assistant',
}

# Finance Industries
FINANCE_INDUSTRIES = [
    'Technology',
    'Finance',
    'Healthcare',
    'Retail',
    'Energy',
    'Transportation',
    'Real Estate',
    'Manufacturing',
    'Telecommunications',
    'Consumer Goods',
    'Cryptocurrency',
    'Stocks',
    'Forex',
    'Commodities',
]

# Default User Interests
DEFAULT_INTERESTS = [
    'Stock Market',
    'Cryptocurrency',
    'Tech News',
    'Economic News',
    'Market Analysis',
    'Company News',
]

# API Timeouts
API_TIMEOUT_SECONDS = 30
LLM_TIMEOUT_SECONDS = 60
NEWS_API_TIMEOUT = 30

# Cache TTL (Time To Live) in seconds
NEWS_CACHE_TTL = 3600  # 1 hour
STOCK_CACHE_TTL = 300  # 5 minutes
USER_PROFILE_CACHE_TTL = 1800  # 30 minutes
CONVERSATION_CONTEXT_TTL = 86400  # 24 hours

# Message Limits
MAX_MESSAGE_LENGTH = 4096  # Telegram limit
MAX_CONVERSATION_HISTORY = 50  # Number of messages to keep in context
MAX_NEWS_ITEMS_PER_BRIEFING = 10

# LLM Configuration
LLM_MAX_RETRIES = 3
LLM_RETRY_DELAY = 2  # seconds

# Briefing Times (in 24-hour format)
DEFAULT_MORNING_BRIEFING_HOUR = 8  # 8 AM
DEFAULT_EVENING_BRIEFING_HOUR = 17  # 5 PM
DEFAULT_WEEKLY_BRIEFING_DAY = 'monday'
DEFAULT_WEEKLY_BRIEFING_HOUR = 9  # 9 AM

# Pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# Message Types
MESSAGE_TYPE_USER = 'user'
MESSAGE_TYPE_ASSISTANT = 'assistant'
MESSAGE_TYPE_SYSTEM = 'system'
