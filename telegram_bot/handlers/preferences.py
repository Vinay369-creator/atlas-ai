import logging
from telegram import Update
from telegram.ext import ContextTypes
from django.contrib.auth.models import User
from accounts.services import UserInterestService, UserCompanyService, UserIndustryService
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

logger = logging.getLogger(__name__)


class PreferencesHandler:
    """Handler for preference management commands"""
    
    @staticmethod
    async def add_interests(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Add user interests
        """
        try:
            user_id = context.user_data.get('user_id')
            if not user_id:
                await update.message.reply_text('Please use /start first')
                return
            
            user = User.objects.get(id=user_id)
            
            keyboard = [
                ['Technology', 'Finance'],
                ['Healthcare', 'Energy'],
                ['Cryptocurrency', 'Real Estate'],
                ['Skip']
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
            
            await update.message.reply_text(
                "Select interests to add:",
                reply_markup=reply_markup
            )
            
            context.user_data['adding_interests'] = True
        
        except Exception as e:
            logger.error(f'Error in add_interests: {str(e)}')
            await update.message.reply_text('Error adding interests')
    
    @staticmethod
    async def add_companies(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Add companies to follow
        """
        try:
            user_id = context.user_data.get('user_id')
            if not user_id:
                await update.message.reply_text('Please use /start first')
                return
            
            await update.message.reply_text(
                "Enter company names or stock symbols to follow:\n"
                "(comma-separated, e.g., Apple, MSFT, Tesla)"
            )
            
            context.user_data['adding_companies'] = True
        
        except Exception as e:
            logger.error(f'Error in add_companies: {str(e)}')
            await update.message.reply_text('Error adding companies')
    
    @staticmethod
    async def view_interests(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        View user interests
        """
        try:
            user_id = context.user_data.get('user_id')
            if not user_id:
                await update.message.reply_text('Please use /start first')
                return
            
            user = User.objects.get(id=user_id)
            interests = UserInterestService.get_user_interests(user)
            
            if not interests:
                await update.message.reply_text('No interests added yet. Use /add_interest')
                return
            
            interests_text = "📌 Your Interests:\n\n"
            for interest in interests:
                interests_text += f"• {interest.name}\n"
            
            await update.message.reply_text(interests_text)
        
        except Exception as e:
            logger.error(f'Error in view_interests: {str(e)}')
            await update.message.reply_text('Error retrieving interests')
    
    @staticmethod
    async def view_companies(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        View followed companies
        """
        try:
            user_id = context.user_data.get('user_id')
            if not user_id:
                await update.message.reply_text('Please use /start first')
                return
            
            user = User.objects.get(id=user_id)
            companies = UserCompanyService.get_user_companies(user)
            
            if not companies:
                await update.message.reply_text('No companies added yet. Use /add_company')
                return
            
            companies_text = "📈 Followed Companies:\n\n"
            for company in companies:
                companies_text += f"• {company.name} ({company.symbol or 'N/A'})\n"
            
            await update.message.reply_text(companies_text)
        
        except Exception as e:
            logger.error(f'Error in view_companies: {str(e)}')
            await update.message.reply_text('Error retrieving companies')
