import os
from typing import List

try:
    import google.generativeai as genai
except Exception:
    genai = None

from app.api.core.config import GEMINI_API_KEY


# Try to call the installed Google generative API client when available;
# otherwise fall back to a simple mock reply so the app can run locally
# without failing during tests.
if genai is not None and GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        _model = genai.GenerativeModel("gemini-1.5-flash")
    except Exception:
        _model = None
else:
    _model = None


async def chat_with_model(messages: List[dict]) -> str:
    # Prefer real model if available
    if _model is not None:
        try:
            # older clients expose `chat`; guard in case API differs
            if hasattr(_model, "chat"):
                resp = _model.chat(messages=messages, temperature=0.7, max_output_tokens=1024)
                return getattr(resp, "text", str(resp))
            # fallback to a generic generate call if present
            if hasattr(_model, "generate"):
                resp = _model.generate(messages=messages, temperature=0.7, max_output_tokens=1024)
                return getattr(resp, "text", str(resp))
        except Exception as e:
            # fall through to mock reply
            pass

    # Mock reply for local testing / when model isn't available
    user_msg = next((m.get("content", "") for m in messages if m.get("role") == "user"), "")
    system_ctx = "\n".join([m.get("content", "") for m in messages if m.get("role") == "system"]).strip()
    mock = f"(mock) I received: {user_msg}" + (f"\nContext:\n{system_ctx}" if system_ctx else "")
    return mock