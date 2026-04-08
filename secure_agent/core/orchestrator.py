"""
Orchestrator — generates a dynamic Plan + Policy for a given task.

Implements Design Space 1 (replanning) from the paper.
"""

from __future__ import annotations

from secure_agent.core.models import PlanAndPolicy

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from secure_agent.protocols import LLMProvider

_SYSTEM_PROMPT = """\
You are the Orchestrator. Your job is to create a dynamic Plan and Policy to accomplish the user task.
Follow the Principle of Least Privilege: The policy should only allow actions necessary for the current plan.
Provide clear steps.
"""


def generate_plan_and_policy(
    llm: LLMProvider,
    task: str,
    context: str = "",
    current_plan: str = "",
    feedback: str = "",
) -> PlanAndPolicy:
    """Build or refine a :class:`PlanAndPolicy` using the supplied *llm*."""
    prompt = f"Task: {task}\nContext: {context}\n"
    if current_plan:
        prompt += f"Current Plan:\n{current_plan}\n"
    if feedback:
        prompt += f"Recent Feedback / Execution Results:\n{feedback}\n"

    prompt += "\nPlease propose the optimal execution Plan and Security Policy."

    return llm.generate_structured(prompt, PlanAndPolicy, _SYSTEM_PROMPT)
