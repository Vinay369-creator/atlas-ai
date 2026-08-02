from rest_framework import serializers
from chat.models import Conversation, Message, ConversationAnalytics


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model"""
    class Meta:
        model = Message
        fields = ['id', 'role', 'content', 'tokens_used', 'model', 'is_helpful', 'feedback', 'created_at']
        read_only_fields = ['id', 'created_at']


class ConversationAnalyticsSerializer(serializers.ModelSerializer):
    """Serializer for ConversationAnalytics"""
    class Meta:
        model = ConversationAnalytics
        fields = [
            'id', 'total_messages', 'user_messages', 'assistant_messages',
            'total_tokens', 'total_cost', 'duration_seconds', 'average_response_time',
            'average_helpfulness', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for Conversation model"""
    messages = MessageSerializer(many=True, read_only=True)
    analytics = ConversationAnalyticsSerializer(read_only=True)
    message_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = [
            'id', 'title', 'status', 'is_briefing', 'context',
            'messages', 'analytics', 'message_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'messages', 'analytics', 'created_at', 'updated_at']
    
    def get_message_count(self, obj):
        return obj.get_message_count()


class ConversationListSerializer(serializers.ModelSerializer):
    """Serializer for conversation list"""
    message_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = ['id', 'title', 'status', 'message_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_message_count(self, obj):
        return obj.get_message_count()


class SendMessageSerializer(serializers.Serializer):
    """Serializer for sending a message"""
    conversation_id = serializers.UUIDField(required=False, allow_null=True)
    content = serializers.CharField(max_length=4096)
    context = serializers.JSONField(required=False, default=dict)
    
    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError('Message content cannot be empty')
        return value.strip()


class ConversationCreateSerializer(serializers.Serializer):
    """Serializer for creating a conversation"""
    title = serializers.CharField(max_length=255, required=False, allow_blank=True)
    is_briefing = serializers.BooleanField(default=False)
    initial_message = serializers.CharField(max_length=4096, required=False)
