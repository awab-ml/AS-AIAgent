"""
OpenAI LLM provider — uses the OpenAI Python SDK with Pydantic structured outputs.
"""

from __future__ import annotations

import os
from typing import Type, TypeVar

from pydantic import BaseModel


T = TypeVar("T", bound=BaseModel)


class OpenAILLMProvider:
    """An :class:`~secure_agent.protocols.LLMProvider` backed by the OpenAI API.

    Parameters
    ----------
    api_key:
        OpenAI API key. Falls back to the ``OPENAI_API_KEY`` env var.
    model:
        Model identifier. Falls back to ``OPENAI_MODEL`` env var or ``gpt-4o-mini``.
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
    ) -> None:
        from openai import OpenAI # deferred so the dep is optional at import time

        resolved_key = api_key or os.getenv("OPENAI_API_KEY", "")
        if not resolved_key:
            raise ValueError(
                "An OpenAI API key is required. Pass it explicitly or set OPENAI_API_KEY."
            )
        self._client = OpenAI(api_key=resolved_key)
        self._model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def generate_structured(
        self,
        prompt: str,
        response_model: Type[T],
        system_prompt: str = "You are a helpful AI.",
    ) -> T:
        completion = self._client.beta.chat.completions.parse(
            model=self._model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            response_format=response_model,
        )
        return completion.choices[0].message.parsed  # type: ignore[return-value]

    def generate_text(
        self,
        prompt: str,
        system_prompt: str = "You are a helpful AI.",
    ) -> str:
        completion = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
        )
        return completion.choices[0].message.content or ""
