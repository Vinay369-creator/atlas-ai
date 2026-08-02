"""Decorators for Atlas AI application"""

import logging
import functools
from typing import Callable, Any
from core.exceptions import AtlasAIException

logger = logging.getLogger(__name__)


def handle_exceptions(func: Callable) -> Callable:
    """Decorator to handle exceptions in functions"""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except AtlasAIException as e:
            logger.error(f'Atlas AI Exception in {func.__name__}: {str(e)}')
            raise
        except Exception as e:
            logger.error(f'Unexpected exception in {func.__name__}: {str(e)}')
            raise AtlasAIException(f'Error in {func.__name__}: {str(e)}')
    return wrapper


def log_execution_time(func: Callable) -> Callable:
    """Decorator to log function execution time"""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        import time
        start_time = time.time()
        logger.info(f'Starting {func.__name__}')
        
        try:
            result = func(*args, **kwargs)
            elapsed_time = time.time() - start_time
            logger.info(f'Completed {func.__name__} in {elapsed_time:.2f}s')
            return result
        except Exception as e:
            elapsed_time = time.time() - start_time
            logger.error(f'Failed {func.__name__} after {elapsed_time:.2f}s: {str(e)}')
            raise
    return wrapper


def require_telegram_user(func: Callable) -> Callable:
    """Decorator to require Telegram user authentication"""
    @functools.wraps(func)
    def wrapper(request: Any, *args: Any, **kwargs: Any) -> Any:
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            from django.http import JsonResponse
            return JsonResponse({'error': 'Authentication required'}, status=401)
        return func(request, *args, **kwargs)
    return wrapper


def rate_limit(calls: int, period: int) -> Callable:
    """Decorator for rate limiting"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Implementation would use Redis for actual rate limiting
            return func(*args, **kwargs)
        return wrapper
    return decorator
