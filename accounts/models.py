from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from core.constants import UserStatusChoices, BriefingFrequencyChoices
import uuid


class UserProfile(models.Model):
    """Extended user profile with preferences and settings"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    telegram_user_id = models.BigIntegerField(unique=True, null=True, blank=True)
    telegram_chat_id = models.BigIntegerField(unique=True, null=True, blank=True)
    telegram_username = models.CharField(max_length=255, null=True, blank=True)
    
    # Profile Information
    bio = models.TextField(null=True, blank=True)
    profession = models.CharField(max_length=255, null=True, blank=True)
    avatar_url = models.URLField(null=True, blank=True)
    
    # Status and Preferences
    status = models.CharField(
        max_length=20,
        choices=[(choice.value, choice.name) for choice in UserStatusChoices],
        default=UserStatusChoices.ONBOARDING.value
    )
    is_onboarding_complete = models.BooleanField(default=False)
    onboarding_step = models.IntegerField(default=0, help_text='Current step in onboarding flow')
    
    # Notification Preferences
    notifications_enabled = models.BooleanField(default=True)
    morning_briefing_enabled = models.BooleanField(default=True)
    evening_summary_enabled = models.BooleanField(default=True)
    weekly_digest_enabled = models.BooleanField(default=True)
    breaking_news_enabled = models.BooleanField(default=False)
    
    # Briefing Times
    morning_briefing_hour = models.IntegerField(
        default=8,
        validators=[MinValueValidator(0), MaxValueValidator(23)]
    )
    evening_briefing_hour = models.IntegerField(
        default=17,
        validators=[MinValueValidator(0), MaxValueValidator(23)]
    )
    timezone = models.CharField(max_length=50, default='UTC')
    
    # Communication Preferences
    language = models.CharField(max_length=10, default='en')
    verbose_mode = models.BooleanField(
        default=False,
        help_text='Send detailed responses instead of concise ones'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_active = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'user_profile'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['telegram_user_id']),
            models.Index(fields=['telegram_chat_id']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Profile: {self.user.username}"
    
    def mark_active(self):
        """Mark user as active"""
        from django.utils import timezone
        self.last_active = timezone.now()
        self.save(update_fields=['last_active'])
    
    def complete_onboarding(self):
        """Mark onboarding as complete"""
        self.is_onboarding_complete = True
        self.status = UserStatusChoices.ACTIVE.value
        self.save()


class UserInterest(models.Model):
    """User interests and preferences"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='interests')
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_interest'
        unique_together = ['profile', 'name']
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['profile', 'category']),
        ]
    
    def __str__(self):
        return f"{self.profile.user.username} - {self.name}"


class UserCompany(models.Model):
    """Companies followed by user"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='followed_companies')
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=20, null=True, blank=True)
    industry = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_company'
        unique_together = ['profile', 'symbol'] if 'symbol' else ['profile', 'name']
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['profile', 'symbol']),
            models.Index(fields=['symbol']),
        ]
    
    def __str__(self):
        return f"{self.profile.user.username} - {self.name}"


class UserIndustry(models.Model):
    """Industries of interest to user"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='industries')
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_industry'
        unique_together = ['profile', 'name']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.profile.user.username} - {self.name}"
