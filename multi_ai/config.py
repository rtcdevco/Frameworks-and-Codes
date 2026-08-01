"""Configuration management for Multi-AI System"""

import os
from typing import Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()


class AIProviderConfig(BaseModel):
    """Configuration for an AI provider"""
    api_key: str
    model: str
    base_url: Optional[str] = None
    enabled: bool = True


class SystemConfig(BaseModel):
    """System-wide configuration"""
    log_level: str = Field(default="INFO")
    plugin_dir: str = Field(default="./plugins")
    default_provider: str = Field(default="claude")
    enable_consensus: bool = Field(default=False)
    rate_limit_rpm: int = Field(default=60)
    max_concurrent_requests: int = Field(default=5)
    request_timeout: int = Field(default=60)


class AirtableConfig(BaseModel):
    """Airtable configuration"""
    api_key: str
    base_id: str
    default_table: Optional[str] = None


class Config:
    """Main configuration loader"""

    def __init__(self):
        self.providers: Dict[str, AIProviderConfig] = {}
        self.system = SystemConfig(
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            plugin_dir=os.getenv("PLUGIN_DIR", "./plugins"),
            default_provider=os.getenv("DEFAULT_PROVIDER", "claude"),
            enable_consensus=os.getenv("ENABLE_CONSENSUS", "false").lower() == "true",
            rate_limit_rpm=int(os.getenv("RATE_LIMIT_RPM", "60")),
            max_concurrent_requests=int(os.getenv("MAX_CONCURRENT_REQUESTS", "5")),
            request_timeout=int(os.getenv("REQUEST_TIMEOUT", "60")),
        )
        self.airtable: Optional[AirtableConfig] = None
        self._load_providers()
        self._load_airtable()

    def _load_providers(self):
        """Load AI provider configurations from environment"""
        # OpenAI / GPT
        if os.getenv("OPENAI_API_KEY"):
            self.providers["gpt"] = AIProviderConfig(
                api_key=os.getenv("OPENAI_API_KEY"),
                model=os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview"),
            )

        # Anthropic / Claude
        if os.getenv("ANTHROPIC_API_KEY"):
            self.providers["claude"] = AIProviderConfig(
                api_key=os.getenv("ANTHROPIC_API_KEY"),
                model=os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022"),
            )

        # Google / Gemini
        if os.getenv("GOOGLE_API_KEY"):
            self.providers["gemini"] = AIProviderConfig(
                api_key=os.getenv("GOOGLE_API_KEY"),
                model=os.getenv("GEMINI_MODEL", "gemini-pro"),
            )

        # DeepSeek
        if os.getenv("DEEPSEEK_API_KEY"):
            self.providers["deepseek"] = AIProviderConfig(
                api_key=os.getenv("DEEPSEEK_API_KEY"),
                model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
                base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
            )

    def _load_airtable(self):
        """Load Airtable configuration"""
        if os.getenv("AIRTABLE_API_KEY") and os.getenv("AIRTABLE_BASE_ID"):
            self.airtable = AirtableConfig(
                api_key=os.getenv("AIRTABLE_API_KEY"),
                base_id=os.getenv("AIRTABLE_BASE_ID"),
                default_table=os.getenv("AIRTABLE_DEFAULT_TABLE"),
            )

    def get_provider_config(self, provider: str) -> Optional[AIProviderConfig]:
        """Get configuration for a specific provider"""
        return self.providers.get(provider)

    def list_enabled_providers(self) -> list[str]:
        """List all enabled AI providers"""
        return [name for name, config in self.providers.items() if config.enabled]


# Global config instance
config = Config()
