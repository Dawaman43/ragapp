import google.generativeai as genai
from app.api.core.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

async def chat_with_model(messages: list[dict]) -> str:
    response = model.chat(
        messages=messages,
        temperature=0.7,
        max_output_tokens=1024,
    )
    return response.text