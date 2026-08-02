import logging
from typing import Dict, List, Optional, Tuple
from django.contrib.auth.models import User
from ai.llm_client import LLMClient
from ai.prompt_manager import PromptManager
from ai.response_formatter import ResponseFormatter
from chat.models import Conversation, Message
from chat.services import ConversationService
from core.exceptions import LLMAPIException, AIException

logger = logging.getLogger(__name__)


class AIService:
    """Service for AI operations"""
    
    def __init__(self):
        self.llm_client = LLMClient()
    
    def generate_response(
        self,
        user: User,
        conversation: Conversation,
        user_message: str,
        user_interests: List[str] = None,
        user_companies: List[str] = None
    ) -> Tuple[bool, Optional[str], Optional[Dict]]:
        """
        Generate AI response to user message
        """
        try:
            # Get conversation context
            context_messages = ConversationService.get_conversation_context(
                conversation,
                limit=10
            )
            
            # Format messages for LLM
            messages = PromptManager.format_conversation_context(
                context_messages + [{'role': 'user', 'content': user_message}],
                user_interests=user_interests,
                user_companies=user_companies
            )
            
            logger.info(f'Generating response for user {user.username}')
            
            # Get response from LLM
            success, response_text, metadata = self.llm_client.chat_completion(messages)
            
            if not success:
                logger.error(f'Failed to get LLM response: {response_text}')
                return False, 'Failed to generate response', None
            
            # Save response to conversation
            ConversationService.add_message(
                conversation=conversation,
                role='assistant',
                content=response_text,
                tokens_used=metadata.get('usage', {}).get('total_tokens'),
                model=metadata.get('model')
            )
            
            logger.info(f'Generated response of {len(response_text)} characters')
            return True, response_text, metadata
        
        except LLMAPIException as e:
            logger.error(f'LLM API error: {str(e)}')
            return False, 'Error generating response', None
        except Exception as e:
            logger.error(f'Unexpected error in generate_response: {str(e)}')
            return False, 'Unexpected error', None
    
    def generate_briefing(
        self,
        user: User,
        news_items: List[Dict],
        industries: List[str] = None,
        companies: List[str] = None,
        date: str = None
    ) -> Tuple[bool, Optional[str], Optional[Dict]]:
        """
        Generate daily briefing
        """
        try:
            from datetime import datetime
            date = date or datetime.now().strftime('%Y-%m-%d')
            
            # Create prompt
            prompt = PromptManager.create_briefing_prompt(
                date=date,
                news_items=news_items,
                industries=industries,
                companies=companies
            )
            
            # Get LLM response
            messages = [
                {'role': 'system', 'content': PromptManager.BRIEFING_SYSTEM_PROMPT},
                {'role': 'user', 'content': prompt}
            ]
            
            success, response_text, metadata = self.llm_client.chat_completion(messages)
            
            if not success:
                logger.error('Failed to generate briefing')
                return False, 'Failed to generate briefing', None
            
            logger.info('Generated briefing successfully')
            return True, response_text, metadata
        
        except Exception as e:
            logger.error(f'Error generating briefing: {str(e)}')
            return False, 'Error generating briefing', None
    
    def generate_market_insight(
        self,
        topic: str,
        data: Dict,
        context: str = None
    ) -> Tuple[bool, Optional[str], Optional[Dict]]:
        """
        Generate market insight
        """
        try:
            # Create prompt
            prompt = PromptManager.create_analysis_prompt(
                topic=topic,
                data=data,
                context=context
            )
            
            # Get LLM response
            messages = [
                {'role': 'system', 'content': PromptManager.INSIGHTS_SYSTEM_PROMPT},
                {'role': 'user', 'content': prompt}
            ]
            
            success, response_text, metadata = self.llm_client.chat_completion(messages)
            
            if not success:
                logger.error('Failed to generate insight')
                return False, 'Failed to generate insight', None
            
            logger.info(f'Generated insight for {topic}')
            return True, response_text, metadata
        
        except Exception as e:
            logger.error(f'Error generating insight: {str(e)}')
            return False, 'Error generating insight', None
    
    def summarize_text(
        self,
        text: str,
        length: str = 'medium'
    ) -> Tuple[bool, Optional[str], Optional[Dict]]:
        """
        Summarize text
        """
        try:
            prompt = PromptManager.create_summary_prompt(text, length)
            success, response_text, metadata = self.llm_client.generate_text(prompt)
            
            if not success:
                return False, 'Failed to summarize', None
            
            return True, response_text, metadata
        
        except Exception as e:
            logger.error(f'Error summarizing text: {str(e)}')
            return False, 'Error summarizing', None
    
    def answer_question(
        self,
        question: str,
        context: str = None
    ) -> Tuple[bool, Optional[str], Optional[Dict]]:
        """
        Answer user question
        """
        try:
            prompt = PromptManager.create_qa_prompt(question, context)
            success, response_text, metadata = self.llm_client.generate_text(prompt)
            
            if not success:
                return False, 'Failed to answer question', None
            
            return True, response_text, metadata
        
        except Exception as e:
            logger.error(f'Error answering question: {str(e)}')
            return False, 'Error answering question', None
