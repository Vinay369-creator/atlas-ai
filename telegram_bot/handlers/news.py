import logging
from telegram import Update
from telegram.ext import ContextTypes
from django.contrib.auth.models import User
from ai.services import AIService
from ai.response_formatter import ResponseFormatter
from chat.services import ConversationService
from accounts.services import UserInterestService, UserCompanyService

logger = logging.getLogger(__name__)


class NewsHandler:
    """Handler for news and briefing commands"""
    
    @staticmethod
    async def get_briefing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        /brief command - Get daily briefing
        """
        try:
            user_id = context.user_data.get('user_id')
            if not user_id:
                await update.message.reply_text('Please use /start first')
                return
            
            user = User.objects.get(id=user_id)
            
            # Show typing indicator
            await update.message.chat.send_action('typing')
            
            # Get user's followed companies and industries
            companies = list(UserCompanyService.get_user_companies(user).values_list('name', flat=True))
            industries = list(UserInterestService.get_user_interests(user).values_list('name', flat=True))
            
            # Get AI service
            ai_service = AIService()
            
            # Mock news items (in production, fetch from news API)
            news_items = [
                {
                    'title': 'Stock Market Reaches New High',
                    'description': 'Global markets continue upward trend...'
                },
                {
                    'title': 'Tech Giants Report Strong Earnings',
                    'description': 'Major technology companies exceed expectations...'
                }
            ]
            
            success, briefing_text, _ = ai_service.generate_briefing(
                user=user,
                news_items=news_items,
                industries=industries or None,
                companies=companies or None
            )
            
            if not success:
                await update.message.reply_text(
                    ResponseFormatter.format_error_message('Failed to generate briefing')
                )
                return
            
            # Format and send briefing
            briefing_msg = ResponseFormatter.format_briefing(
                title='Daily Financial Briefing',
                content=briefing_text,
                is_verbose=user.profile.verbose_mode
            )
            
            response_msgs = ResponseFormatter.split_long_message(briefing_msg)
            for msg in response_msgs:
                await update.message.reply_text(msg)
        
        except User.DoesNotExist:
            await update.message.reply_text('User not found')
        except Exception as e:
            logger.error(f'Error in get_briefing: {str(e)}')
            await update.message.reply_text(
                ResponseFormatter.format_error_message('Failed to get briefing')
            )
    
    @staticmethod
    async def get_news(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        /news command - Get latest financial news
        """
        try:
            user_id = context.user_data.get('user_id')
            if not user_id:
                await update.message.reply_text('Please use /start first')
                return
            
            user = User.objects.get(id=user_id)
            
            # Show typing indicator
            await update.message.chat.send_action('typing')
            
            # Mock news (in production, fetch from API)
            news_items = [
                {
                    'title': 'Breaking: Tech Company Announces New Product',
                    'source': 'Financial News Daily',
                    'sentiment': 'positive'
                },
                {
                    'title': 'Market Volatility Continues',
                    'source': 'Market Watch',
                    'sentiment': 'neutral'
                }
            ]
            
            news_text = "📰 Latest Financial News:\n\n"
            for item in news_items:
                formatted = ResponseFormatter.format_news_item(
                    title=item['title'],
                    description=item.get('description', 'Read more for details...'),
                    source=item.get('source'),
                    sentiment=item.get('sentiment')
                )
                news_text += formatted + "\n\n"
            
            response_msgs = ResponseFormatter.split_long_message(news_text)
            for msg in response_msgs:
                await update.message.reply_text(msg)
        
        except User.DoesNotExist:
            await update.message.reply_text('User not found')
        except Exception as e:
            logger.error(f'Error in get_news: {str(e)}')
            await update.message.reply_text(
                ResponseFormatter.format_error_message('Failed to get news')
            )
    
    @staticmethod
    async def get_insights(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        /insights command - Get market insights
        """
        try:
            user_id = context.user_data.get('user_id')
            if not user_id:
                await update.message.reply_text('Please use /start first')
                return
            
            user = User.objects.get(id=user_id)
            
            # Show typing indicator
            await update.message.chat.send_action('typing')
            
            ai_service = AIService()
            
            # Generate insight
            success, insight_text, _ = ai_service.generate_market_insight(
                topic='Technology Sector',
                data={
                    'Average PE Ratio': '25.5',
                    'YTD Performance': '+18.3%',
                    'Market Cap': '$2.5T'
                },
                context='Current market conditions'
            )
            
            if not success:
                await update.message.reply_text(
                    ResponseFormatter.format_error_message('Failed to generate insights')
                )
                return
            
            response_msgs = ResponseFormatter.split_long_message(insight_text)
            for msg in response_msgs:
                await update.message.reply_text(msg)
        
        except User.DoesNotExist:
            await update.message.reply_text('User not found')
        except Exception as e:
            logger.error(f'Error in get_insights: {str(e)}')
            await update.message.reply_text(
                ResponseFormatter.format_error_message('Failed to get insights')
            )
