"""
plan/policy Approver — thin wrapper delegating to an ApprovalStrategy.

The actual approval logic (LLM judge, HITL prompt, auto-approve, …) is
provided by an :class:`~secure_agent.protocols.ApprovalStrategy` implementor
so the caller can choose (or build) the strategy that fits their deployment.
"""

from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from secure_agent.core.models import ApproverDecision, PlanAndPolicy

if TYPE_CHECKING:
    from secure_agent.protocols import ApprovalStrategy


def approve_plan_policy(
    strategy: ApprovalStrategy,
    proposed: PlanAndPolicy,
    previous: Optional[PlanAndPolicy] = None,
) -> ApproverDecision:
    """Delegate approval of *proposed* to the given *strategy*."""
    return strategy.review(proposed, previous)
