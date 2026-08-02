import logging
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from telegram_bot.handlers.commands import CommandHandler as CmdHandler
from telegram_bot.handlers.messages import MessageHandler as MsgHandler, InlineHandler
from telegram_bot.handlers.preferences import PreferencesHandler
from telegram_bot.handlers.news import NewsHandler
from django.conf import settings

logger = logging.getLogger(__name__)


class TelegramBotSetup:
    """Setup and configuration for Telegram bot"""
    
    @staticmethod
    def create_app():
        """
        Create and configure Telegram bot application
        """
        app = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
        
        # Add command handlers
        app.add_handler(CommandHandler('start', CmdHandler.start))
        app.add_handler(CommandHandler('help', CmdHandler.help))
        app.add_handler(CommandHandler('settings', CmdHandler.settings))
        app.add_handler(CommandHandler('about', CmdHandler.about))
        
        # Add news handlers
        app.add_handler(CommandHandler('brief', NewsHandler.get_briefing))
        app.add_handler(CommandHandler('news', NewsHandler.get_news))
        app.add_handler(CommandHandler('insights', NewsHandler.get_insights))
        
        # Add preference handlers
        app.add_handler(CommandHandler('add_interest', PreferencesHandler.add_interests))
        app.add_handler(CommandHandler('add_company', PreferencesHandler.add_companies))
        app.add_handler(CommandHandler('interests', PreferencesHandler.view_interests))
        app.add_handler(CommandHandler('companies', PreferencesHandler.view_companies))
        
        # Add message handler
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, MsgHandler.handle_message))
        
        # Add callback handler
        app.add_handler(CallbackQueryHandler(InlineHandler.handle_callback))
        
        logger.info('Telegram bot application created')
        return app
    
    @staticmethod
    async def start_bot(app):
        """
        Start the bot
        """
        try:
            await app.initialize()
            await app.start()
            await app.updater.start_polling(allowed_updates=['message', 'callback_query'])
            logger.info('Telegram bot started successfully')
        except Exception as e:
            logger.error(f'Error starting bot: {str(e)}')
            raise
    
    @staticmethod
    async def stop_bot(app):
        """
        Stop the bot
        """
        try:
            await app.updater.stop()
            await app.stop()
            await app.shutdown()
            logger.info('Telegram bot stopped')
        except Exception as e:
            logger.error(f'Error stopping bot: {str(e)}')
