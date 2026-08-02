import logging
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.exceptions import AtlasAIException

logger = logging.getLogger(__name__)


class BaseAPIView(APIView):
    """Base API view with common functionality"""
    
    def handle_exception(self, exc):
        """Handle exceptions and return appropriate response"""
        if isinstance(exc, AtlasAIException):
            logger.error(f'API Exception: {str(exc)}')
            return Response(
                {'error': str(exc)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        logger.error(f'Unexpected error: {str(exc)}', exc_info=True)
        return Response(
            {'error': 'Internal server error'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class PaginatedAPIView(BaseAPIView):
    """Base API view with pagination support"""
    
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100
    
    def get_pagination_params(self):
        """Extract pagination parameters from request"""
        page = int(self.request.query_params.get('page', 1))
        page_size = int(self.request.query_params.get('page_size', self.DEFAULT_PAGE_SIZE))
        
        # Validate page_size
        if page_size > self.MAX_PAGE_SIZE:
            page_size = self.MAX_PAGE_SIZE
        if page_size < 1:
            page_size = self.DEFAULT_PAGE_SIZE
        if page < 1:
            page = 1
        
        offset = (page - 1) * page_size
        return offset, page_size, page
    
    def get_paginated_response(self, data, total_count, page, page_size):
        """Return paginated response"""
        total_pages = (total_count + page_size - 1) // page_size
        
        return Response({
            'results': data,
            'pagination': {
                'total_count': total_count,
                'page': page,
                'page_size': page_size,
                'total_pages': total_pages,
                'has_next': page < total_pages,
                'has_previous': page > 1
            }
        })
