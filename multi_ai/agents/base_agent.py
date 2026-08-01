"""Base Agent interface for all AI providers"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, AsyncIterator


class BaseAgent(ABC):
    """Abstract base class for all AI agents"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.provider_name = self.__class__.__name__.replace("Agent", "").lower()
        self.api_key = config.get("api_key")
        self.model = config.get("model")

    @abstractmethod
    async def send_message(
        self,
        prompt: str,
        tools: Optional[List[Dict]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Send a message and get a response

        Args:
            prompt: The message/prompt to send
            tools: Optional list of tools the AI can use
            **kwargs: Additional provider-specific parameters

        Returns:
            Dict containing the response and metadata
        """
        pass

    @abstractmethod
    async def stream_message(
        self,
        prompt: str,
        tools: Optional[List[Dict]] = None,
        **kwargs
    ) -> AsyncIterator[str]:
        """
        Stream response for real-time output

        Args:
            prompt: The message/prompt to send
            tools: Optional list of tools the AI can use
            **kwargs: Additional provider-specific parameters

        Yields:
            str: Chunks of the response as they arrive
        """
        pass

    @abstractmethod
    def supports_tools(self) -> bool:
        """Whether this agent supports tool/function calling"""
        pass

    def format_tools(self, tools: List[Dict]) -> List[Dict]:
        """
        Format tools for this provider's API format
        Override in subclasses if needed
        """
        return tools

    async def __aenter__(self):
        """Async context manager entry"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        pass
