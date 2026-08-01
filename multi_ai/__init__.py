"""
Multi-AI Orchestration System

A modular AI orchestration platform that coordinates multiple AI providers
and enables them to interact with external services through plugins.
"""

__version__ = "0.1.0"

from multi_ai.orchestrator import MultiAIOrchestrator, Provider

__all__ = ["MultiAIOrchestrator", "Provider"]
