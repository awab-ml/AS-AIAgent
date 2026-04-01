from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class Step(BaseModel):
    id: str = Field(description="Unique identifier for the step (e.g., 'step_1')")
    description: str = Field(description="Natural language description of what to do")
    tool_name: Optional[str] = Field(None, description="The tool to use, if any")

class PolicyRule(BaseModel):
    effect: str = Field(description="'allow' or 'deny'")
    action: str = Field(description="The action or tool name (e.g., 'read_email', '*')")
    resource: Optional[str] = Field(None, description="The resource or domains allowed (e.g., '*.internal.com')")
    condition: Optional[str] = Field(None, description="Specific conditions or constraints")

class Plan(BaseModel):
    steps: List[Step] = Field(description="List of execution steps to complete the task")

class Policy(BaseModel):
    rules: List[PolicyRule] = Field(description="List of access control rules for the plan")

class PlanAndPolicy(BaseModel):
    plan: Plan = Field(description="The proposed plan")
    policy: Policy = Field(description="The security policy necessary to complete the plan")

class ToolCall(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]

class IntendedInstruction(BaseModel):
    instruction_text: str = Field(description="The exact text of the instruction recognized")
    source_hypothesis: str = Field(description="Where the instruction came from in the context (user, environment, internal thought)")

class ExecutorOutput(BaseModel):
    verbalized_instructions: List[IntendedInstruction] = Field(description="List of instructions the model intends to follow (Proposal 1)")
    tool_call: Optional[ToolCall] = Field(None, description="The concrete tool call to execute, if any")

class ApproverDecision(BaseModel):
    approved: bool = Field(description="Whether the proposed plan/policy changes are benign and approved.")
    reason: str = Field(description="Reasoning behind the decision.")
