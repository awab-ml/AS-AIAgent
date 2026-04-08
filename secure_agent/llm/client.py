"""Backward-compatible re-exports from the original ``secure_agent.llm.client`` location."""

from secure_agent.defaults.llm_mock import MockLLMProvider as _Mock
from secure_agent.defaults.llm_openai import OpenAILLMProvider as _OpenAI

# Provide the old functional API as a thin shim so existing code doesn't break.
_default_provider: _Mock | _OpenAI | None = None


def _get_provider() -> _Mock | _OpenAI:
    global _default_provider
    if _default_provider is None:
        import os
        from dotenv import load_dotenv

        load_dotenv()
        use_mock = os.getenv("USE_MOCK_LLM", "false").lower() == "true"
        has_key = bool(os.getenv("OPENAI_API_KEY"))

        if has_key and not use_mock:
            _default_provider = _OpenAI()
        else:
            _default_provider = _Mock()
    return _default_provider


def generate_structured(prompt, response_model, system_prompt="You are a helpful AI."):
    """Legacy shim — delegates to the default LLMProvider."""
    return _get_provider().generate_structured(prompt, response_model, system_prompt)


def generate_text(prompt, system_prompt="You are a helpful AI."):
    """Legacy shim — delegates to the default LLMProvider."""
    return _get_provider().generate_text(prompt, system_prompt)
