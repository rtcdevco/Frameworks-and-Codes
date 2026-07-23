"""Plugin Manager - discovers and loads plugins"""

import json
import importlib.util
from pathlib import Path
from typing import Dict, List, Any, Optional
from multi_ai.plugins.base_plugin import BasePlugin, Tool


class PluginManager:
    """Manages plugin lifecycle and discovery"""

    def __init__(self, plugin_dir: str = "./plugins"):
        self.plugin_dir = Path(plugin_dir)
        self.loaded_plugins: Dict[str, BasePlugin] = {}

    def discover_plugins(self) -> List[Dict[str, Any]]:
        """Find all plugins with plugin.json manifest"""
        plugins = []

        if not self.plugin_dir.exists():
            print(f"Plugin directory {self.plugin_dir} does not exist")
            return plugins

        for plugin_path in self.plugin_dir.iterdir():
            if not plugin_path.is_dir():
                continue

            manifest_path = plugin_path / "plugin.json"
            if manifest_path.exists():
                try:
                    with open(manifest_path) as f:
                        manifest = json.load(f)
                        manifest['path'] = plugin_path
                        plugins.append(manifest)
                except Exception as e:
                    print(f"Error reading manifest for {plugin_path.name}: {e}")

        return plugins

    async def load_plugin(self, manifest: Dict[str, Any]) -> BasePlugin:
        """Dynamically load a plugin from its manifest"""

        plugin_path = manifest['path']
        entry_point = manifest['entry_point']
        plugin_name = manifest['name']

        # Parse entry_point: "module.py:ClassName"
        module_file, class_name = entry_point.split(':')
        module_path = plugin_path / module_file

        if not module_path.exists():
            raise FileNotFoundError(f"Plugin module not found: {module_path}")

        # Dynamic import
        spec = importlib.util.spec_from_file_location(
            f"plugin_{plugin_name}",
            module_path
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Instantiate plugin
        plugin_class = getattr(module, class_name)
        plugin_config = manifest.get('config', {})

        # Resolve environment variables if specified
        resolved_config = self._resolve_config(plugin_config, manifest.get('config_schema', {}))

        plugin = plugin_class(resolved_config)
        await plugin.initialize()

        self.loaded_plugins[plugin_name] = plugin
        print(f"✓ Loaded plugin: {plugin_name} ({len(plugin.get_tools())} tools)")

        return plugin

    def _resolve_config(self, config: Dict[str, Any], schema: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve configuration from environment variables"""
        import os

        resolved = {}
        properties = schema.get('properties', {})

        for key, prop_schema in properties.items():
            # Check if there's an environment variable mapping
            env_var = prop_schema.get('env')
            if env_var:
                value = os.getenv(env_var)
                if value:
                    resolved[key] = value
                elif key in config:
                    resolved[key] = config[key]
            elif key in config:
                resolved[key] = config[key]

        return resolved

    async def load_all_plugins(self) -> List[str]:
        """Discover and load all available plugins"""
        plugins = self.discover_plugins()
        loaded_names = []

        for manifest in plugins:
            try:
                await self.load_plugin(manifest)
                loaded_names.append(manifest['name'])
            except Exception as e:
                print(f"✗ Failed to load plugin {manifest['name']}: {e}")

        return loaded_names

    def get_plugin(self, name: str) -> Optional[BasePlugin]:
        """Get a loaded plugin by name"""
        return self.loaded_plugins.get(name)

    def get_all_tools(self) -> List[Tool]:
        """Get all tools from all loaded plugins"""
        tools = []
        for plugin in self.loaded_plugins.values():
            tools.extend(plugin.get_tools())
        return tools

    def get_all_tools_dict(self) -> List[Dict[str, Any]]:
        """Get all tools as dictionaries for AI providers"""
        tools = []
        for plugin in self.loaded_plugins.values():
            tools.extend(plugin.get_tools_dict())
        return tools

    async def execute_tool(self, tool_name: str, **kwargs) -> Any:
        """Execute a tool from any loaded plugin"""
        for plugin in self.loaded_plugins.values():
            try:
                return await plugin.execute_tool(tool_name, **kwargs)
            except ValueError:
                continue  # Tool not in this plugin

        raise ValueError(f"Tool '{tool_name}' not found in any loaded plugin")

    async def cleanup_all(self):
        """Cleanup all loaded plugins"""
        for plugin in self.loaded_plugins.values():
            try:
                await plugin.cleanup()
            except Exception as e:
                print(f"Error cleaning up plugin {plugin.name}: {e}")

    def list_plugins(self) -> List[Dict[str, Any]]:
        """List all loaded plugins with their info"""
        return [
            {
                "name": name,
                "tools_count": len(plugin.get_tools()),
                "tools": [t.name for t in plugin.get_tools()],
            }
            for name, plugin in self.loaded_plugins.items()
        ]

    async def __aenter__(self):
        """Async context manager entry"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.cleanup_all()
