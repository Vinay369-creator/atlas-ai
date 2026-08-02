import logging
from typing import List, Optional, Dict, Tuple
from django.contrib.auth.models import User
from accounts.models import (
    UserProfile, UserInterest, UserCompany,
    UserIndustry, PriceAlert
)
from django.utils import timezone
from core.constants import LAST_ACTIVITY_UPDATE_THRESHOLD

logger = logging.getLogger(__name__)


class UserService:
    """Service for user management"""
    
    @staticmethod
    def get_or_create_telegram_user(
        telegram_user_id: int,
        telegram_chat_id: int,
        username: str,
        first_name: str = None,
        last_name: str = None
    ) -> Tuple[User, bool]:
        """
        Get or create user from Telegram data
        Returns: (user, created)
        """
        # Check if user exists by telegram_user_id
        existing_profile = UserProfile.objects.filter(
            telegram_user_id=telegram_user_id
        ).first()
        
        if existing_profile:
            return existing_profile.user, False
        
        # Create new user
        user = User.objects.create_user(
            username=username,
            first_name=first_name or '',
            last_name=last_name or ''
        )
        
        # Create profile
        UserProfile.objects.create(
            user=user,
            telegram_user_id=telegram_user_id,
            telegram_chat_id=telegram_chat_id,
            telegram_username=username
        )
        
        logger.info(f'Created new user {user.username} from Telegram {telegram_user_id}')
        return user, True
    
    @staticmethod
    def mark_user_active(user: User) -> None:
        """
        Mark user as active
        """
        profile = user.profile
        now = timezone.now()
        
        # Only update if threshold has passed
        if (profile.last_activity_at is None or
            (now - profile.last_activity_at) > LAST_ACTIVITY_UPDATE_THRESHOLD):
            profile.update_last_activity()
    
    @staticmethod
    def get_inactive_users(days: int = 30) -> List[User]:
        """
        Get users inactive for N days
        """
        from datetime import timedelta
        from django.utils import timezone
        
        threshold = timezone.now() - timedelta(days=days)
        return User.objects.filter(
            profile__last_activity_at__lt=threshold
        )
    
    @staticmethod
    def get_active_users() -> List[User]:
        """
        Get all active users
        """
        return User.objects.filter(
            profile__is_active=True
        )


class UserInterestService:
    """Service for user interests"""
    
    @staticmethod
    def add_interest(user: User, name: str, description: str = None) -> UserInterest:
        """
        Add interest for user
        """
        interest, created = UserInterest.objects.get_or_create(
            user=user,
            name=name,
            defaults={'description': description}
        )
        logger.info(f'Added interest {name} for user {user.username}')
        return interest
    
    @staticmethod
    def remove_interest(user: User, name: str) -> bool:
        """
        Remove interest for user
        """
        deleted_count, _ = UserInterest.objects.filter(
            user=user,
            name=name
        ).delete()
        return deleted_count > 0
    
    @staticmethod
    def get_user_interests(user: User) -> List[UserInterest]:
        """
        Get all interests for user
        """
        return UserInterest.objects.filter(user=user)


class UserCompanyService:
    """Service for user companies"""
    
    @staticmethod
    def add_company(
        user: User,
        name: str,
        symbol: str = None,
        industry: str = None
    ) -> UserCompany:
        """
        Add company for user
        """
        company, created = UserCompany.objects.get_or_create(
            user=user,
            name=name,
            defaults={'symbol': symbol, 'industry': industry}
        )
        logger.info(f'Added company {name} for user {user.username}')
        return company
    
    @staticmethod
    def remove_company(user: User, name: str) -> bool:
        """
        Remove company for user
        """
        deleted_count, _ = UserCompany.objects.filter(
            user=user,
            name=name
        ).delete()
        return deleted_count > 0
    
    @staticmethod
    def get_user_companies(user: User) -> List[UserCompany]:
        """
        Get all companies for user
        """
        return UserCompany.objects.filter(user=user)
    
    @staticmethod
    def update_company_price(
        company: UserCompany,
        price: float
    ) -> None:
        """
        Update company price
        """
        company.current_price = price
        company.price_updated_at = timezone.now()
        company.save()


class UserIndustryService:
    """Service for user industries"""
    
    @staticmethod
    def add_industry(user: User, name: str, description: str = None) -> UserIndustry:
        """
        Add industry for user
        """
        industry, created = UserIndustry.objects.get_or_create(
            user=user,
            name=name,
            defaults={'description': description}
        )
        logger.info(f'Added industry {name} for user {user.username}')
        return industry
    
    @staticmethod
    def remove_industry(user: User, name: str) -> bool:
        """
        Remove industry for user
        """
        deleted_count, _ = UserIndustry.objects.filter(
            user=user,
            name=name
        ).delete()
        return deleted_count > 0
    
    @staticmethod
    def get_user_industries(user: User) -> List[UserIndustry]:
        """
        Get all industries for user
        """
        return UserIndustry.objects.filter(user=user)


class PriceAlertService:
    """Service for price alerts"""
    
    @staticmethod
    def create_alert(
        user: User,
        company: UserCompany,
        alert_type: str,
        target_price: float
    ) -> PriceAlert:
        """
        Create price alert
        """
        alert = PriceAlert.objects.create(
            user=user,
            company=company,
            alert_type=alert_type,
            target_price=target_price
        )
        logger.info(f'Created alert for {company.name} at {target_price}')
        return alert
    
    @staticmethod
    def get_active_alerts(user: User) -> List[PriceAlert]:
        """
        Get active alerts for user
        """
        return PriceAlert.objects.filter(
            user=user,
            is_active=True,
            triggered=False
        )
    
    @staticmethod
    def check_alert_triggered(
        alert: PriceAlert,
        current_price: float
    ) -> bool:
        """
        Check if alert should be triggered
        """
        if alert.alert_type == 'above':
            return current_price >= alert.target_price
        else:  # below
            return current_price <= alert.target_price
    
    @staticmethod
    def trigger_alert(alert: PriceAlert) -> None:
        """
        Trigger alert
        """
        alert.triggered = True
        alert.triggered_at = timezone.now()
        alert.save()
        logger.info(f'Alert triggered for {alert.company.name}')
