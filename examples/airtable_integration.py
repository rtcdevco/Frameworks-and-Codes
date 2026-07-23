"""
Airtable Integration Example

Demonstrates AI-powered Airtable operations using the Multi-AI system
"""

import asyncio
from multi_ai import MultiAIOrchestrator, Provider
from multi_ai.plugins import PluginManager


async def main():
    print("=== Multi-AI + Airtable Integration ===\n")

    # Initialize orchestrator and plugin manager
    orchestrator = MultiAIOrchestrator()
    plugin_manager = PluginManager("./plugins")

    # Load all plugins (including Airtable)
    loaded = await plugin_manager.load_all_plugins()
    print(f"Loaded plugins: {loaded}\n")

    # Get Airtable plugin
    airtable_plugin = plugin_manager.get_plugin("airtable")
    if not airtable_plugin:
        print("✗ Airtable plugin not loaded. Check your .env file.")
        return

    # Get tools for AI to use
    tools = airtable_plugin.get_tools_dict()
    print(f"Airtable tools available: {[t['name'] for t in tools]}\n")

    # Example 1: AI creates a record
    print("1. AI creating a record in Airtable:")
    prompt = """
    Create a new record in the 'Research' table with these fields:
    - Title: "Multi-AI Orchestration System"
    - Category: "Framework"
    - Status: "Active"
    - Tags: "AI, Automation, Integration"
    - Description: "A system that coordinates multiple AI providers"

    Use the airtable_create_record tool to do this.
    """

    response = await orchestrator.route_request(
        prompt=prompt,
        provider=Provider.CLAUDE,  # Claude is best with tools
        tools=tools
    )

    print(f"   AI Response: {response['content']}")

    # Check if AI used tools
    if response.get('tool_calls'):
        print(f"\n   AI called tools:")
        for tool_call in response['tool_calls']:
            print(f"   - {tool_call['name']}: {tool_call['input']}")

            # Execute the tool
            result = await plugin_manager.execute_tool(
                tool_call['name'],
                **tool_call['input']
            )
            print(f"     Result: {result}\n")

    # Example 2: AI lists records
    print("\n2. AI listing records:")
    prompt = """
    List all records from the 'Research' table.
    Use the airtable_list_records tool.
    Show me the first 3 records.
    """

    response = await orchestrator.route_request(
        prompt=prompt,
        provider=Provider.CLAUDE,
        tools=tools
    )

    if response.get('tool_calls'):
        for tool_call in response['tool_calls']:
            result = await plugin_manager.execute_tool(
                tool_call['name'],
                **tool_call['input']
            )
            print(f"   Found {len(result)} records")
            for i, record in enumerate(result[:3], 1):
                print(f"   {i}. {record['fields']}")

    # Example 3: Direct tool execution (without AI)
    print("\n3. Direct tool execution (no AI):")
    records = await airtable_plugin.execute_tool(
        "airtable_list_records",
        table_name="Research",
        max_records=5
    )
    print(f"   Retrieved {len(records)} records directly\n")

    # Cleanup
    await plugin_manager.cleanup_all()

    print("✓ Airtable integration examples complete!")


if __name__ == "__main__":
    asyncio.run(main())
