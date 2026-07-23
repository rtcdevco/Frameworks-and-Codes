"""Gemini (Google) Agent implementation"""

from typing import Dict, Any, List, Optional, AsyncIterator
import google.generativeai as genai
from multi_ai.agents.base_agent import BaseAgent


class GeminiAgent(BaseAgent):
    """Google Gemini agent implementation"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        genai.configure(api_key=self.api_key)
        self.client = genai.GenerativeModel(self.model)

    async def send_message(
        self,
        prompt: str,
        tools: Optional[List[Dict]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Send message to Gemini and get response"""

        generation_config = {
            "temperature": kwargs.get("temperature", 1.0),
            "max_output_tokens": kwargs.get("max_tokens", 4096),
        }

        # Gemini tool calling is different - we'll implement basic support
        # For now, focusing on text generation
        response = await self.client.generate_content_async(
            prompt,
            generation_config=generation_config,
        )

        result = {
            "content": response.text,
            "tool_calls": [],
            "stop_reason": "stop",  # Gemini doesn't expose detailed stop reasons
            "usage": {
                "input_tokens": getattr(response.usage_metadata, 'prompt_token_count', 0),
                "output_tokens": getattr(response.usage_metadata, 'candidates_token_count', 0),
            }
        }

        return result

    async def stream_message(
        self,
        prompt: str,
        tools: Optional[List[Dict]] = None,
        **kwargs
    ) -> AsyncIterator[str]:
        """Stream response from Gemini"""

        generation_config = {
            "temperature": kwargs.get("temperature", 1.0),
            "max_output_tokens": kwargs.get("max_tokens", 4096),
        }

        response = await self.client.generate_content_async(
            prompt,
            generation_config=generation_config,
            stream=True,
        )

        async for chunk in response:
            if chunk.text:
                yield chunk.text

    def supports_tools(self) -> bool:
        """Gemini has limited tool support - returning False for now"""
        return False

    def format_tools(self, tools: List[Dict]) -> List[Dict]:
        """Format tools for Gemini's API"""
        # Gemini tool format is different, simplified for now
        return tools
