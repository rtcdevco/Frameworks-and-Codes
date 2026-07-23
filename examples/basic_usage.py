"""
Basic Multi-AI System Usage Example

Shows how to use the orchestrator with different AI providers
"""

import asyncio
from multi_ai import MultiAIOrchestrator, Provider


async def main():
    print("=== Multi-AI System - Basic Usage ===\n")

    # Initialize orchestrator
    orchestrator = MultiAIOrchestrator()

    print(f"Available providers: {orchestrator.list_providers()}\n")

    # Example 1: Use specific provider
    print("1. Using Claude specifically:")
    response = await orchestrator.route_request(
        prompt="Explain what a Multi-AI orchestrator is in one sentence.",
        provider=Provider.CLAUDE
    )
    print(f"   {response['content'][:200]}...")
    print(f"   Provider: {response['provider']}")
    print(f"   Tokens: {response['usage']}\n")

    # Example 2: Auto-routing (code-related -> DeepSeek)
    print("2. Auto-routing for code question:")
    response = await orchestrator.route_request(
        prompt="Write a Python function to calculate fibonacci numbers.",
        provider=None  # Auto-route
    )
    print(f"   Selected provider: {response['provider']}")
    print(f"   Response: {response['content'][:150]}...\n")

    # Example 3: Streaming response
    print("3. Streaming response from GPT:")
    print("   ", end="", flush=True)
    stream = await orchestrator.route_request(
        prompt="Count from 1 to 5 slowly.",
        provider=Provider.GPT,
        stream=True
    )
    async for chunk in stream:
        print(chunk, end="", flush=True)
    print("\n")

    # Example 4: Provider information
    print("4. Provider information:")
    for provider_name in orchestrator.list_providers():
        info = orchestrator.get_provider_info(Provider(provider_name))
        print(f"   {provider_name}: {info}")

    print("\n✓ Examples complete!")


if __name__ == "__main__":
    asyncio.run(main())
