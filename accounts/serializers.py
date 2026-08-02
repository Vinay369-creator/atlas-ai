from rest_framework import serializers
from accounts.models import UserProfile, UserInterest, UserCompany, UserIndustry, PriceAlert
from django.contrib.auth.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile"""
    class Meta:
        model = UserProfile
        fields = [
            'id', 'timezone', 'language', 'currency', 'verbose_mode',
            'notifications_enabled', 'morning_briefing_enabled', 'briefing_time',
            'price_alerts_enabled', 'role', 'is_onboarding_complete',
            'last_activity_at', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'last_activity_at']


class UserInterestSerializer(serializers.ModelSerializer):
    """Serializer for UserInterest"""
    class Meta:
        model = UserInterest
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserCompanySerializer(serializers.ModelSerializer):
    """Serializer for UserCompany"""
    class Meta:
        model = UserCompany
        fields = [
            'id', 'name', 'symbol', 'industry', 'description',
            'current_price', 'price_alert_enabled', 'created_at'
        ]
        read_only_fields = ['id', 'current_price', 'created_at']


class UserIndustrySerializer(serializers.ModelSerializer):
    """Serializer for UserIndustry"""
    class Meta:
        model = UserIndustry
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']


class PriceAlertSerializer(serializers.ModelSerializer):
    """Serializer for PriceAlert"""
    company_name = serializers.CharField(source='company.name', read_only=True)
    
    class Meta:
        model = PriceAlert
        fields = [
            'id', 'company', 'company_name', 'alert_type', 'target_price',
            'is_active', 'triggered', 'created_at'
        ]
        read_only_fields = ['id', 'triggered', 'created_at']


class UserDetailSerializer(serializers.ModelSerializer):
    """Detailed user serializer with profile"""
    profile = UserProfileSerializer(read_only=True)
    interests = UserInterestSerializer(many=True, read_only=True)
    companies = UserCompanySerializer(many=True, read_only=True)
    industries = UserIndustrySerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'profile', 'interests', 'companies', 'industries',
            'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']
