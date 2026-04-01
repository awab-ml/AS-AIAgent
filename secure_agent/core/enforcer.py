from secure_agent.core.models import Policy, ExecutorOutput
from rich.console import Console
from rich.panel import Panel

console = Console()

class PolicyViolation(Exception):
    pass

def enforce_policy(policy: Policy, proposed: ExecutorOutput) -> bool:
    """
    Blocks tool calls that violate the Plan's dynamically generated Policy.
    Also serves as the checkpoint to enforce 'trusted vs untrusted' provenance constraints (Proposal 1, Step 2).
    """
    if not proposed.tool_call:
        return True # Nothing to enforce
        
    tool_name = proposed.tool_call.tool_name
    
    # 1. Enforce Mode 1 from the paper (No external instructions allowed directly for critical loops)
    for inst in proposed.verbalized_instructions:
        source_lower = inst.source_hypothesis.lower()
        if "environment" in source_lower or "untrusted" in source_lower or "web" in source_lower or "email" in source_lower:
             console.print(Panel(f"[bold red]Policy Violation: Execution blocked!\nDetected untrusted provenance in intended instructions:\n'{inst.instruction_text}'[/bold red]", title="Enforcer"))
             return False

    # 2. Check rule-based policy matches
    allowed = False
    for rule in policy.rules:
        # A simple engine: match on tool name. Real system uses Cedar or equivalent.
        if rule.action == tool_name or rule.action == "*":
            if rule.effect == "allow":
                allowed = True
            elif rule.effect == "deny":
                allowed = False # Deny overrides

    if not allowed:
        console.print(f"[bold red]Policy Violation: Tool '{tool_name}' is not allowed by the current policy.[/bold red]")
        return False

    console.print(f"[bold green]Enforcer approved execution of {tool_name}[/bold green]")
    return True
