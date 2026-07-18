import json
import os
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
from dotenv import load_dotenv
from app.core.config import settings


class AIService:
    def __init__(self):
        load_dotenv()

        self.api_key_val = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY") or ""

        if self.api_key_val.startswith("nvapi"):
            self.openai_client = AsyncOpenAI(
                api_key=self.api_key_val,
                base_url="https://integrate.api.nvidia.com/v1",
                default_headers={
                    "HTTP-Referer": "http://localhost:3000",
                    "X-Title": "Lawly App",
                },
            )
        elif self.api_key_val:
            self.openai_client = AsyncOpenAI(api_key=self.api_key_val)
        else:
            self.openai_client = None

        self.anthropic_client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY) if settings.ANTHROPIC_API_KEY else None

    async def stream_legal_response(self, prompt: str, provider: str = "openai", model: str = "gpt-4o"):
        system_instruction = (
            "You are Lawly, a helpful AI legal assistant. Provide concise guidance. "
            "You are an AI, not a licensed attorney. Never claim to establish an attorney-client relationship, "
            "and encourage consulting a qualified legal professional for legal advice."
        )

        provider_name = (provider or "openai").lower()
        effective_model = model if model and model != "gpt-4o" else "meta/llama-3.1-8b-instruct"

        if provider_name == "openai":
            if not self.openai_client:
                yield f"data: {json.dumps({'error': 'No OpenAI-compatible API key configured'})}\n\n"
                return

            try:
                response = await self.openai_client.chat.completions.create(
                    model=effective_model,
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": prompt},
                    ],
                    stream=True,
                    max_tokens=400,
                )

                async for chunk in response:
                    delta = getattr(chunk.choices[0], "delta", None)
                    content = getattr(delta, "content", None)
                    if content:
                        if isinstance(content, list):
                            content = "".join(part.text if hasattr(part, "text") else str(part) for part in content)
                        elif not isinstance(content, str):
                            content = str(content)
                        if content:
                            yield f"data: {json.dumps({'content': content})}\n\n"
            except Exception as exc:
                print(f"\n--- NVIDIA ERROR ---\n{exc}\n--------------------\n")
                yield f"data: {json.dumps({'error': str(exc)})}\n\n"

        elif provider_name == "anthropic":
            if not self.anthropic_client:
                yield f"data: {json.dumps({'error': 'No Anthropic API key configured'})}\n\n"
                return

            try:
                async with self.anthropic_client.messages.stream(
                    model=effective_model,
                    max_tokens=4000,
                    system=system_instruction,
                    messages=[{"role": "user", "content": prompt}],
                ) as stream:
                    async for text in stream.text_stream:
                        yield f"data: {json.dumps({'content': text})}\n\n"
            except Exception as exc:
                print(f"\n--- ANTHROPIC ERROR ---\n{exc}\n--------------------\n")
                yield f"data: {json.dumps({'error': str(exc)})}\n\n"
        else:
            yield f"data: {json.dumps({'error': 'Unsupported provider'})}\n\n"