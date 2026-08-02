from django.core.management.base import BaseCommand
from telegram_bot.bot import TelegramBotSetup
import asyncio
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Start the Telegram bot'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Telegram bot...'))
        
        try:
            # Create bot application
            app = TelegramBotSetup.create_app()
            
            # Run bot
            asyncio.run(TelegramBotSetup.start_bot(app))
        
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('Bot interrupted by user'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
            logger.error(f'Bot error: {str(e)}')
