from typing import Any, Dict

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., description="User message to the assistant")
    user_id: str = Field("", description="Optional user id; empty for anonymous")


class ChatResponse(BaseModel):
    reply: str
    conversation_id: str = ""
    conversation_message_id: str = ""
    user_id: str = ""
    timestamp: str = ""  # ISO 8601
    role: str = "assistant"  # 'assistant' | 'user' | 'system'
    model: str = ""
    tokens_used: int = 0
    metadata: Dict[str, Any] = Field(default_factory=dict)
    error: str = ""
