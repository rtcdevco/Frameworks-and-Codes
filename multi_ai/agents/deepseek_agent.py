"""DeepSeek Agent implementation"""

from typing import Dict, Any, List, Optional, AsyncIterator
import httpx
import json
from multi_ai.agents.base_agent import BaseAgent


class DeepSeekAgent(BaseAgent):
    """DeepSeek agent implementation using OpenAI-compatible API"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.base_url = config.get("base_url", "https://api.deepseek.com")
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            timeout=60.0,
        )

    async def send_message(
        self,
        prompt: str,
        tools: Optional[List[Dict]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Send message to DeepSeek and get response"""

        temperature = kwargs.get("temperature", 1.0)
        max_tokens = kwargs.get("max_tokens", 4096)

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        if tools:
            payload["tools"] = self.format_tools(tools)

        response = await self.client.post("/v1/chat/completions", json=payload)
        response.raise_for_status()
        data = response.json()

        message = data["choices"][0]["message"]

        result = {
            "content": message.get("content", ""),
            "tool_calls": [],
            "stop_reason": data["choices"][0].get("finish_reason", "stop"),
            "usage": {
                "input_tokens": data.get("usage", {}).get("prompt_tokens", 0),
                "output_tokens": data.get("usage", {}).get("completion_tokens", 0),
            }
        }

        # Extract tool calls if present
        if "tool_calls" in message and message["tool_calls"]:
            for tool_call in message["tool_calls"]:
                result["tool_calls"].append({
                    "id": tool_call.get("id"),
                    "name": tool_call["function"]["name"],
                    "input": json.loads(tool_call["function"]["arguments"]),
                })

        return result

    async def stream_message(
        self,
        prompt: str,
        tools: Optional[List[Dict]] = None,
        **kwargs
    ) -> AsyncIterator[str]:
        """Stream response from DeepSeek"""

        temperature = kwargs.get("temperature", 1.0)
        max_tokens = kwargs.get("max_tokens", 4096)

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True,
        }

        if tools:
            payload["tools"] = self.format_tools(tools)

        async with self.client.stream("POST", "/v1/chat/completions", json=payload) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data_str = line[6:]  # Remove "data: " prefix
                    if data_str.strip() == "[DONE]":
                        break

                    try:
                        data = json.loads(data_str)
                        if data["choices"][0]["delta"].get("content"):
                            yield data["choices"][0]["delta"]["content"]
                    except json.JSONDecodeError:
                        continue

    def supports_tools(self) -> bool:
        """DeepSeek supports tool calling"""
        return True

    def format_tools(self, tools: List[Dict]) -> List[Dict]:
        """Format tools for DeepSeek's API (OpenAI-compatible)"""
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

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close HTTP client on exit"""
        await self.client.aclose()
