# 🤖 Multi-AI Orchestration System + Airtable Plugin

A modular AI orchestration platform that coordinates multiple AI providers (GPT, Claude, Gemini, DeepSeek) and enables them to interact with external services through an extensible plugin system.

## ✨ Features

- **🎯 Multi-AI Orchestration**: Use 4 different AI providers from one unified interface
- **🧩 Plugin System**: Extensible architecture for adding new capabilities
- **🔧 Airtable Integration**: AI-powered data organization and CRUD operations
- **🤝 Multi-Agent Consensus**: Get answers from multiple AIs and synthesize them
- **⚡ Smart Routing**: Automatically select the best AI for each task
- **🛠️ Tool Support**: AIs can use external tools to accomplish complex tasks

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

Copy the example environment file and add your API keys:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```env
# At minimum, you need ONE AI provider:
ANTHROPIC_API_KEY=sk-ant-...
CLAUDE_MODEL=claude-3-5-sonnet-20241022

# Airtable (for the plugin)
AIRTABLE_API_KEY=pat...
AIRTABLE_BASE_ID=appXXXXXXXXXXXXXX
```

**Getting API Keys:**
- **Anthropic (Claude)**: https://console.anthropic.com/settings/keys
- **OpenAI (GPT)**: https://platform.openai.com/api-keys
- **Google (Gemini)**: https://makersuite.google.com/app/apikey
- **DeepSeek**: https://platform.deepseek.com/api_keys
- **Airtable**: https://airtable.com/create/tokens

### 3. Run Examples

```bash
# Basic usage
python examples/basic_usage.py

# Airtable integration
python examples/airtable_integration.py

# Multi-agent consensus
python examples/multi_agent_consensus.py
```

## 📚 Usage Examples

### Basic AI Request

```python
import asyncio
from multi_ai import MultiAIOrchestrator, Provider

async def main():
    orchestrator = MultiAIOrchestrator()

    # Use specific provider
    response = await orchestrator.route_request(
        prompt="Explain quantum computing in one sentence.",
        provider=Provider.CLAUDE
    )

    print(response['content'])

asyncio.run(main())
```

### AI with Airtable Tools

```python
import asyncio
from multi_ai import MultiAIOrchestrator, Provider
from multi_ai.plugins import PluginManager

async def main():
    orchestrator = MultiAIOrchestrator()
    plugin_manager = PluginManager("./plugins")

    # Load Airtable plugin
    await plugin_manager.load_all_plugins()
    tools = plugin_manager.get_all_tools_dict()

    # AI can now use Airtable tools
    response = await orchestrator.route_request(
        prompt="Create a record in the 'Tasks' table with Title='Build AI system' and Status='In Progress'",
        provider=Provider.CLAUDE,
        tools=tools
    )

    # Execute tool calls
    if response.get('tool_calls'):
        for tool_call in response['tool_calls']:
            result = await plugin_manager.execute_tool(
                tool_call['name'],
                **tool_call['input']
            )
            print(f"Created: {result}")

    await plugin_manager.cleanup_all()

asyncio.run(main())
```

### Multi-Agent Consensus

```python
import asyncio
from multi_ai import MultiAIOrchestrator

async def main():
    orchestrator = MultiAIOrchestrator()

    # Get answers from multiple AIs
    result = await orchestrator.multi_agent_consensus(
        prompt="What's the future of AI in 2025?"
    )

    # Individual responses
    for provider, response in result['individual_responses'].items():
        print(f"{provider}: {response['content']}\n")

    # Synthesized answer
    print(f"Synthesis: {result['synthesis']}")

asyncio.run(main())
```

## 🔌 Airtable Plugin

The Airtable plugin provides tools for AI-powered data operations:

### Available Tools

| Tool | Description |
|------|-------------|
| `airtable_list_records` | List records with filtering and sorting |
| `airtable_create_record` | Create a new record |
| `airtable_update_record` | Update existing record |
| `airtable_delete_record` | Delete a record |
| `airtable_bulk_create` | Create multiple records at once |

### Example: AI Organizing Data

```python
# AI can analyze data and organize it in Airtable
prompt = """
Scan the local 'research/' directory for markdown files.
For each file, create a record in the 'Research' Airtable table with:
- Title: filename
- Category: determined by analyzing content
- Tags: extracted keywords
- Summary: brief description

Use airtable_bulk_create to import them all.
"""

response = await orchestrator.route_request(
    prompt=prompt,
    provider=Provider.CLAUDE,
    tools=airtable_tools
)
```

## 🏗️ Project Structure

