"""GPT (OpenAI) Agent implementation"""

from typing import Dict, Any, List, Optional, AsyncIterator
from openai import AsyncOpenAI
from multi_ai.agents.base_agent import BaseAgent


class GPTAgent(BaseAgent):
    """OpenAI GPT agent implementation"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.client = AsyncOpenAI(api_key=self.api_key)

    async def send_message(
        self,
        prompt: str,
        tools: Optional[List[Dict]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Send message to GPT and get response"""

        temperature = kwargs.get("temperature", 1.0)
        max_tokens = kwargs.get("max_tokens", 4096)

        messages = [{"role": "user", "content": prompt}]

        request_params = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        if tools:
            request_params["tools"] = self.format_tools(tools)
            request_params["tool_choice"] = "auto"

        response = await self.client.chat.completions.create(**request_params)

        message = response.choices[0].message

        result = {
            "content": message.content or "",
            "tool_calls": [],
            "stop_reason": response.choices[0].finish_reason,
            "usage": {
                "input_tokens": response.usage.prompt_tokens,
                "output_tokens": response.usage.completion_tokens,
            }
        }

        # Extract tool calls if present
        if message.tool_calls:
            for tool_call in message.tool_calls:
                result["tool_calls"].append({
                    "id": tool_call.id,
                    "name": tool_call.function.name,
                    "input": eval(tool_call.function.arguments),  # Parse JSON string
                })

        return result

    async def stream_message(
        self,
        prompt: str,
        tools: Optional[List[Dict]] = None,
        **kwargs
    ) -> AsyncIterator[str]:
        """Stream response from GPT"""

        temperature = kwargs.get("temperature", 1.0)
        max_tokens = kwargs.get("max_tokens", 4096)

        messages = [{"role": "user", "content": prompt}]

        request_params = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True,
        }

        if tools:
            request_params["tools"] = self.format_tools(tools)
            request_params["tool_choice"] = "auto"

        stream = await self.client.chat.completions.create(**request_params)

        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    def supports_tools(self) -> bool:
        """GPT supports tool calling"""
        return True

    def format_tools(self, tools: List[Dict]) -> List[Dict]:
        """Format tools for OpenAI's API"""
        # OpenAI expects: type: "function", function: {name, description, parameters}
        formatted = []
        for tool in tools:
            formatted.append({
                "type": "function",
                "function": {
                    "name": tool.get("name"),
                    "description": tool.get("description"),
                    "parameters": tool.get("input_schema", tool.get("parameters", {})),
                }
            })
        return formatted
