"""Central configuration for the SEO Premium Agent.

Backward-compatible configuration:
- Existing app.py can continue importing DEFAULT_MODEL and SUPPORTED_MODELS.
- New code can use DEFAULT_GROQ_MODEL and SUPPORTED_GROQ_MODELS.
- Exact Groq model IDs are preserved, including the required openai/ prefix.
"""

from __future__ import annotations

GROQ_BASE_URL = "https://api.groq.com/openai/v1"

SUPPORTED_GROQ_MODELS = (
    "openai/gpt-oss-20b",
    "openai/gpt-oss-120b",
)

DEFAULT_GROQ_MODEL = "openai/gpt-oss-20b"

# Backward-compatible names used by the existing app.py.
SUPPORTED_MODELS = SUPPORTED_GROQ_MODELS
DEFAULT_MODEL = DEFAULT_GROQ_MODEL


def normalize_groq_model(model: str | None) -> str:
    """Convert legacy/short model names to an exact Groq model ID."""
    value = (model or DEFAULT_GROQ_MODEL).strip()

    if value.startswith("custom_openai/"):
        value = value[len("custom_openai/"):]
    if value.startswith("groq/"):
        value = value[len("groq/"):]

    aliases = {
        "gpt-oss-20b": "openai/gpt-oss-20b",
        "gpt-oss-120b": "openai/gpt-oss-120b",
        "openai/gpt-oss-20b": "openai/gpt-oss-20b",
        "openai/gpt-oss-120b": "openai/gpt-oss-120b",
    }
    normalized = aliases.get(value, value)

    if normalized not in SUPPORTED_GROQ_MODELS:
        raise ValueError(
            f"Unsupported Groq model '{model}'. "
            f"Choose one of: {', '.join(SUPPORTED_GROQ_MODELS)}"
        )

    return normalized
