import json
import os
import datetime
from pathlib import Path

class AuditLogger:
    def __init__(self, log_dir="logs", filename="audit.jsonl"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / filename
        
    def _log_event(self, phase: str, payload: dict):
        event = {
            "timestamp": datetime.datetime.now().isoformat(),
            "phase": phase,
            "payload": payload
        }
        with open(self.log_file, "a") as f:
            f.write(json.dumps(event) + "\n")
            
    def log_orchestration(self, plan: dict, policy: dict):
        self._log_event("orchestrator", {"plan": plan, "policy": policy})
        
    def log_approval(self, decision: dict):
        self._log_event("approver", {"decision": decision})
        
    def log_execution(self, executor_output: dict):
        self._log_event("executor", {"executor_output": executor_output})
        
    def log_enforcement(self, is_allowed: bool, reason: str = ""):
        self._log_event("enforcer", {"is_allowed": is_allowed, "reason": reason})
        
    def log_environment(self, output: str):
        self._log_event("environment", {"output": output})
