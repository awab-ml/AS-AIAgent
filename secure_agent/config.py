"""
Configuration dataclass for the SecureAgent SDK.

All behavioural knobs live here so they can be passed around immutably
instead of relying on scattered environment variables.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class AgentConfig:
    """Immutable runtime configuration for a :class:`SecureAgent` instance.

    Parameters
    ----------
    max_iterations:
        Hard ceiling on the orchestrate → execute loop to prevent runaways.
    context:
        Static context string injected into every orchestrator prompt
        (e.g. available tools, domain constraints).
    headless:
        When ``True`` the SDK will *never* emit Rich console output.
        Useful for embedding inside REST APIs, background workers, or tests.
    """

    max_iterations: int = 10
    context: str = ""
    headless: bool = False