```
Frameworks-and-Codes/
├── multi_ai/                   # Core system
│   ├── agents/                 # AI provider implementations
│   │   ├── base_agent.py
│   │   ├── claude_agent.py
│   │   ├── gpt_agent.py
│   │   ├── gemini_agent.py
│   │   └── deepseek_agent.py
│   ├── plugins/                # Plugin system
│   │   ├── base_plugin.py
│   │   └── plugin_manager.py
│   ├── orchestrator.py         # Main coordinator
│   └── config.py               # Configuration
│
├── plugins/                    # External plugins
│   └── airtable/               # Airtable plugin
│       ├── plugin.json
│       └── airtable_plugin.py
│
├── examples/                   # Usage examples
│   ├── basic_usage.py
│   ├── airtable_integration.py
│   └── multi_agent_consensus.py
│
├── requirements.txt
├── .env.example
└── README.md
```

## 🎯 AI Provider Selection

The orchestrator automatically selects the best AI for each task:

| Task Type | Preferred AI | Reason |
|-----------|--------------|--------|
| Tool use | Claude | Best tool-calling support |
| Code | DeepSeek | Code-specialized model |
| General | Claude/GPT | Most capable |
| Multimodal | Gemini | Native multimodal support |

Override auto-selection:
```python
response = await orchestrator.route_request(
    prompt="...",
    provider=Provider.GPT  # Force GPT
)
```

## 🔧 Configuration

### System Settings

Edit `.env` to configure:

```env
# Default AI provider
DEFAULT_PROVIDER=claude

# Enable multi-agent consensus by default
ENABLE_CONSENSUS=false

# Rate limiting
RATE_LIMIT_RPM=60

# Max concurrent requests
MAX_CONCURRENT_REQUESTS=5
```

### Adding More Plugins

Create a new plugin:

1. Create directory: `plugins/your-plugin/`
2. Add `plugin.json` manifest
3. Implement plugin class extending `BasePlugin`
4. Register tools in `_register_tools()`

Example structure:
```
plugins/your-plugin/
├── plugin.json
└── your_plugin.py
```

## 📊 Performance

- **Response time**: 1-5 seconds (depends on AI provider)
- **Token usage**: Tracked per request
- **Rate limits**: Configurable per provider
- **Concurrent requests**: Up to 5 simultaneous

## 🐛 Troubleshooting

### "Provider X not available"
- Check your API key in `.env`
- Ensure the provider is enabled
- Run `python -c "from multi_ai import MultiAIOrchestrator; print(MultiAIOrchestrator().list_providers())"`

### "Airtable plugin not loaded"
- Verify `AIRTABLE_API_KEY` and `AIRTABLE_BASE_ID` in `.env`
- Check base ID starts with `app`
- Ensure you have access to the base

### "Tool not found"
- Plugin may not be loaded
- Check plugin manifest matches tool name
- Verify plugin initialization succeeded

## 🔐 Security

- **Never commit `.env`** - it contains API keys
- Use environment-specific configs (`.env.local`, `.env.production`)
- Rotate API keys regularly
- Limit Airtable token permissions to specific bases

## 📖 Documentation

- [Implementation Plan](IMPLEMENTATION_PLAN.md) - Detailed build guide
- [Architecture](ARCHITECTURE.md) - System design and patterns
- [Decision Guide](DECISION_GUIDE.md) - Choosing the right approach

## 🎓 Examples & Use Cases

### 1. Research Organization
```python
# AI scans files and organizes them in Airtable
prompt = "Scan research/ folder and categorize all PDFs into Airtable"
```

### 2. Data Analysis
```python
# Multi-agent analysis
result = await orchestrator.multi_agent_consensus(
    prompt="Analyze this dataset and suggest improvements"
)
```

### 3. Automated Workflows
```python
# AI chains multiple tools
prompt = "Read records from Airtable, analyze them, create a summary document"
```

## 🚧 Roadmap

- [ ] Web dashboard (FastAPI + React)
- [ ] More plugins (GitHub, Slack, Notion)
- [ ] MCP server support
- [ ] Workflow automation
- [ ] Memory/context persistence
- [ ] Cost tracking and budgets

## 🤝 Contributing

This is currently a personal project, but suggestions welcome!

## 📄 License

MIT License - use freely!

## 🙏 Acknowledgments

- Anthropic (Claude API)
- OpenAI (GPT API)
- Google (Gemini API)
- DeepSeek (DeepSeek API)
- Airtable (Airtable API)

---

**Built with [Claude Code](https://claude.com/claude-code)** 🤖

For questions or issues, create an issue on GitHub!
