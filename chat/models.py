from django.db import models
from django.contrib.auth.models import User
from core.constants import ConversationStatusChoices, MESSAGE_TYPE_USER, MESSAGE_TYPE_ASSISTANT
import uuid


class Conversation(models.Model):
    """Conversation/Chat history model"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    title = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[(choice.value, choice.name) for choice in ConversationStatusChoices],
        default=ConversationStatusChoices.ACTIVE.value
    )
    
    # Context and metadata
    context = models.JSONField(default=dict, blank=True, help_text='Conversation context')
    is_briefing = models.BooleanField(default=False, help_text='Is this a briefing conversation')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'conversation'
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['user', '-updated_at']),
            models.Index(fields=['status']),
            models.Index(fields=['is_briefing']),
        ]
    
    def __str__(self):
        return f"Conversation: {self.user.username} - {self.created_at}"
    
    def get_message_count(self) -> int:
        """Get number of messages in conversation"""
        return self.messages.count()
    
    def get_recent_messages(self, limit: int = 10) -> list:
        """Get recent messages from conversation"""
        return list(self.messages.order_by('-created_at')[:limit])
    
    def add_context(self, key: str, value) -> None:
        """Add context to conversation"""
        if not self.context:
            self.context = {}
        self.context[key] = value
        self.save(update_fields=['context'])
    
    def close(self) -> None:
        """Close conversation"""
        self.status = ConversationStatusChoices.CLOSED.value
        self.save(update_fields=['status'])


class Message(models.Model):
    """Message in conversation"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(
        max_length=20,
        choices=[('user', 'User'), ('assistant', 'Assistant'), ('system', 'System')],
        default='user'
    )
    content = models.TextField()
    
    # Metadata
    tokens_used = models.IntegerField(null=True, blank=True, help_text='Tokens used for this message')
    model = models.CharField(max_length=50, null=True, blank=True, help_text='Model used to generate response')
    
    # Feedback
    is_helpful = models.BooleanField(null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'message'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['conversation', 'created_at']),
            models.Index(fields=['role']),
        ]
    
    def __str__(self):
        return f"{self.role}: {self.content[:50]}..."
    
    def to_dict(self) -> dict:
        """Convert message to dictionary"""
        return {
            'id': str(self.id),
            'role': self.role,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
        }


class ConversationAnalytics(models.Model):
    """Analytics for conversations"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.OneToOneField(
        Conversation,
        on_delete=models.CASCADE,
        related_name='analytics'
    )
    
    # Message statistics
    total_messages = models.IntegerField(default=0)
    user_messages = models.IntegerField(default=0)
    assistant_messages = models.IntegerField(default=0)
    
    # Token usage
    total_tokens = models.IntegerField(default=0)
    total_cost = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    
    # Duration
    duration_seconds = models.IntegerField(default=0)
    average_response_time = models.FloatField(default=0)
    
    # Quality metrics
    average_helpfulness = models.FloatField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'conversation_analytics'
    
    def __str__(self):
        return f"Analytics: {self.conversation.id}"
    
    def update_statistics(self) -> None:
        """Update analytics from conversation messages"""
        messages = self.conversation.messages.all()
        self.total_messages = messages.count()
        self.user_messages = messages.filter(role='user').count()
        self.assistant_messages = messages.filter(role='assistant').count()
        self.total_tokens = sum(m.tokens_used or 0 for m in messages)
        self.save()
