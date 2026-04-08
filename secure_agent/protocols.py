"""
Protocol definitions for the AS-AIAgent SDK.

These protocols define the contracts that users can implement to inject
their own LLM providers, tool executors, approval strategies, and loggers
into the secure agent pipeline.

All protocols use ``typing.Protocol`` (structural subtyping) so implementors
do **not** need to inherit from these classes — they just need to satisfy the
method signatures.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Protocol, Type, TypeVar, runtime_checkable

from pydantic import BaseModel

from secure_agent.core.models import ApproverDecision, PlanAndPolicy

T = TypeVar("T", bound=BaseModel)


# ---------------------------------------------------------------------------
# LLM Provider
# ---------------------------------------------------------------------------

@runtime_checkable
class LLMProvider(Protocol):
    """Contract for any LLM backend (OpenAI, Anthropic, local, mock, …)."""

    def generate_structured(
        self,
        prompt: str,
        response_model: Type[T],
        system_prompt: str = "You are a helpful AI.",
    ) -> T:
        """Return a Pydantic model instance parsed from the LLM response."""
        ...

    def generate_text(
        self,
        prompt: str,
        system_prompt: str = "You are a helpful AI.",
    ) -> str:
        """Return a plain-text LLM response."""
        ...


# ---------------------------------------------------------------------------
# Tool Executor
# ---------------------------------------------------------------------------

@runtime_checkable
class ToolExecutor(Protocol):
    """Contract for an environment that can execute named tool calls."""

    def execute(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Run *tool_name* with the given keyword arguments and return a result string."""
        ...

    def list_tools(self) -> List[str]:
        """Return the names of all tools available in this environment."""
        ...


# ---------------------------------------------------------------------------
# Approval Strategy
# ---------------------------------------------------------------------------

@runtime_checkable
class ApprovalStrategy(Protocol):
    """Contract for a plan/policy approval mechanism (LLM judge, HITL, auto, …)."""

    def review(
        self,
        proposed: PlanAndPolicy,
        previous: Optional[PlanAndPolicy] = None,
    ) -> ApproverDecision:
        """Evaluate *proposed* against *previous* and return an approval decision."""
        ...


# ---------------------------------------------------------------------------
# Event Logger
# ---------------------------------------------------------------------------

@runtime_checkable
class EventLogger(Protocol):
    """Contract for an audit/event logger.

    Implementors can choose to handle any subset of these methods; the SDK
    will always call them, but a no-op implementation is perfectly valid.
    """

    def on_orchestration(self, plan: dict, policy: dict) -> None:
        """Called after a new plan + policy is generated."""
        ...

    def on_approval(self, decision: dict) -> None:
        """Called after the approval strategy returns a verdict."""
        ...

    def on_execution(self, executor_output: dict) -> None:
        """Called after the executor proposes a tool call."""
        ...

    def on_enforcement(self, is_allowed: bool, reason: str = "") -> None:
        """Called after the enforcer evaluates the proposed action."""
        ...

    def on_environment(self, output: str) -> None:
        """Called after the tool executor returns a result."""
        ...
