from django.db import models
from django.contrib.auth.models import User
from core.constants import UserRoleChoices, BRIEFING_TIMEZONE, DEFAULT_CURRENCY
import uuid


class UserProfile(models.Model):
    """Extended user profile"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Telegram integration
    telegram_user_id = models.BigIntegerField(null=True, blank=True, unique=True)
    telegram_chat_id = models.BigIntegerField(null=True, blank=True)
    telegram_username = models.CharField(max_length=255, null=True, blank=True)
    
    # User preferences
    timezone = models.CharField(max_length=50, default=BRIEFING_TIMEZONE)
    language = models.CharField(max_length=10, default='en')
    currency = models.CharField(max_length=10, default=DEFAULT_CURRENCY)
    verbose_mode = models.BooleanField(default=False, help_text='More detailed responses')
    
    # Notifications
    notifications_enabled = models.BooleanField(default=True)
    morning_briefing_enabled = models.BooleanField(default=True)
    briefing_time = models.TimeField(default='09:00')
    price_alerts_enabled = models.BooleanField(default=True)
    
    # User role
    role = models.CharField(
        max_length=20,
        choices=[(choice.value, choice.name) for choice in UserRoleChoices],
        default=UserRoleChoices.USER.value
    )
    
    # Onboarding
    is_onboarding_complete = models.BooleanField(default=False)
    onboarding_completed_at = models.DateTimeField(null=True, blank=True)
    
    # Activity tracking
    last_activity_at = models.DateTimeField(null=True, blank=True)
    last_briefing_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    # Account status
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    
    # Preferences for content
    favorite_industries = models.JSONField(default=list, blank=True)
    risk_tolerance = models.CharField(
        max_length=20,
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        default='medium'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_profile'
        verbose_name = 'User Profile'
    
    def __str__(self):
        return f'Profile: {self.user.username}'
    
    def complete_onboarding(self):
        """Mark onboarding as complete"""
        from django.utils import timezone
        self.is_onboarding_complete = True
        self.onboarding_completed_at = timezone.now()
        self.save()
    
    def update_last_activity(self):
        """Update last activity timestamp"""
        from django.utils import timezone
        self.last_activity_at = timezone.now()
        self.save(update_fields=['last_activity_at'])


class UserInterest(models.Model):
    """User interests in financial topics"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interests')
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_interest'
        unique_together = ('user', 'name')
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.username}: {self.name}'


class UserCompany(models.Model):
    """Companies followed by user"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='companies')
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=10, null=True, blank=True)
    industry = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    
    # Price tracking
    current_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_updated_at = models.DateTimeField(null=True, blank=True)
    
    # Alerts
    price_alert_enabled = models.BooleanField(default=True)
    price_alert_threshold = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_company'
        unique_together = ('user', 'name')
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.username}: {self.name} ({self.symbol})'


class UserIndustry(models.Model):
    """Industries followed by user"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='industries')
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_industry'
        unique_together = ('user', 'name')
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.username}: {self.name}'


class PriceAlert(models.Model):
    """Price alerts for stocks"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='price_alerts')
    company = models.ForeignKey(UserCompany, on_delete=models.CASCADE, related_name='alerts')
    
    # Alert conditions
    alert_type = models.CharField(
        max_length=20,
        choices=[('above', 'Price Above'), ('below', 'Price Below')],
        default='above'
    )
    target_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Status
    is_active = models.BooleanField(default=True)
    triggered_at = models.DateTimeField(null=True, blank=True)
    triggered = models.BooleanField(default=False)
    
    # Notification
    notification_sent = models.BooleanField(default=False)
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'price_alert'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.username}: {self.company.name} {self.alert_type} {self.target_price}'
