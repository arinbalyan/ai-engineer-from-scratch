import json
import os
import pathlib


_SECRETS_PATH = pathlib.Path.home() / ".config" / "ai-eng" / "secrets.json"
_cache: dict | None = None


def _load() -> dict:
    global _cache
    if _cache is None:
        _cache = json.loads(_SECRETS_PATH.read_text())
    assert _cache is not None
    return _cache


def get_key(name: str) -> str:
    """Return a secret from ~/.config/ai-eng/secrets.json."""
    return _load()[name]


def get_openai_key() -> str:
    return get_key("openai")


def get_anthropic_key() -> str:
    return get_key("anthropic")


def get_huggingface_key() -> str:
    return get_key("huggingface")


def get_openrouter_key() -> str:
    return get_key("openrouter")


def get_default_model() -> str:
    return get_key("default_model")
