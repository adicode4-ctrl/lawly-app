import sys
import os
from dotenv import load_dotenv
load_dotenv()
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
print("--- BOOTING BACKEND SERVER ---")
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from app.services.ai_service import AIService
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows testing from any frontend port for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ai_service = AIService()

@app.get("/api/v1/chat/stream")
async def chat_stream(
    prompt: str = Query(..., description="The message payload for the AI assistant"),
    provider: str = Query("openai", description="Choose 'openai' or 'anthropic'"),
    model: str = Query("gpt-4o", description="Target model variant name")
):
    return StreamingResponse(
        ai_service.stream_legal_response(prompt=prompt, provider=provider, model=model),
        media_type="text/event-stream"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)