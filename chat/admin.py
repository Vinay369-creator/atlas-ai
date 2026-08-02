from django.contrib import admin
from chat.models import Conversation, Message, ConversationAnalytics


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'is_briefing', 'created_at', 'updated_at']
    list_filter = ['status', 'is_briefing', 'created_at']
    search_fields = ['user__username', 'title']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Information', {
            'fields': ('id', 'user', 'title')
        }),
        ('Status', {
            'fields': ('status', 'is_briefing')
        }),
        ('Context', {
            'fields': ('context',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class MessageInline(admin.TabularInline):
    """Inline admin for messages"""
    model = Message
    extra = 0
    readonly_fields = ['id', 'created_at']
    fields = ['role', 'content', 'created_at']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'conversation', 'role', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['conversation__id', 'content']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Message', {
            'fields': ('id', 'conversation', 'role', 'content')
        }),
        ('Metadata', {
            'fields': ('tokens_used', 'model')
        }),
        ('Feedback', {
            'fields': ('is_helpful', 'feedback')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ConversationAnalytics)
class ConversationAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'total_messages', 'total_tokens', 'total_cost']
    list_filter = ['created_at']
    search_fields = ['conversation__id']
    readonly_fields = [
        'id', 'conversation', 'created_at', 'updated_at',
        'total_messages', 'user_messages', 'assistant_messages'
    ]
