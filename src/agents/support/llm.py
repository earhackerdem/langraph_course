import os
from typing import Literal

from langchain.chat_models import init_chat_model
from langchain_core.language_models.chat_models import BaseChatModel

Tier = Literal["full", "mini"]


def is_ollama_backend() -> bool:
    return os.getenv("LLM_BACKEND", "openai").strip().lower() == "ollama"


def _openai_model_id(tier: Tier) -> str:
    if tier == "mini":
        return os.getenv("OPENAI_MINI_MODEL", "gpt-4o-mini").strip()
    return os.getenv("OPENAI_CHAT_MODEL", "gpt-4o").strip()


def _ollama_model_id(tier: Tier) -> str:
    if tier == "mini":
        return (
            os.getenv("OLLAMA_MINI_MODEL", "").strip()
            or os.getenv("OLLAMA_MODEL", "llama3.1").strip()
        )
    return os.getenv("OLLAMA_MODEL", "llama3.1").strip()


def get_chat_model(*, temperature: float = 0, tier: Tier = "full") -> BaseChatModel:
    if is_ollama_backend():
        return init_chat_model(
            _ollama_model_id(tier),
            model_provider="ollama",
            temperature=temperature,
            base_url=os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434"),
        )
    return init_chat_model(
        f"openai:{_openai_model_id(tier)}",
        temperature=temperature,
    )
