import logging
from typing import Dict, List, Optional
from django.conf import settings

logger = logging.getLogger(__name__)


class ResponseFormatter:
    """Formatter for AI responses"""
    
    # Telegram message length limits
    MAX_MESSAGE_LENGTH = 4096
    MAX_MESSAGE_LENGTH_SHORT = 1024
    
    @staticmethod
    def truncate_for_telegram(text: str, limit: int = MAX_MESSAGE_LENGTH) -> str:
        """
        Truncate text to fit Telegram message limit
        """
        if len(text) <= limit:
            return text
        return text[:limit-3] + '...'
    
    @staticmethod
    def split_long_message(text: str, chunk_size: int = 4000) -> List[str]:
        """
        Split long text into multiple messages
        """
        if len(text) <= chunk_size:
            return [text]
        
        messages = []
        current_chunk = ""
        
        # Split by paragraphs
        paragraphs = text.split('\n\n')
        
        for paragraph in paragraphs:
            if len(current_chunk) + len(paragraph) + 2 <= chunk_size:
                current_chunk += paragraph + "\n\n"
            else:
                if current_chunk:
                    messages.append(current_chunk.strip())
                current_chunk = paragraph + "\n\n"
        
        if current_chunk:
            messages.append(current_chunk.strip())
        
        return messages
    
    @staticmethod
    def format_briefing(
        title: str,
        content: str,
        is_verbose: bool = False
    ) -> str:
        """
        Format briefing response
        """
        formatted = f"📰 {title}\n\n{content}"
        
        if not is_verbose:
            formatted = ResponseFormatter.truncate_for_telegram(
                formatted,
                ResponseFormatter.MAX_MESSAGE_LENGTH_SHORT
            )
        else:
            formatted = ResponseFormatter.truncate_for_telegram(formatted)
        
        return formatted
    
    @staticmethod
    def format_news_item(
        title: str,
        description: str,
        source: str = None,
        sentiment: str = None
    ) -> str:
        """
        Format news item for display
        """
        emoji = '📈' if sentiment == 'positive' else '📉' if sentiment == 'negative' else '📰'
        
        formatted = f"{emoji} {title}\n\n{description}"
        
        if source:
            formatted += f"\n\n📄 Source: {source}"
        
        return formatted
    
    @staticmethod
    def format_market_insight(
        insight_type: str,
        data: Dict,
        analysis: str
    ) -> str:
        """
        Format market insight
        """
        formatted = f"💡 {insight_type}\n\n"
        
        # Add data
        for key, value in data.items():
            formatted += f"• {key}: {value}\n"
        
        formatted += f"\n{analysis}"
        
        return formatted
    
    @staticmethod
    def format_error_message(error: str) -> str:
        """
        Format error message
        """
        return f"❌ Error: {error}\n\nPlease try again later or contact support."
    
    @staticmethod
    def format_welcome_message(username: str) -> str:
        """
        Format welcome message
        """
        return f"""👋 Welcome to Atlas AI, {username}!

I'm your intelligent financial assistant. I can help you with:
• 📊 Financial news and updates
• 💼 Market insights and analysis
• 📈 Stock information
• 🏭 Industry trends
• 💡 Investment guidance

Use /help to see all available commands."""
    
    @staticmethod
    def format_help_message() -> str:
        """
        Format help message with available commands
        """
        return """📚 Available Commands:

/start - Start using Atlas AI
/help - Show this help message
/brief - Get today's briefing
/news - Get latest financial news
/insights - Get market insights
/add_interest - Add interest topics
/settings - Manage your preferences
/portfolio - View your portfolio
/alerts - Manage price alerts
/about - About Atlas AI

Type /start to begin!"""
    
    @staticmethod
    def format_settings_summary(profile: Dict) -> str:
        """
        Format settings summary
        """
        briefing_status = "✅" if profile.get('morning_briefing_enabled') else "❌"
        notifications_status = "✅" if profile.get('notifications_enabled') else "❌"
        
        return f"""⚙️ Your Settings:

📰 Briefings: {briefing_status}
🔔 Notifications: {notifications_status}
🌍 Timezone: {profile.get('timezone', 'UTC')}
🗣️ Language: {profile.get('language', 'English')}

Use /settings to modify your preferences."""
