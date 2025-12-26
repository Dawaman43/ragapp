from uuid import uuid4
from datetime import datetime

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.llm import chat_with_model


router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
	if not request.message or not request.message.strip():
		raise HTTPException(status_code=400, detail="message is required")

	# Build the messages payload for the LLM. Keep it simple for now.
	messages = [
		{"role": "system", "content": "You are a helpful assistant."},
		{"role": "user", "content": request.message},
	]

	# Call the model service
	try:
		reply_text = await chat_with_model(messages)
	except Exception as e:
		raise HTTPException(status_code=502, detail=f"LLM error: {e}")

	now = datetime.utcnow().isoformat() + "Z"
	conv_id = str(uuid4())
	msg_id = str(uuid4())

	resp = ChatResponse(
		reply=reply_text,
		conversation_id=conv_id,
		conversation_message_id=msg_id,
		user_id=request.user_id or "",
		timestamp=now,
		role="assistant",
		model="gemini-1.5-flash",
		tokens_used=0,
		metadata={},
		error="",
	)

	return resp


@router.get("/chat/health")
async def chat_health():
	return {"ok": True, "message": "Chat API is healthy."}


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
	"""Simple streaming wrapper: calls the same model and yields the full reply once.

	This avoids using undefined variables and provides a streaming-compatible
	response shape for clients that expect SSE/chunked output.
	"""

	if not request.message or not request.message.strip():
		raise HTTPException(status_code=400, detail="message is required")

	messages = [
		{"role": "system", "content": "You are a helpful assistant."},
		{"role": "user", "content": request.message},
	]

	async def event_stream():
		try:
			text = await chat_with_model(messages)
		except Exception as e:
			yield f"event: error\ndata: LLM error: {e}\n\n"
			return
		# Yield the full reply as a single data event
		yield f"data: {text}\n\n"

	return StreamingResponse(event_stream(), media_type="text/event-stream")