from fastapi import Request
from fastapi.responses import StreamingResponse
from fastapi import APIRouter

import requests

from app.config import settings
from app.types import ChatCompletionRequest

router = APIRouter()


@router.post("/chat/completions")
async def chat_completion(request: Request):
    json_payload = await request.json()
    validated = ChatCompletionRequest(**json_payload)

    for msg in validated.messages:
        if msg.role == "developer":
            msg.role = "system"

    # Prepare payload, excluding None values to match OpenAI API behavior
    payload = validated.model_dump(exclude_none=True)

    response = requests.post(
        f"{settings.BASE_URL}/chat/completions",
        headers=settings.HEADERS,
        json=payload,
        stream=True,
        timeout=settings.TIMEOUT,
    )

    def generate():
        for chunk in response.iter_lines():
            if chunk:
                decoded_chunk = chunk.decode()
                # Pass through the chunk as-is - the upstream API should handle tool_calls
                yield decoded_chunk + "\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"},
    )
