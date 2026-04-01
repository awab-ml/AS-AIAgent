from secure_agent.core.models import PlanAndPolicy
from secure_agent.llm.client import generate_structured
import json

def generate_plan_and_policy(task: str, context: str = "", current_plan: str = "", feedback: str = "") -> PlanAndPolicy:
    """
    Generates an initial or updated plan and policy.
    Implements Design Space 1 (replanning) from the paper.
    """
    sys_prompt = """
You are the Orchestrator. Your job is to create a dynamic Plan and Policy to accomplish the user task.
Follow the Principle of Least Privilege: The policy should only allow actions necessary for the current plan.
Provide clear steps.
"""
    prompt = f"Task: {task}\nContext: {context}\n"
    if current_plan:
        prompt += f"Current Plan:\n{current_plan}\n"
    if feedback:
        prompt += f"Recent Feedback / Execution Results:\n{feedback}\n"
        
    prompt += "\nPlease propose the optimal execution Plan and Security Policy."
    
    return generate_structured(prompt, PlanAndPolicy, sys_prompt)
