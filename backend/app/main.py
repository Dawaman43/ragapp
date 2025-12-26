from os import getenv
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import logging
import traceback
import os

from app.api.chat import router as chat_router
from app.api.admin import router as admin_router


app = FastAPI()

# Read Gemini key from environment; do NOT expose it in responses.
GEMINI_API_KEY = getenv("GEMINI_API_KEY")


@app.get("/health")
async def health():
	"""Basic health endpoint. Returns if Gemini API key is configured (boolean).

	This avoids returning the value of the key.
	"""
	return {"ok": True, "gemini_configured": bool(GEMINI_API_KEY)}


app.include_router(chat_router, prefix="/api")
app.include_router(admin_router, prefix="/api")

# Ensure logs dir
os.makedirs("./logs", exist_ok=True)
logging.basicConfig(filename="./logs/error.log", level=logging.ERROR)


@app.exception_handler(Exception)
async def all_exception_handler(request, exc):
	tb = traceback.format_exc()
	logging.error(tb)
	return JSONResponse(status_code=500, content={"detail": "Internal Server Error", "error": str(exc)})


if __name__ == "__main__":
	# Simple local runner for convenience (not used in production Docker image).
	import uvicorn

	uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
