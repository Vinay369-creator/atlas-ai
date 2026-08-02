from django.contrib import admin
from accounts.models import UserProfile, UserInterest, UserCompany, UserIndustry, PriceAlert


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'timezone', 'language', 'is_onboarding_complete', 'is_active']
    list_filter = ['timezone', 'language', 'is_onboarding_complete', 'is_active']
    search_fields = ['user__username', 'telegram_username']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('User', {'fields': ('user', 'id')}),
        ('Telegram', {'fields': ('telegram_user_id', 'telegram_chat_id', 'telegram_username')}),
        ('Preferences', {'fields': ('timezone', 'language', 'currency', 'verbose_mode')}),
        ('Notifications', {'fields': ('notifications_enabled', 'morning_briefing_enabled', 'briefing_time')}),
        ('Account', {'fields': ('role', 'is_active', 'is_verified')}),
        ('Onboarding', {'fields': ('is_onboarding_complete', 'onboarding_completed_at')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(UserInterest)
class UserInterestAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'name']


@admin.register(UserCompany)
class UserCompanyAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'symbol', 'current_price', 'created_at']
    list_filter = ['created_at', 'industry']
    search_fields = ['user__username', 'name', 'symbol']


@admin.register(UserIndustry)
class UserIndustryAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'name']


@admin.register(PriceAlert)
class PriceAlertAdmin(admin.ModelAdmin):
    list_display = ['user', 'company', 'alert_type', 'target_price', 'is_active', 'triggered']
    list_filter = ['alert_type', 'is_active', 'triggered', 'created_at']
    search_fields = ['user__username', 'company__name']
