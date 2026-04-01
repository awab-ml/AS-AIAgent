import os
from openai import OpenAI
from pydantic import BaseModel
from typing import Type, TypeVar
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "mock-key"))

T = TypeVar('T', bound=BaseModel)

def generate_structured(prompt: str, response_model: Type[T], system_prompt: str = "You are a helpful AI.") -> T:
    """Generates a structured response strictly parsing to the given Pydantic schema."""
    try:
        response = client.beta.chat.completions.parse(
            model="gpt-4o-mini", # Default to smaller model for demo/speed; can be gpt-4o.
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            response_format=response_model
        )
        parsed = response.choices[0].message.parsed
        if parsed is None:
            raise ValueError("Failed to parse structured output from model")
        return parsed
    except Exception as e:
        print(f"Error calling LLM: {e}")
        raise e

def generate_text(prompt: str, system_prompt: str = "You are a helpful AI.") -> str:
    """Generates pure text output."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content or ""
