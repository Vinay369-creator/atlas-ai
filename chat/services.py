from django.contrib.auth.models import User
from chat.models import Conversation, Message, ConversationAnalytics
from typing import List, Dict, Optional, Tuple
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class ConversationService:
    """Service for conversation management"""
    
    @staticmethod
    def create_conversation(
        user: User,
        title: str = None,
        is_briefing: bool = False,
        context: Dict = None
    ) -> Conversation:
        """
        Create a new conversation
        """
        conversation = Conversation.objects.create(
            user=user,
            title=title or f"Conversation {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            is_briefing=is_briefing,
            context=context or {}
        )
        
        # Create associated analytics
        ConversationAnalytics.objects.create(conversation=conversation)
        logger.info(f'Created conversation {conversation.id} for user {user.username}')
        
        return conversation
    
    @staticmethod
    def get_user_conversations(user: User, limit: int = 20) -> List[Conversation]:
        """
        Get user's conversations
        """
        return Conversation.objects.filter(
            user=user,
            status='active'
        ).order_by('-updated_at')[:limit]
    
    @staticmethod
    def get_conversation_by_id(user: User, conversation_id: str) -> Optional[Conversation]:
        """
        Get conversation by ID for user
        """
        try:
            return Conversation.objects.get(
                id=conversation_id,
                user=user
            )
        except Conversation.DoesNotExist:
            return None
    
    @staticmethod
    def add_message(
        conversation: Conversation,
        role: str,
        content: str,
        tokens_used: int = None,
        model: str = None
    ) -> Message:
        """
        Add message to conversation
        """
        message = Message.objects.create(
            conversation=conversation,
            role=role,
            content=content,
            tokens_used=tokens_used,
            model=model
        )
        
        # Update conversation timestamp
        conversation.updated_at = datetime.now()
        conversation.save(update_fields=['updated_at'])
        
        logger.info(f'Added {role} message to conversation {conversation.id}')
        return message
    
    @staticmethod
    def get_conversation_context(
        conversation: Conversation,
        limit: int = 10
    ) -> List[Dict]:
        """
        Get conversation context for LLM
        Returns list of messages in format [{'role': 'user/assistant', 'content': '...'}]
        """
        messages = Message.objects.filter(
            conversation=conversation
        ).order_by('-created_at')[:limit]
        
        # Reverse to get chronological order
        messages = list(reversed(messages))
        
        return [
            {'role': msg.role, 'content': msg.content}
            for msg in messages
        ]
    
    @staticmethod
    def close_conversation(conversation: Conversation) -> None:
        """
        Close conversation
        """
        conversation.close()
        
        # Update analytics
        if hasattr(conversation, 'analytics'):
            conversation.analytics.update_statistics()
        
        logger.info(f'Closed conversation {conversation.id}')
    
    @staticmethod
    def get_recent_conversations(
        user: User,
        hours: int = 24
    ) -> List[Conversation]:
        """
        Get conversations from last N hours
        """
        from django.utils import timezone
        from datetime import timedelta
        
        since = timezone.now() - timedelta(hours=hours)
        return Conversation.objects.filter(
            user=user,
            updated_at__gte=since
        ).order_by('-updated_at')


class MessageService:
    """Service for message management"""
    
    @staticmethod
    def add_feedback(
        message: Message,
        is_helpful: bool,
        feedback_text: str = None
    ) -> Message:
        """
        Add feedback to message
        """
        message.is_helpful = is_helpful
        message.feedback = feedback_text
        message.save()
        
        logger.info(f'Added feedback to message {message.id}')
        return message
    
    @staticmethod
    def get_conversation_messages(
        conversation: Conversation,
        offset: int = 0,
        limit: int = 50
    ) -> List[Message]:
        """
        Get messages from conversation with pagination
        """
        return Message.objects.filter(
            conversation=conversation
        ).order_by('created_at')[offset:offset + limit]
    
    @staticmethod
    def search_messages(
        user: User,
        query: str
    ) -> List[Message]:
        """
        Search messages for user
        """
        return Message.objects.filter(
            conversation__user=user,
            content__icontains=query
        ).order_by('-created_at')


class AnalyticsService:
    """Service for conversation analytics"""
    
    @staticmethod
    def update_analytics(conversation: Conversation) -> None:
        """
        Update conversation analytics
        """
        if not hasattr(conversation, 'analytics'):
            ConversationAnalytics.objects.create(conversation=conversation)
        
        analytics = conversation.analytics
        analytics.update_statistics()
        logger.info(f'Updated analytics for conversation {conversation.id}')
    
    @staticmethod
    def get_user_analytics(user: User) -> Dict:
        """
        Get user's overall analytics
        """
        conversations = Conversation.objects.filter(user=user)
        
        total_conversations = conversations.count()
        total_messages = Message.objects.filter(
            conversation__user=user
        ).count()
        
        analytics_data = {
            'total_conversations': total_conversations,
            'total_messages': total_messages,
            'active_conversations': conversations.filter(status='active').count(),
            'closed_conversations': conversations.filter(status='closed').count(),
        }
        
        return analytics_data
