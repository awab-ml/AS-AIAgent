"""Backward-compatible re-export from the original ``secure_agent.security.audit_logger`` location."""

from secure_agent.defaults.logger_jsonl import JSONLEventLogger


class AuditLogger(JSONLEventLogger):
    """Legacy shim mapping old method names to the new EventLogger protocol."""

    def log_orchestration(self, plan: dict, policy: dict):
        self.on_orchestration(plan, policy)

    def log_approval(self, decision: dict):
        self.on_approval(decision)

    def log_execution(self, executor_output: dict):
        self.on_execution(executor_output)

    def log_enforcement(self, is_allowed: bool, reason: str = ""):
        self.on_enforcement(is_allowed, reason)

    def log_environment(self, output: str):
        self.on_environment(output)
