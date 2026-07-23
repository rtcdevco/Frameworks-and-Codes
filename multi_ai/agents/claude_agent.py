"""Claude (Anthropic) Agent implementation"""

from typing import Dict, Any, List, Optional, AsyncIterator
from anthropic import AsyncAnthropic
from multi_ai.agents.base_agent import BaseAgent


class ClaudeAgent(BaseAgent):
    """Anthropic Claude agent implementation"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.client = AsyncAnthropic(api_key=self.api_key)

    async def send_message(
        self,
        prompt: str,
        tools: Optional[List[Dict]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Send message to Claude and get response"""

        max_tokens = kwargs.get("max_tokens", 4096)
        temperature = kwargs.get("temperature", 1.0)

        messages = [{"role": "user", "content": prompt}]

        request_params = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": messages,
            "temperature": temperature,
        }

        if tools:
            request_params["tools"] = self.format_tools(tools)

        response = await self.client.messages.create(**request_params)

        # Extract response
        result = {
            "content": "",
            "tool_calls": [],
            "stop_reason": response.stop_reason,
            "usage": {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
            }
        }

        # Process content blocks
        for block in response.content:
            if block.type == "text":
                result["content"] += block.text
            elif block.type == "tool_use":
                result["tool_calls"].append({
                    "id": block.id,
                    "name": block.name,
                    "input": block.input,
                })

        return result

    async def stream_message(
        self,
        prompt: str,
        tools: Optional[List[Dict]] = None,
        **kwargs
    ) -> AsyncIterator[str]:
        """Stream response from Claude"""

        max_tokens = kwargs.get("max_tokens", 4096)
        temperature = kwargs.get("temperature", 1.0)

        messages = [{"role": "user", "content": prompt}]

        request_params = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": messages,
            "temperature": temperature,
        }

        if tools:
            request_params["tools"] = self.format_tools(tools)

        async with self.client.messages.stream(**request_params) as stream:
            async for text in stream.text_stream:
                yield text

    def supports_tools(self) -> bool:
        """Claude supports tool calling"""
        return True

    def format_tools(self, tools: List[Dict]) -> List[Dict]:
        """Format tools for Claude's API"""
        # Claude expects: name, description, input_schema
        formatted = []
        for tool in tools:
            formatted.append({
                "name": tool.get("name"),
                "description": tool.get("description"),
                "input_schema": tool.get("input_schema", tool.get("parameters", {})),
            })
        return formatted
