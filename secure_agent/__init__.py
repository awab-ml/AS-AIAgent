"""
AS-AIAgent SDK — System-level defense architecture for AI agents.

Quick start::

    from secure_agent import SecureAgent

    agent = SecureAgent()
    result = agent.run("Read my emails and process urgent payments")
    print(result.history)
"""

from secure_agent.client import AgentRunResult, SecureAgent
from secure_agent.config import AgentConfig
from secure_agent.core.models import (
    ApproverDecision,
    ExecutorOutput,
    IntendedInstruction,
    Plan,
    PlanAndPolicy,
    Policy,
    PolicyRule,
    Step,
    ToolCall,
)
from secure_agent.protocols import (
    ApprovalStrategy,
    EventLogger,
    LLMProvider,
    ToolExecutor,
)

__all__ = [
    # Client
    "SecureAgent",
    "AgentRunResult",
    "AgentConfig",
    # Protocols
    "LLMProvider",
    "ToolExecutor",
    "ApprovalStrategy",
    "EventLogger",
    # Models
    "ApproverDecision",
    "ExecutorOutput",
    "IntendedInstruction",
    "Plan",
    "PlanAndPolicy",
    "Policy",
    "PolicyRule",
    "Step",
    "ToolCall",
]
