import logging
from typing import List, Dict
from core.constants import MESSAGE_TYPE_USER, MESSAGE_TYPE_ASSISTANT

logger = logging.getLogger(__name__)


class PromptManager:
    """Manager for generating and formatting prompts"""
    
    # System prompts
    BASE_SYSTEM_PROMPT = """You are Atlas AI, an intelligent financial assistant that helps users stay updated with 
financial news, market insights, and investment information. You provide thoughtful, accurate, and helpful responses.

Your capabilities:
- Financial news summarization
- Market analysis and insights
- Stock and company information
- Industry trends
- Investment advice (general guidance)
- Portfolio tracking assistance
- Economic indicators explanation

Always be:
- Accurate and cite sources when possible
- Professional yet friendly
- Concise but comprehensive
- Helpful and non-judgmental
"""
    
    BRIEFING_SYSTEM_PROMPT = """You are Atlas AI creating a financial briefing. Summarize the key market events, 
news, and insights in a concise and engaging format. Focus on the most impactful information for the user's interests."""
    
    INSIGHTS_SYSTEM_PROMPT = """You are Atlas AI providing market insights. Analyze market trends, company performance, 
and economic indicators. Provide balanced perspectives on potential opportunities and risks."""
    
    @staticmethod
    def get_system_prompt(briefing_type: str = 'general') -> str:
        """
        Get appropriate system prompt based on type
        """
        prompts = {
            'general': PromptManager.BASE_SYSTEM_PROMPT,
            'briefing': PromptManager.BRIEFING_SYSTEM_PROMPT,
            'insights': PromptManager.INSIGHTS_SYSTEM_PROMPT,
        }
        return prompts.get(briefing_type, PromptManager.BASE_SYSTEM_PROMPT)
    
    @staticmethod
    def format_conversation_context(
        conversation_messages: List[Dict[str, str]],
        user_interests: List[str] = None,
        user_companies: List[str] = None
    ) -> List[Dict[str, str]]:
        """
        Format conversation context for LLM with user context
        """
        messages = []
        
        # Add system message with context
        system_content = PromptManager.BASE_SYSTEM_PROMPT
        
        if user_interests or user_companies:
            system_content += "\n\nUser Context:\n"
            
            if user_interests:
                system_content += f"Interests: {', '.join(user_interests)}\n"
            
            if user_companies:
                system_content += f"Followed Companies: {', '.join(user_companies)}\n"
        
        messages.append({'role': 'system', 'content': system_content})
        
        # Add conversation history
        messages.extend(conversation_messages)
        
        return messages
    
    @staticmethod
    def create_briefing_prompt(
        date: str,
        news_items: List[Dict],
        industries: List[str] = None,
        companies: List[str] = None
    ) -> str:
        """
        Create a prompt for daily briefing
        """
        prompt = f"""Create a financial briefing for {date}.

Key News Items:
"""
        
        for idx, item in enumerate(news_items, 1):
            prompt += f"{idx}. Title: {item.get('title', 'N/A')}\n"
            if item.get('description'):
                prompt += f"   Description: {item['description'][:200]}...\n"
            prompt += "\n"
        
        if industries:
            prompt += f"\nFocus Areas: {', '.join(industries)}\n"
        
        if companies:
            prompt += f"Followed Companies: {', '.join(companies)}\n"
        
        prompt += """\nPlease provide:
1. Executive Summary (2-3 sentences)
2. Top 3 Key Developments
3. Market Impact Analysis
4. Relevant for User's Interests
5. Action Items (if any)
"""
        return prompt
    
    @staticmethod
    def create_analysis_prompt(
        topic: str,
        data: Dict,
        context: str = None
    ) -> str:
        """
        Create prompt for market analysis
        """
        prompt = f"Analyze the following {topic}:\n\n"
        
        for key, value in data.items():
            prompt += f"- {key}: {value}\n"
        
        if context:
            prompt += f"\nContext: {context}\n"
        
        prompt += """\nProvide:
1. Current Situation Analysis
2. Key Trends
3. Potential Opportunities
4. Risks to Consider
5. Recommendations
"""
        return prompt
    
    @staticmethod
    def create_summary_prompt(
        text: str,
        length: str = 'medium'
    ) -> str:
        """
        Create prompt for text summarization
        """
        length_instructions = {
            'short': '1-2 sentences',
            'medium': '3-5 sentences',
            'long': '1 paragraph'
        }
        
        instruction = length_instructions.get(length, length_instructions['medium'])
        
        prompt = f"""Summarize the following text in {instruction}. 
Focus on key points and insights.

Text:
{text}

Summary:"""
        return prompt
    
    @staticmethod
    def create_qa_prompt(
        question: str,
        context: str = None
    ) -> str:
        """
        Create prompt for question answering
        """
        prompt = f"Question: {question}\n"
        
        if context:
            prompt += f"\nContext: {context}\n"
        
        prompt += "\nProvide a detailed and accurate answer."
        return prompt
