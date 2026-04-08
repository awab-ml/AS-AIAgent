"""
JSONL event logger — writes structured audit events to a ``.jsonl`` file.

This is the default :class:`~secure_agent.protocols.EventLogger` implementation.
"""

from __future__ import annotations

import datetime
import json
from pathlib import Path


class JSONLEventLogger:
    """Append-only JSONL logger satisfying the :class:`~secure_agent.protocols.EventLogger` protocol.

    Parameters
    ----------
    log_dir:
        Directory to create the log file in (created automatically).
    filename:
        Name of the JSONL file.
    """

    def __init__(self, log_dir: str = "logs", filename: str = "audit.jsonl") -> None:
        self._log_dir = Path(log_dir)
        self._log_dir.mkdir(parents=True, exist_ok=True)
        self._log_file = self._log_dir / filename

    # -- internal -----------------------------------------------------------

    def _write(self, phase: str, payload: dict) -> None:
        event = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "phase": phase,
            "payload": payload,
        }
        with open(self._log_file, "a") as fh:
            fh.write(json.dumps(event) + "\n")

    # -- EventLogger protocol -----------------------------------------------

    def on_orchestration(self, plan: dict, policy: dict) -> None:
        self._write("orchestrator", {"plan": plan, "policy": policy})

    def on_approval(self, decision: dict) -> None:
        self._write("approver", {"decision": decision})

    def on_execution(self, executor_output: dict) -> None:
        self._write("executor", {"executor_output": executor_output})

    def on_enforcement(self, is_allowed: bool, reason: str = "") -> None:
        self._write("enforcer", {"is_allowed": is_allowed, "reason": reason})

    def on_environment(self, output: str) -> None:
        self._write("environment", {"output": output})
