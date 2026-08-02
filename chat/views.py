from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from chat.models import Conversation, Message, ConversationAnalytics
from chat.serializers import (
    ConversationSerializer,
    ConversationListSerializer,
    MessageSerializer,
    SendMessageSerializer,
    ConversationCreateSerializer,
    ConversationAnalyticsSerializer
)
from chat.services import ConversationService, MessageService, AnalyticsService
import logging

logger = logging.getLogger(__name__)


class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for conversations"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Get user's conversations"""
        return Conversation.objects.filter(user=self.request.user).order_by('-updated_at')
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return ConversationListSerializer
        return ConversationSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Create a new conversation
        """
        serializer = ConversationCreateSerializer(data=request.data)
        if serializer.is_valid():
            conversation = ConversationService.create_conversation(
                user=request.user,
                title=serializer.validated_data.get('title'),
                is_briefing=serializer.validated_data.get('is_briefing', False)
            )
            
            # Add initial message if provided
            initial_message = serializer.validated_data.get('initial_message')
            if initial_message:
                ConversationService.add_message(
                    conversation=conversation,
                    role='user',
                    content=initial_message
                )
            
            return Response(
                ConversationSerializer(conversation).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        """
        Close a conversation
        """
        conversation = self.get_object()
        ConversationService.close_conversation(conversation)
        return Response(
            {'status': 'Conversation closed'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['get'])
    def analytics(self, request, pk=None):
        """
        Get conversation analytics
        """
        conversation = self.get_object()
        if hasattr(conversation, 'analytics'):
            serializer = ConversationAnalyticsSerializer(conversation.analytics)
            return Response(serializer.data)
        return Response(
            {'error': 'No analytics available'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    @action(detail=False, methods=['get'])
    def user_analytics(self, request):
        """
        Get user's overall analytics
        """
        analytics = AnalyticsService.get_user_analytics(request.user)
        return Response(analytics)


class MessageViewSet(viewsets.ModelViewSet):
    """ViewSet for messages"""
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Get user's messages"""
        conversation_id = self.request.query_params.get('conversation_id')
        
        if conversation_id:
            return Message.objects.filter(
                conversation_id=conversation_id,
                conversation__user=self.request.user
            ).order_by('created_at')
        
        return Message.objects.filter(
            conversation__user=self.request.user
        ).order_by('-created_at')
    
    @action(detail=True, methods=['post'])
    def feedback(self, request, pk=None):
        """
        Add feedback to message
        """
        message = self.get_object()
        is_helpful = request.data.get('is_helpful')
        feedback_text = request.data.get('feedback')
        
        if is_helpful is None:
            return Response(
                {'error': 'is_helpful is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        message = MessageService.add_feedback(
            message,
            is_helpful,
            feedback_text
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def search(self, request):
        """
        Search messages
        """
        query = request.data.get('query')
        
        if not query:
            return Response(
                {'error': 'query is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        messages = MessageService.search_messages(request.user, query)
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)
