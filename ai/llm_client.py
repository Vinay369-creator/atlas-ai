import openai
import logging
from typing import Dict, List, Optional, Tuple
from django.conf import settings
from core.exceptions import LLMAPIException
from core.constants import LLM_MAX_RETRIES, LLM_RETRY_DELAY
import time

logger = logging.getLogger(__name__)


class LLMClient:
    """Client for interacting with OpenAI API"""
    
    def __init__(
        self,
        api_key: str = None,
        model: str = None,
        temperature: float = None,
        max_tokens: int = None
    ):
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.model = model or settings.OPENAI_MODEL
        self.temperature = temperature if temperature is not None else settings.OPENAI_TEMPERATURE
        self.max_tokens = max_tokens or settings.OPENAI_MAX_TOKENS
        
        openai.api_key = self.api_key
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = None,
        max_tokens: int = None,
        retry_count: int = 0
    ) -> Tuple[bool, Optional[str], Optional[Dict]]:
        """
        Get chat completion from OpenAI
        Returns: (success, response_text, metadata)
        """
        try:
            temperature = temperature or self.temperature
            max_tokens = max_tokens or self.max_tokens
            
            logger.debug(f'Calling OpenAI API with {len(messages)} messages')
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                timeout=60
            )
            
            # Extract response
            content = response.choices[0].message.content
            metadata = {
                'model': response.model,
                'usage': {
                    'prompt_tokens': response.usage.prompt_tokens,
                    'completion_tokens': response.usage.completion_tokens,
                    'total_tokens': response.usage.total_tokens
                },
                'finish_reason': response.choices[0].finish_reason
            }
            
            logger.info(f'Successfully got completion. Total tokens: {metadata["usage"]["total_tokens"]}')
            return True, content, metadata
            
        except openai.error.RateLimitError as e:
            logger.warning(f'Rate limit error: {str(e)}')
            if retry_count < LLM_MAX_RETRIES:
                time.sleep(LLM_RETRY_DELAY * (retry_count + 1))
                return self.chat_completion(messages, temperature, max_tokens, retry_count + 1)
            raise LLMAPIException(f'Rate limit exceeded after {LLM_MAX_RETRIES} retries')
        
        except openai.error.APIError as e:
            logger.error(f'OpenAI API error: {str(e)}')
            if retry_count < LLM_MAX_RETRIES:
                time.sleep(LLM_RETRY_DELAY)
                return self.chat_completion(messages, temperature, max_tokens, retry_count + 1)
            raise LLMAPIException(f'OpenAI API error: {str(e)}')
        
        except Exception as e:
            logger.error(f'Unexpected error in chat_completion: {str(e)}')
            raise LLMAPIException(f'Error getting chat completion: {str(e)}')
    
    def generate_text(
        self,
        prompt: str,
        max_tokens: int = None
    ) -> Tuple[bool, Optional[str], Optional[Dict]]:
        """
        Generate text from prompt
        """
        messages = [
            {'role': 'user', 'content': prompt}
        ]
        return self.chat_completion(messages, max_tokens=max_tokens)
    
    def stream_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = None,
        max_tokens: int = None
    ):
        """
        Stream chat completion from OpenAI
        """
        try:
            temperature = temperature or self.temperature
            max_tokens = max_tokens or self.max_tokens
            
            logger.debug('Starting stream completion')
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
                timeout=60
            )
            
            for chunk in response:
                if 'choices' in chunk:
                    delta = chunk['choices'][0].get('delta', {})
                    if 'content' in delta:
                        yield delta['content']
        
        except Exception as e:
            logger.error(f'Error in stream completion: {str(e)}')
            raise LLMAPIException(f'Error in stream completion: {str(e)}')
