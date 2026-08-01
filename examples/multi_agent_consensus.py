"""
Multi-Agent Consensus Example

Get answers from multiple AIs and synthesize them
"""

import asyncio
from multi_ai import MultiAIOrchestrator, Provider


async def main():
    print("=== Multi-Agent Consensus Example ===\n")

    orchestrator = MultiAIOrchestrator()

    # Question to ask all AIs
    question = """
    What are the top 3 benefits of using multiple AI providers
    instead of relying on just one?
    """

    print(f"Question: {question}\n")
    print("Consulting all available AI providers...\n")

    # Get consensus from all providers
    result = await orchestrator.multi_agent_consensus(
        prompt=question,
        max_tokens=200
    )

    # Show individual responses
    print("=== Individual Responses ===\n")
    for provider, response in result['individual_responses'].items():
        print(f"{provider.upper()}:")
        print(f"{response['content']}\n")
        print(f"Tokens used: {response['usage']}\n")
        print("-" * 60 + "\n")

    # Show synthesis
    print("=== Synthesized Consensus ===\n")
    print(result['synthesis'])

    print(f"\n\nProviders consulted: {result['providers_consulted']}")
    print("\n✓ Consensus example complete!")


if __name__ == "__main__":
    asyncio.run(main())
