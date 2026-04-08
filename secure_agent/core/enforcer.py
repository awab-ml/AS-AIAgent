"""
Policy Enforcer — blocks tool calls that violate the dynamic policy or
originate from untrusted instruction sources.

Also serves as the checkpoint for Proposal 1, Step 2: trusted-vs-untrusted
provenance constraints.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from secure_agent.core.models import ExecutorOutput, Policy


class PolicyViolation(Exception):
    """Raised when an action violates the active security policy."""


@dataclass(frozen=True)
class EnforcementResult:
    """Structured outcome from :func:`enforce_policy`."""
    allowed: bool
    reason: str = ""


def enforce_policy(policy: Policy, proposed: ExecutorOutput) -> EnforcementResult:
    """Evaluate *proposed* against *policy* and return an :class:`EnforcementResult`.

    The function is **pure** — no Rich output, no side-effects.
    """
    if not proposed.tool_call:
        return EnforcementResult(allowed=True, reason="No tool call to enforce.")

    tool_name = proposed.tool_call.tool_name

    # 1. Enforce provenance constraints (Proposal 1 — untrusted sources)
    for inst in proposed.verbalized_instructions:
        source_lower = inst.source_hypothesis.lower()
        untrusted_keywords = ("environment", "untrusted", "web", "email")
        if any(kw in source_lower for kw in untrusted_keywords):
            return EnforcementResult(
                allowed=False,
                reason=(
                    f"Untrusted provenance detected in intended instruction: "
                    f"'{inst.instruction_text}' (source: {inst.source_hypothesis})"
                ),
            )

    # 2. Rule-based policy evaluation
    allowed = False
    for rule in policy.rules:
        if rule.action == tool_name or rule.action == "*":
            if rule.effect == "allow":
                allowed = True
            elif rule.effect == "deny":
                allowed = False  # Deny overrides

    if not allowed:
        return EnforcementResult(
            allowed=False,
            reason=f"Tool '{tool_name}' is not allowed by the current policy.",
        )

    return EnforcementResult(allowed=True, reason=f"Tool '{tool_name}' approved.")
