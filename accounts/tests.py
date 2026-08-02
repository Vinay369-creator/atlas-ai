from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import UserProfile, UserInterest, UserCompany, UserIndustry
from accounts.services import UserService, UserInterestService


class UserProfileTestCase(TestCase):
    """Test cases for UserProfile model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_user_profile_created_on_user_creation(self):
        """Test that UserProfile is created when User is created"""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsNotNone(self.user.profile)
    
    def test_user_profile_default_values(self):
        """Test UserProfile has correct default values"""
        profile = self.user.profile
        self.assertEqual(profile.morning_briefing_hour, 8)
        self.assertEqual(profile.evening_briefing_hour, 17)
        self.assertTrue(profile.notifications_enabled)
        self.assertFalse(profile.is_onboarding_complete)
    
    def test_mark_user_active(self):
        """Test marking user as active"""
        profile = self.user.profile
        self.assertIsNone(profile.last_active)
        
        profile.mark_active()
        self.assertIsNotNone(profile.last_active)
    
    def test_complete_onboarding(self):
        """Test completing onboarding"""
        profile = self.user.profile
        self.assertFalse(profile.is_onboarding_complete)
        
        profile.complete_onboarding()
        self.assertTrue(profile.is_onboarding_complete)


class UserServiceTestCase(TestCase):
    """Test cases for UserService"""
    
    def test_get_or_create_telegram_user_new(self):
        """Test creating new user from Telegram"""
        user, created = UserService.get_or_create_telegram_user(
            telegram_user_id=123456,
            telegram_chat_id=123456,
            username='testuser',
            first_name='Test',
            last_name='User'
        )
        
        self.assertTrue(created)
        self.assertIsNotNone(user.profile.telegram_user_id)
        self.assertEqual(user.profile.telegram_user_id, 123456)
    
    def test_get_or_create_telegram_user_existing(self):
        """Test getting existing Telegram user"""
        user1, created1 = UserService.get_or_create_telegram_user(
            telegram_user_id=123456,
            telegram_chat_id=123456,
            username='testuser'
        )
        
        user2, created2 = UserService.get_or_create_telegram_user(
            telegram_user_id=123456,
            telegram_chat_id=123456,
            username='testuser'
        )
        
        self.assertTrue(created1)
        self.assertFalse(created2)
        self.assertEqual(user1.id, user2.id)


class UserInterestServiceTestCase(TestCase):
    """Test cases for UserInterestService"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com'
        )
    
    def test_add_interest(self):
        """Test adding interest"""
        interest = UserInterestService.add_interest(
            self.user,
            'Technology',
            'Finance'
        )
        
        self.assertIsNotNone(interest)
        self.assertEqual(interest.name, 'Technology')
        self.assertEqual(interest.category, 'Finance')
    
    def test_get_user_interests(self):
        """Test getting user interests"""
        UserInterestService.add_interest(self.user, 'Technology')
        UserInterestService.add_interest(self.user, 'Cryptocurrency')
        
        interests = UserInterestService.get_user_interests(self.user)
        self.assertEqual(interests.count(), 2)
