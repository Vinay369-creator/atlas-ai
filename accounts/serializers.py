from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.models import UserProfile, UserInterest, UserCompany, UserIndustry


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class UserInterestSerializer(serializers.ModelSerializer):
    """Serializer for UserInterest model"""
    class Meta:
        model = UserInterest
        fields = ['id', 'name', 'category', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserCompanySerializer(serializers.ModelSerializer):
    """Serializer for UserCompany model"""
    class Meta:
        model = UserCompany
        fields = ['id', 'name', 'symbol', 'industry', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserIndustrySerializer(serializers.ModelSerializer):
    """Serializer for UserIndustry model"""
    class Meta:
        model = UserIndustry
        fields = ['id', 'name', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model"""
    user = UserSerializer(read_only=True)
    interests = UserInterestSerializer(many=True, read_only=True)
    followed_companies = UserCompanySerializer(many=True, read_only=True)
    industries = UserIndustrySerializer(many=True, read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'telegram_user_id', 'telegram_chat_id', 'telegram_username',
            'bio', 'profession', 'avatar_url', 'status', 'is_onboarding_complete',
            'notifications_enabled', 'morning_briefing_enabled', 'evening_summary_enabled',
            'weekly_digest_enabled', 'breaking_news_enabled', 'morning_briefing_hour',
            'evening_briefing_hour', 'timezone', 'language', 'verbose_mode',
            'interests', 'followed_companies', 'industries', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating UserProfile"""
    class Meta:
        model = UserProfile
        fields = [
            'bio', 'profession', 'notifications_enabled', 'morning_briefing_enabled',
            'evening_summary_enabled', 'weekly_digest_enabled', 'breaking_news_enabled',
            'morning_briefing_hour', 'evening_briefing_hour', 'timezone', 'language', 'verbose_mode'
        ]


class TelegramAuthSerializer(serializers.Serializer):
    """Serializer for Telegram authentication"""
    telegram_user_id = serializers.IntegerField()
    telegram_chat_id = serializers.IntegerField()
    telegram_username = serializers.CharField(max_length=255, required=False)
    first_name = serializers.CharField(max_length=255, required=False)
    last_name = serializers.CharField(max_length=255, required=False)
    
    def validate_telegram_user_id(self, value):
        if value <= 0:
            raise serializers.ValidationError('Invalid Telegram user ID')
        return value
    
    def validate_telegram_chat_id(self, value):
        if value == 0:
            raise serializers.ValidationError('Invalid Telegram chat ID')
        return value
