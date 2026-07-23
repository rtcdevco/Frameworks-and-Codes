"""Multi-AI Orchestrator - coordinates multiple AI providers"""

from enum import Enum
from typing import Dict, Any, List, Optional, AsyncIterator
from multi_ai.config import config
from multi_ai.agents import ClaudeAgent, GPTAgent, GeminiAgent, DeepSeekAgent


class Provider(str, Enum):
    """Available AI providers"""
    GPT = "gpt"
    CLAUDE = "claude"
    GEMINI = "gemini"
    DEEPSEEK = "deepseek"


class MultiAIOrchestrator:
    """Coordinates multiple AI providers and routing"""

    _instance = None

    def __init__(self):
        self.config = config
        self.agents: Dict[Provider, Any] = {}
        self._load_agents()

    @classmethod
    def get_instance(cls):
        """Get singleton instance"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _load_agents(self):
        """Initialize all configured AI agents"""

        agent_classes = {
            "gpt": GPTAgent,
            "claude": ClaudeAgent,
            "gemini": GeminiAgent,
            "deepseek": DeepSeekAgent,
        }

        for provider_name, agent_class in agent_classes.items():
            provider_config = self.config.get_provider_config(provider_name)
            if provider_config and provider_config.enabled:
                try:
                    self.agents[Provider(provider_name)] = agent_class({
                        "api_key": provider_config.api_key,
                        "model": provider_config.model,
                        "base_url": provider_config.base_url,
                    })
                    print(f"✓ Loaded {provider_name} agent ({provider_config.model})")
                except Exception as e:
                    print(f"✗ Failed to load {provider_name} agent: {e}")

    async def route_request(
        self,
        prompt: str,
        provider: Optional[Provider] = None,
        tools: Optional[List[Dict]] = None,
        stream: bool = False,
        **kwargs
    ) -> Dict[str, Any] | AsyncIterator[str]:
        """
        Route request to appropriate agent

        Args:
            prompt: The message/prompt to send
            provider: Specific provider to use (None for auto-routing)
            tools: Optional tools the AI can use
            stream: Whether to stream the response
            **kwargs: Additional parameters for the agent

        Returns:
            Response dict or async iterator if streaming
        """

        # Select provider
        if provider:
            if provider not in self.agents:
                raise ValueError(f"Provider {provider} not available. Available: {self.list_providers()}")
            selected_provider = provider
        else:
            selected_provider = self._auto_route(prompt, tools)

        agent = self.agents[selected_provider]

        # Execute request
        if stream:
            return agent.stream_message(prompt, tools=tools, **kwargs)
        else:
            response = await agent.send_message(prompt, tools=tools, **kwargs)
            response["provider"] = selected_provider.value
            return response

    def _auto_route(self, prompt: str, tools: Optional[List[Dict]] = None) -> Provider:
        """
        Automatically select best agent for task

        Logic:
        1. If tools are needed -> prefer Claude or GPT (best tool support)
        2. If code-related -> prefer DeepSeek
        3. Otherwise -> use default provider from config
        """

        # If tools are needed, prefer Claude or GPT
        if tools:
            if Provider.CLAUDE in self.agents:
                return Provider.CLAUDE
            elif Provider.GPT in self.agents:
                return Provider.GPT

        # Check for code-related keywords
        code_keywords = ["code", "function", "class", "debug", "implement", "refactor"]
        if any(keyword in prompt.lower() for keyword in code_keywords):
            if Provider.DEEPSEEK in self.agents:
                return Provider.DEEPSEEK

        # Use default provider
        default = self.config.system.default_provider
        if default and Provider(default) in self.agents:
            return Provider(default)

        # Fallback: first available agent
        return list(self.agents.keys())[0]

    async def multi_agent_consensus(
        self,
        prompt: str,
        providers: Optional[List[Provider]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Get consensus from multiple agents

        Args:
            prompt: The question/prompt
            providers: List of providers to consult (None = all)
            **kwargs: Additional parameters

        Returns:
            Dict with individual responses and synthesis
        """

        if providers is None:
            providers = list(self.agents.keys())

        responses = {}

        # Collect responses from each provider
        for provider in providers:
            if provider in self.agents:
                try:
                    response = await self.agents[provider].send_message(prompt, **kwargs)
                    responses[provider.value] = {
                        "content": response["content"],
                        "usage": response["usage"],
                    }
                except Exception as e:
                    responses[provider.value] = {
                        "content": f"Error: {str(e)}",
                        "usage": {"input_tokens": 0, "output_tokens": 0},
                    }

        # Synthesize consensus using Claude (if available)
        synthesis = await self._synthesize_responses(responses)

        return {
            "individual_responses": responses,
            "synthesis": synthesis,
            "providers_consulted": [p.value for p in providers if p in self.agents],
        }

    async def _synthesize_responses(self, responses: Dict[str, Dict]) -> str:
        """Synthesize multiple responses into a consensus"""

        # Use Claude for synthesis if available, otherwise GPT
        synthesizer = None
        if Provider.CLAUDE in self.agents:
            synthesizer = self.agents[Provider.CLAUDE]
        elif Provider.GPT in self.agents:
            synthesizer = self.agents[Provider.GPT]

        if not synthesizer:
            # Fallback: simple concatenation
            return "\n\n".join([
                f"**{provider}**: {resp['content']}"
                for provider, resp in responses.items()
            ])

        # Build synthesis prompt
        synthesis_prompt = "I asked multiple AI systems the same question. Here are their responses:\n\n"
        for provider, resp in responses.items():
            synthesis_prompt += f"**{provider.upper()}**:\n{resp['content']}\n\n"

        synthesis_prompt += (
            "Please synthesize these responses into a single, coherent answer. "
            "Highlight areas of agreement, note any disagreements, and provide "
            "a balanced synthesis."
        )

        result = await synthesizer.send_message(synthesis_prompt)
        return result["content"]

    def list_providers(self) -> List[str]:
        """List all available providers"""
        return [p.value for p in self.agents.keys()]

    def get_provider_info(self, provider: Provider) -> Dict[str, Any]:
        """Get information about a specific provider"""
        if provider not in self.agents:
            return {"available": False}

        agent = self.agents[provider]
        return {
            "available": True,
            "model": agent.model,
            "supports_tools": agent.supports_tools(),
        }

    async def __aenter__(self):
        """Async context manager entry"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit - cleanup all agents"""
        for agent in self.agents.values():
            await agent.__aexit__(exc_type, exc_val, exc_tb)
