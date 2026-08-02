from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class SecurityMiddleware:
    """Security middleware for request/response handling"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Add security headers
        response = self.get_response(request)
        
        # Security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        return response


class LoggingMiddleware:
    """Logging middleware for request tracking"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        logger.info(
            f'Request: {request.method} {request.path} from {request.META.get("REMOTE_ADDR")}'
        )
        
        response = self.get_response(request)
        
        logger.info(
            f'Response: {response.status_code} for {request.method} {request.path}'
        )
        
        return response


class ExceptionMiddleware:
    """Middleware for exception handling"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Exception as e:
            logger.error(f'Exception: {str(e)}', exc_info=True)
            raise
        
        return response
