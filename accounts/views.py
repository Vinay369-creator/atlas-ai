from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from accounts.models import UserProfile, UserInterest, UserCompany, UserIndustry
from accounts.serializers import (
    UserProfileSerializer,
    UserProfileUpdateSerializer,
    UserInterestSerializer,
    UserCompanySerializer,
    UserIndustrySerializer,
    TelegramAuthSerializer
)
from accounts.services import (
    UserService,
    UserInterestService,
    UserCompanyService,
    UserIndustryService
)
import logging

logger = logging.getLogger(__name__)


class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for user profiles"""
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Get user's own profile"""
        return UserProfile.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Get current user's profile
        """
        profile = UserService.get_user_profile(request.user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put', 'patch'])
    def update_preferences(self, request):
        """
        Update user preferences
        """
        serializer = UserProfileUpdateSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            profile = UserService.update_user_preferences(
                request.user,
                serializer.validated_data
            )
            return Response(
                UserProfileSerializer(profile).data,
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def complete_onboarding(self, request):
        """
        Mark onboarding as complete
        """
        profile = request.user.profile
        profile.complete_onboarding()
        return Response(
            {'status': 'Onboarding completed'},
            status=status.HTTP_200_OK
        )


class UserInterestViewSet(viewsets.ModelViewSet):
    """ViewSet for user interests"""
    serializer_class = UserInterestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Get user's interests"""
        return UserInterest.objects.filter(profile__user=self.request.user)
    
    def perform_create(self, serializer):
        """Create interest for current user"""
        profile = self.request.user.profile
        serializer.save(profile=profile)
    
    @action(detail=False, methods=['post'])
    def add_interest(self, request):
        """
        Add new interest
        """
        name = request.data.get('name')
        category = request.data.get('category')
        
        if not name:
            return Response(
                {'error': 'Interest name is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        interest = UserInterestService.add_interest(
            request.user,
            name,
            category
        )
        serializer = self.get_serializer(interest)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserCompanyViewSet(viewsets.ModelViewSet):
    """ViewSet for user followed companies"""
    serializer_class = UserCompanySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Get user's followed companies"""
        return UserCompany.objects.filter(profile__user=self.request.user)
    
    def perform_create(self, serializer):
        """Create company for current user"""
        profile = self.request.user.profile
        serializer.save(profile=profile)
    
    @action(detail=False, methods=['post'])
    def add_company(self, request):
        """
        Add new company to follow
        """
        name = request.data.get('name')
        symbol = request.data.get('symbol')
        industry = request.data.get('industry')
        
        if not name:
            return Response(
                {'error': 'Company name is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        company = UserCompanyService.add_company(
            request.user,
            name,
            symbol,
            industry
        )
        serializer = self.get_serializer(company)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserIndustryViewSet(viewsets.ModelViewSet):
    """ViewSet for user industries"""
    serializer_class = UserIndustrySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Get user's industries"""
        return UserIndustry.objects.filter(profile__user=self.request.user)
    
    def perform_create(self, serializer):
        """Create industry for current user"""
        profile = self.request.user.profile
        serializer.save(profile=profile)
    
    @action(detail=False, methods=['post'])
    def add_industry(self, request):
        """
        Add new industry
        """
        name = request.data.get('name')
        
        if not name:
            return Response(
                {'error': 'Industry name is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        industry = UserIndustryService.add_industry(request.user, name)
        serializer = self.get_serializer(industry)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
