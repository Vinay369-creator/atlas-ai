# Custom exceptions for the application


class AtlasAIException(Exception):
    """Base exception for Atlas AI"""
    pass


class LLMAPIException(AtlasAIException):
    """Exception for LLM API errors"""
    pass


class AIException(AtlasAIException):
    """Exception for AI service errors"""
    pass


class AuthenticationException(AtlasAIException):
    """Exception for authentication errors"""
    pass


class AuthorizationException(AtlasAIException):
    """Exception for authorization errors"""
    pass


class ValidationException(AtlasAIException):
    """Exception for validation errors"""
    pass


class DataNotFound(AtlasAIException):
    """Exception when data is not found"""
    pass


class ExternalAPIException(AtlasAIException):
    """Exception for external API errors"""
    pass


class RateLimitException(AtlasAIException):
    """Exception for rate limit errors"""
    pass


class InternalException(AtlasAIException):
    """Exception for internal server errors"""
    pass
