"""
Policy Enforcer — blocks tool calls that violate the dynamic policy or
originate from untrusted instruction sources.

Also serves as the checkpoint for Proposal 1, Step 2: trusted-vs-untrusted
provenance constraints.

When a :class:`GlobalRules` config is provided, provenance keywords and tool
deny-lists are driven entirely by the external JSON configuration file.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from secure_agent.core.models import ExecutorOutput, Policy
from secure_agent.security.rule_parser import GlobalRules


class PolicyViolation(Exception):
    """Raised when an action violates the active security policy."""


@dataclass(frozen=True)
class EnforcementResult:
    """Structured outcome from :func:`enforce_policy`."""
    allowed: bool
    reason: str = ""


def enforce_policy(
    policy: Policy,
    proposed: ExecutorOutput,
    global_rules: Optional[GlobalRules] = None,
) -> EnforcementResult:
    """Evaluate *proposed* against *policy* and return an :class:`EnforcementResult`.

    The function is **pure** — no Rich output, no side-effects.

    When *global_rules* is supplied the provenance keywords and tool deny-lists
    come from the external ``global_rules.json`` config.  Otherwise the legacy
    hardcoded keywords are used for backward compatibility.
    """
    if not proposed.tool_call:
        return EnforcementResult(allowed=True, reason="No tool call to enforce.")

    tool_name = proposed.tool_call.tool_name

    # --- Config-driven checks (loaded from global_rules.json) ---
    if global_rules:
        # 0. Unconditionally blocked tools
        if tool_name in global_rules.always_deny_tools:
            return EnforcementResult(
                allowed=False,
                reason=f"Tool '{tool_name}' is permanently blocked by global rules.",
            )

        # 1. Provenance check using configurable keywords
        provenance_keywords = [kw.lower() for kw in global_rules.untrusted_provenance_keywords]
        for inst in proposed.verbalized_instructions:
            source_lower = inst.source_hypothesis.lower()
            if any(kw in source_lower for kw in provenance_keywords):
                # Only block if the tool is in the deny-for-untrusted list
                if tool_name in global_rules.global_deny_tools_for_untrusted:
                    return EnforcementResult(
                        allowed=False,
                        reason=(
                            f"Untrusted provenance detected in intended instruction: "
                            f"'{inst.instruction_text}' (source: {inst.source_hypothesis}). "
                            f"Tool '{tool_name}' is denied for untrusted sources."
                        ),
                    )
    else:
        # Legacy fallback: hardcoded provenance keywords (kept for backward compatibility)
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
