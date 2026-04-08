"""Backward-compatible re-exports from the original ``secure_agent.env.tools`` location."""

from secure_agent.defaults.tools_mock import MockToolExecutor

_executor = MockToolExecutor()

# Legacy functional API
def execute_tool(tool_name, args):
    """Legacy shim — delegates to the default MockToolExecutor."""
    return _executor.execute(tool_name, args)

tools_registry = {name: None for name in _executor.list_tools()}
