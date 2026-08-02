from django.contrib.auth.models import User
from accounts.models import UserProfile, UserInterest, UserCompany, UserIndustry
from django.utils import timezone
from typing import Dict, Optional, List
import logging

logger = logging.getLogger(__name__)


class UserService:
    """Service for user operations"""
    
    @staticmethod
    def get_or_create_telegram_user(
        telegram_user_id: int,
        telegram_chat_id: int,
        username: str,
        first_name: str = None,
        last_name: str = None
    ) -> tuple:
        """
        Get or create user from Telegram data
        Returns: (user, created)
        """
        try:
            profile = UserProfile.objects.select_related('user').get(
                telegram_user_id=telegram_user_id
            )
            return profile.user, False
        except UserProfile.DoesNotExist:
            pass
        
        # Create new user
        user_email = f"telegram_{telegram_user_id}@atlas.ai"
        user, created = User.objects.get_or_create(
            username=f"tg_{telegram_user_id}",
            defaults={
                'email': user_email,
                'first_name': first_name or '',
                'last_name': last_name or '',
            }
        )
        
        # Create profile
        profile, _ = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'telegram_user_id': telegram_user_id,
                'telegram_chat_id': telegram_chat_id,
                'telegram_username': username,
            }
        )
        
        logger.info(f'Created new Telegram user: {telegram_user_id}')
        return user, True
    
    @staticmethod
    def update_telegram_user(
        user: User,
        telegram_chat_id: int = None,
        telegram_username: str = None
    ) -> UserProfile:
        """
        Update Telegram user information
        """
        profile = user.profile
        
        if telegram_chat_id:
            profile.telegram_chat_id = telegram_chat_id
        if telegram_username:
            profile.telegram_username = telegram_username
        
        profile.mark_active()
        return profile
    
    @staticmethod
    def mark_user_active(user: User) -> None:
        """Mark user as active"""
        profile = user.profile
        profile.mark_active()
    
    @staticmethod
    def get_user_profile(user: User) -> UserProfile:
        """Get user profile"""
        return UserProfile.objects.prefetch_related(
            'interests',
            'followed_companies',
            'industries'
        ).get(user=user)
    
    @staticmethod
    def update_user_preferences(
        user: User,
        preferences: Dict
    ) -> UserProfile:
        """
        Update user preferences
        """
        profile = user.profile
        
        allowed_fields = [
            'bio', 'profession', 'notifications_enabled',
            'morning_briefing_enabled', 'evening_summary_enabled',
            'weekly_digest_enabled', 'breaking_news_enabled',
            'morning_briefing_hour', 'evening_briefing_hour',
            'timezone', 'language', 'verbose_mode'
        ]
        
        for field, value in preferences.items():
            if field in allowed_fields:
                setattr(profile, field, value)
        
        profile.save()
        logger.info(f'Updated preferences for user: {user.username}')
        return profile


class UserInterestService:
    """Service for user interests"""
    
    @staticmethod
    def add_interest(
        user: User,
        name: str,
        category: str = None
    ) -> UserInterest:
        """
        Add interest for user
        """
        profile = user.profile
        interest, created = UserInterest.objects.get_or_create(
            profile=profile,
            name=name,
            defaults={'category': category}
        )
        logger.info(f'Added interest {name} for user {user.username}')
        return interest
    
    @staticmethod
    def remove_interest(user: User, interest_id: str) -> bool:
        """
        Remove interest for user
        """
        profile = user.profile
        try:
            interest = UserInterest.objects.get(id=interest_id, profile=profile)
            interest.delete()
            logger.info(f'Removed interest {interest_id} for user {user.username}')
            return True
        except UserInterest.DoesNotExist:
            return False
    
    @staticmethod
    def get_user_interests(user: User) -> List[UserInterest]:
        """
        Get all interests for user
        """
        profile = user.profile
        return UserInterest.objects.filter(profile=profile).order_by('-created_at')
    
    @staticmethod
    def add_default_interests(user: User) -> None:
        """
        Add default interests for new user
        """
        from core.constants import DEFAULT_INTERESTS
        profile = user.profile
        
        for interest_name in DEFAULT_INTERESTS:
            UserInterest.objects.get_or_create(
                profile=profile,
                name=interest_name
            )


class UserCompanyService:
    """Service for user followed companies"""
    
    @staticmethod
    def add_company(
        user: User,
        name: str,
        symbol: str = None,
        industry: str = None
    ) -> UserCompany:
        """
        Add company for user to follow
        """
        profile = user.profile
        company, created = UserCompany.objects.get_or_create(
            profile=profile,
            symbol=symbol if symbol else name,
            defaults={
                'name': name,
                'industry': industry
            }
        )
        logger.info(f'Added company {name} for user {user.username}')
        return company
    
    @staticmethod
    def remove_company(user: User, company_id: str) -> bool:
        """
        Remove company for user
        """
        profile = user.profile
        try:
            company = UserCompany.objects.get(id=company_id, profile=profile)
            company.delete()
            logger.info(f'Removed company {company_id} for user {user.username}')
            return True
        except UserCompany.DoesNotExist:
            return False
    
    @staticmethod
    def get_user_companies(user: User) -> List[UserCompany]:
        """
        Get all companies followed by user
        """
        profile = user.profile
        return UserCompany.objects.filter(profile=profile).order_by('-created_at')


class UserIndustryService:
    """Service for user industries"""
    
    @staticmethod
    def add_industry(
        user: User,
        name: str
    ) -> UserIndustry:
        """
        Add industry for user
        """
        profile = user.profile
        industry, created = UserIndustry.objects.get_or_create(
            profile=profile,
            name=name
        )
        logger.info(f'Added industry {name} for user {user.username}')
        return industry
    
    @staticmethod
    def remove_industry(user: User, industry_id: str) -> bool:
        """
        Remove industry for user
        """
        profile = user.profile
        try:
            industry = UserIndustry.objects.get(id=industry_id, profile=profile)
            industry.delete()
            logger.info(f'Removed industry {industry_id} for user {user.username}')
            return True
        except UserIndustry.DoesNotExist:
            return False
    
    @staticmethod
    def get_user_industries(user: User) -> List[UserIndustry]:
        """
        Get all industries for user
        """
        profile = user.profile
        return UserIndustry.objects.filter(profile=profile).order_by('-created_at')
