"""Base Plugin interface"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Callable, Awaitable


class Tool:
    """Represents a plugin tool/capability"""

    def __init__(
        self,
        name: str,
        description: str,
        input_schema: Dict[str, Any],
        handler: Callable[..., Awaitable[Any]]
    ):
        self.name = name
        self.description = description
        self.input_schema = input_schema
        self.handler = handler

    def to_dict(self) -> Dict[str, Any]:
        """Convert tool to dictionary format for AI providers"""
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema,
        }


class BasePlugin(ABC):
    """Abstract base class for plugins"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.name = self.__class__.__name__.replace("Plugin", "").lower()
        self.tools: List[Tool] = []
        self._register_tools()

    @abstractmethod
    def _register_tools(self):
        """Register available tools - implement in subclass"""
        pass

    @abstractmethod
    async def initialize(self):
        """Initialize plugin (connections, auth, etc) - implement in subclass"""
        pass

    @abstractmethod
    async def cleanup(self):
        """Cleanup resources on shutdown - implement in subclass"""
        pass

    def get_tools(self) -> List[Tool]:
        """Return available tools"""
        return self.tools

    def get_tools_dict(self) -> List[Dict[str, Any]]:
        """Return tools as dictionaries for AI providers"""
        return [tool.to_dict() for tool in self.tools]

    async def execute_tool(self, tool_name: str, **kwargs) -> Any:
        """Execute a specific tool by name"""
        tool = next((t for t in self.tools if t.name == tool_name), None)
        if not tool:
            raise ValueError(f"Tool '{tool_name}' not found in plugin '{self.name}'")

        return await tool.handler(**kwargs)

    def __repr__(self):
        return f"<{self.__class__.__name__} tools={len(self.tools)}>"
