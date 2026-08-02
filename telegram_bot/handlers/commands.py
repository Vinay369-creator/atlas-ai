import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from django.contrib.auth.models import User
from accounts.services import UserService
from ai.response_formatter import ResponseFormatter

logger = logging.getLogger(__name__)


class CommandHandler:
    """Handler for Telegram commands"""
    
    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        /start command - Initialize user
        """
        try:
            telegram_user = update.effective_user
            telegram_chat = update.effective_chat
            
            logger.info(f'Start command from user {telegram_user.id}')
            
            # Get or create user
            user, created = UserService.get_or_create_telegram_user(
                telegram_user_id=telegram_user.id,
                telegram_chat_id=telegram_chat.id,
                username=telegram_user.username or f"user_{telegram_user.id}",
                first_name=telegram_user.first_name,
                last_name=telegram_user.last_name
            )
            
            # Store user in context
            context.user_data['user_id'] = user.id
            context.user_data['telegram_user_id'] = telegram_user.id
            
            # Send welcome message
            welcome_msg = ResponseFormatter.format_welcome_message(
                telegram_user.first_name or 'User'
            )
            await update.message.reply_text(welcome_msg)
            
            # Check if onboarding is complete
            if not user.profile.is_onboarding_complete:
                context.user_data['in_onboarding'] = True
                await CommandHandler._start_onboarding(update, context, user)
        
        except Exception as e:
            logger.error(f'Error in start command: {str(e)}')
            await update.message.reply_text(
                ResponseFormatter.format_error_message('Failed to initialize')
            )
    
    @staticmethod
    async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        /help command - Show available commands
        """
        try:
            help_msg = ResponseFormatter.format_help_message()
            await update.message.reply_text(help_msg)
        except Exception as e:
            logger.error(f'Error in help command: {str(e)}')
            await update.message.reply_text('Error retrieving help')
    
    @staticmethod
    async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        /settings command - Show user settings
        """
        try:
            user_id = context.user_data.get('user_id')
            if not user_id:
                await update.message.reply_text('Please use /start first')
                return
            
            user = User.objects.get(id=user_id)
            profile = user.profile
            
            settings_summary = ResponseFormatter.format_settings_summary({
                'morning_briefing_enabled': profile.morning_briefing_enabled,
                'notifications_enabled': profile.notifications_enabled,
                'timezone': profile.timezone,
                'language': profile.language,
            })
            
            await update.message.reply_text(settings_summary)
        
        except Exception as e:
            logger.error(f'Error in settings command: {str(e)}')
            await update.message.reply_text('Error retrieving settings')
    
    @staticmethod
    async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        /about command - Show about information
        """
        about_msg = """📱 Atlas AI - Financial Intelligence Assistant

Version: 1.0.0
Powered by OpenAI GPT & Financial APIs

Atlas AI helps you stay updated with:
• Financial news and market trends
• Investment insights and analysis
• Stock information and tracking
• Industry updates
• Personalized briefings

🌐 Website: https://atlasai.com
📧 Support: support@atlasai.com
"""
        await update.message.reply_text(about_msg)
    
    @staticmethod
    async def _start_onboarding(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        user: User
    ) -> None:
        """
        Start user onboarding process
        """
        keyboard = [
            ['Technology', 'Finance'],
            ['Healthcare', 'Energy'],
            ['Other']
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        
        await update.message.reply_text(
            "👋 Let's set up your preferences!\n\n"
            "First, what industries interest you?",
            reply_markup=reply_markup
        )
        
        context.user_data['onboarding_step'] = 1
