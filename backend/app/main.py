from os import getenv
from fastapi import FastAPI

app = FastAPI()

# Read Gemini key from environment; do NOT expose it in responses.
GEMINI_API_KEY = getenv("GEMINI_API_KEY")


@app.get("/health")
async def health():
	"""Basic health endpoint. Returns if Gemini API key is configured (boolean).

	This avoids returning the value of the key.
	"""
	return {"ok": True, "gemini_configured": bool(GEMINI_API_KEY)}


if __name__ == "__main__":
	# Simple local runner for convenience (not used in production Docker image).
	import uvicorn

	uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
from fastapi import FastAPI 
