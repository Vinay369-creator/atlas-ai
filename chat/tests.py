from django.test import TestCase
from django.contrib.auth.models import User
from chat.models import Conversation, Message, ConversationAnalytics
from chat.services import ConversationService, MessageService, AnalyticsService


class ConversationServiceTestCase(TestCase):
    """Test cases for ConversationService"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com'
        )
    
    def test_create_conversation(self):
        """Test creating a conversation"""
        conversation = ConversationService.create_conversation(
            user=self.user,
            title='Test Conversation'
        )
        
        self.assertIsNotNone(conversation.id)
        self.assertEqual(conversation.user, self.user)
        self.assertEqual(conversation.title, 'Test Conversation')
        self.assertTrue(hasattr(conversation, 'analytics'))
    
    def test_add_message(self):
        """Test adding message to conversation"""
        conversation = ConversationService.create_conversation(
            user=self.user
        )
        
        message = ConversationService.add_message(
            conversation=conversation,
            role='user',
            content='Hello'
        )
        
        self.assertEqual(message.role, 'user')
        self.assertEqual(message.content, 'Hello')
        self.assertEqual(message.conversation, conversation)
    
    def test_get_conversation_context(self):
        """Test getting conversation context"""
        conversation = ConversationService.create_conversation(
            user=self.user
        )
        
        ConversationService.add_message(conversation, 'user', 'Hello')
        ConversationService.add_message(conversation, 'assistant', 'Hi there!')
        
        context = ConversationService.get_conversation_context(conversation)
        
        self.assertEqual(len(context), 2)
        self.assertEqual(context[0]['role'], 'user')
        self.assertEqual(context[1]['role'], 'assistant')
    
    def test_close_conversation(self):
        """Test closing conversation"""
        conversation = ConversationService.create_conversation(
            user=self.user
        )
        
        ConversationService.close_conversation(conversation)
        
        conversation.refresh_from_db()
        self.assertEqual(conversation.status, 'closed')


class AnalyticsServiceTestCase(TestCase):
    """Test cases for AnalyticsService"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com'
        )
    
    def test_get_user_analytics(self):
        """Test getting user analytics"""
        conversation = ConversationService.create_conversation(
            user=self.user
        )
        
        ConversationService.add_message(conversation, 'user', 'Hello')
        ConversationService.add_message(conversation, 'assistant', 'Hi')
        
        analytics = AnalyticsService.get_user_analytics(self.user)
        
        self.assertEqual(analytics['total_conversations'], 1)
        self.assertEqual(analytics['total_messages'], 2)
