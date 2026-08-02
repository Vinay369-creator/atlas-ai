from django.contrib import admin
from accounts.models import UserProfile, UserInterest, UserCompany, UserIndustry


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'telegram_username', 'status', 'is_onboarding_complete', 'created_at']
    list_filter = ['status', 'is_onboarding_complete', 'notifications_enabled', 'created_at']
    search_fields = ['user__username', 'telegram_username', 'telegram_user_id']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User', {
            'fields': ('user', 'telegram_user_id', 'telegram_chat_id', 'telegram_username')
        }),
        ('Profile Information', {
            'fields': ('bio', 'profession', 'avatar_url')
        }),
        ('Status', {
            'fields': ('status', 'is_onboarding_complete', 'onboarding_step')
        }),
        ('Notifications', {
            'fields': (
                'notifications_enabled', 'morning_briefing_enabled',
                'evening_summary_enabled', 'weekly_digest_enabled', 'breaking_news_enabled'
            )
        }),
        ('Briefing Schedule', {
            'fields': ('morning_briefing_hour', 'evening_briefing_hour', 'timezone')
        }),
        ('Preferences', {
            'fields': ('language', 'verbose_mode')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'last_active'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserInterest)
class UserInterestAdmin(admin.ModelAdmin):
    list_display = ['profile', 'name', 'category', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['profile__user__username', 'name']
    readonly_fields = ['created_at']


@admin.register(UserCompany)
class UserCompanyAdmin(admin.ModelAdmin):
    list_display = ['profile', 'name', 'symbol', 'industry', 'created_at']
    list_filter = ['industry', 'created_at']
    search_fields = ['profile__user__username', 'name', 'symbol']
    readonly_fields = ['created_at']


@admin.register(UserIndustry)
class UserIndustryAdmin(admin.ModelAdmin):
    list_display = ['profile', 'name', 'created_at']
    list_filter = ['created_at']
    search_fields = ['profile__user__username', 'name']
    readonly_fields = ['created_at']
