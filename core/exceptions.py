"""Core exceptions for Atlas AI application"""


class AtlasAIException(Exception):
    """Base exception for Atlas AI"""
    pass


class TelegramException(AtlasAIException):
    """Telegram bot related exceptions"""
    pass


class TelegramWebhookException(TelegramException):
    """Telegram webhook related exceptions"""
    pass


class TelegramMessageException(TelegramException):
    """Telegram message sending exceptions"""
    pass


class AIException(AtlasAIException):
    """AI and LLM related exceptions"""
    pass


class LLMAPIException(AIException):
    """LLM API call exceptions"""
    pass


class PromptException(AIException):
    """Prompt generation exceptions"""
    pass


class FinanceException(AtlasAIException):
    """Finance related exceptions"""
    pass


class NewsAPIException(FinanceException):
    """News API related exceptions"""
    pass


class StockAPIException(FinanceException):
    """Stock API related exceptions"""
    pass


class IntegrationException(AtlasAIException):
    """Integration related exceptions"""
    pass


class GmailException(IntegrationException):
    """Gmail integration exceptions"""
    pass


class GoogleCalendarException(IntegrationException):
    """Google Calendar integration exceptions"""
    pass


class SchedulerException(AtlasAIException):
    """Scheduler related exceptions"""
    pass


class NotificationException(AtlasAIException):
    """Notification related exceptions"""
    pass


class ValidationException(AtlasAIException):
    """Data validation exceptions"""
    pass
