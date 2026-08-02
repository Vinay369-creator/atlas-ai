import logging
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from django.contrib.auth.models import User
from chat.services import ConversationService
from ai.services import AIService
from ai.response_formatter import ResponseFormatter
from accounts.services import UserInterestService, UserCompanyService, UserIndustryService

logger = logging.getLogger(__name__)


class MessageHandler:
    """Handler for user messages"""
    
    @staticmethod
    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Handle regular user messages
        """
        try:
            user_id = context.user_data.get('user_id')
            if not user_id:
                await update.message.reply_text('Please use /start first')
                return
            
            user = User.objects.get(id=user_id)
            message_text = update.message.text
            
            # Check if user is in onboarding
            if context.user_data.get('in_onboarding'):
                await MessageHandler._handle_onboarding(update, context, user, message_text)
                return
            
            # Get or create conversation
            conversation_id = context.user_data.get('current_conversation_id')
            if not conversation_id:
                conversation = ConversationService.create_conversation(
                    user=user,
                    title='Chat'
                )
                context.user_data['current_conversation_id'] = str(conversation.id)
            else:
                conversation = ConversationService.get_conversation_by_id(user, conversation_id)
            
            # Add user message to conversation
            ConversationService.add_message(
                conversation=conversation,
                role='user',
                content=message_text
            )
            
            # Show typing indicator
            await update.message.chat.send_action('typing')
            
            # Get AI response
            ai_service = AIService()
            user_interests = list(UserInterestService.get_user_interests(user).values_list('name', flat=True))
            user_companies = list(UserCompanyService.get_user_companies(user).values_list('name', flat=True))
            
            success, response_text, metadata = ai_service.generate_response(
                user=user,
                conversation=conversation,
                user_message=message_text,
                user_interests=user_interests,
                user_companies=user_companies
            )
            
            if not success:
                await update.message.reply_text(
                    ResponseFormatter.format_error_message('Failed to generate response')
                )
                return
            
            # Mark user as active
            from accounts.services import UserService
            UserService.mark_user_active(user)
            
            # Format and send response
            response_msgs = ResponseFormatter.split_long_message(response_text)
            for msg in response_msgs:
                await update.message.reply_text(msg)
        
        except User.DoesNotExist:
            await update.message.reply_text('User not found. Please use /start')
        except Exception as e:
            logger.error(f'Error handling message: {str(e)}')
            await update.message.reply_text(
                ResponseFormatter.format_error_message('An error occurred')
            )
    
    @staticmethod
    async def _handle_onboarding(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        user: User,
        message_text: str
    ) -> None:
        """
        Handle onboarding responses
        """
        step = context.user_data.get('onboarding_step', 0)
        
        if step == 1:  # Industry selection
            industries = message_text.split(',')
            for industry in industries:
                industry = industry.strip()
                if industry != 'Other':
                    UserIndustryService.add_industry(user, industry)
            
            await update.message.reply_text(
                "Great! Now, which companies would you like to follow?\n"
                "(You can add them later too)"
            )
            context.user_data['onboarding_step'] = 2
        
        elif step == 2:  # Company selection
            if message_text.lower() != 'skip':
                companies = message_text.split(',')
                for company in companies:
                    company = company.strip()
                    UserCompanyService.add_company(user, company)
            
            await update.message.reply_text(
                "Perfect! Onboarding complete! 🎉\n\n"
                "Start by typing your first question or use /help for commands."
            )
            
            user.profile.complete_onboarding()
            context.user_data['in_onboarding'] = False
            context.user_data['onboarding_step'] = 0


class InlineHandler:
    """Handler for inline queries and callbacks"""
    
    @staticmethod
    async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Handle callback queries
        """
        try:
            query = update.callback_query
            await query.answer()
            
            # Handle different callback types
            if query.data.startswith('feedback_'):
                await InlineHandler._handle_feedback(update, context)
            elif query.data.startswith('settings_'):
                await InlineHandler._handle_settings_callback(update, context)
        
        except Exception as e:
            logger.error(f'Error in callback handler: {str(e)}')
    
    @staticmethod
    async def _handle_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Handle message feedback
        """
        query = update.callback_query
        feedback_type = query.data.split('_')[1]  # 'helpful' or 'unhelpful'
        
        await query.edit_message_text(
            text="Thank you for your feedback! 🙏"
        )
    
    @staticmethod
    async def _handle_settings_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Handle settings callback
        """
        query = update.callback_query
        setting = query.data.split('_')[1]
        
        user_id = context.user_data.get('user_id')
        user = User.objects.get(id=user_id)
        
        # Toggle setting
        profile = user.profile
        if setting == 'briefing':
            profile.morning_briefing_enabled = not profile.morning_briefing_enabled
        elif setting == 'notifications':
            profile.notifications_enabled = not profile.notifications_enabled
        
        profile.save()
        
        await query.edit_message_text(
            text=f"Setting updated! ✅"
        )
