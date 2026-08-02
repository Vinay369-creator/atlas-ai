from django.utils.decorators import decorator_from_middleware
from core.middleware import SecurityMiddleware, LoggingMiddleware, ExceptionMiddleware
import functools
import logging
from django.http import JsonResponse
from core.exceptions import (
    AuthenticationException,
    AuthorizationException,
    ValidationException,
    RateLimitException,
    InternalException
)

logger = logging.getLogger(__name__)


def authenticate_required(view_func):
    """Decorator to require authentication"""
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise AuthenticationException('User is not authenticated')
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    """Decorator to require admin access"""
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            raise AuthorizationException('Admin access required')
        return view_func(request, *args, **kwargs)
    return wrapper


def handle_exceptions(view_func):
    """Decorator to handle exceptions"""
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except AuthenticationException as e:
            logger.warning(f'Authentication error: {str(e)}')
            return JsonResponse({'error': str(e)}, status=401)
        except AuthorizationException as e:
            logger.warning(f'Authorization error: {str(e)}')
            return JsonResponse({'error': str(e)}, status=403)
        except ValidationException as e:
            logger.warning(f'Validation error: {str(e)}')
            return JsonResponse({'error': str(e)}, status=400)
        except RateLimitException as e:
            logger.warning(f'Rate limit error: {str(e)}')
            return JsonResponse({'error': str(e)}, status=429)
        except Exception as e:
            logger.error(f'Unexpected error: {str(e)}', exc_info=True)
            return JsonResponse({'error': 'Internal server error'}, status=500)
    return wrapper
