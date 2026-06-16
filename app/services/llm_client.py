"""MiniMax LLM client using OpenAI-compatible endpoint."""

import httpx

from app.config import config

CHAT_ENDPOINT = f"{config.API_BASE_URL}/text/chatcompletion_v2"


async def chat_completion(
    messages: list[dict[str, str]],
    temperature: float = 0.3,
    max_tokens: int = 2048,
) -> str:
    """
    Call MiniMax via OpenAI-compatible Chat Completions API.

    Endpoint: POST /v1/chat/completions
    Docs: https://platform.minimax.chat
    """
    async with httpx.AsyncClient(timeout=httpx.Timeout(60.0)) as client:
        response = await client.post(
            CHAT_ENDPOINT,
            headers={
                "Authorization": f"Bearer {config.API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": config.MODEL_NAME,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
            },
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
