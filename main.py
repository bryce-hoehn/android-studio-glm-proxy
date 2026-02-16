import json
import os
from fastapi.responses import StreamingResponse
import requests
import uvicorn
from fastapi import FastAPI, Request, Response
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List, Optional, Union

load_dotenv()

app = FastAPI()

API_KEY = os.getenv("API_KEY")

BASE_URL = "https://api.z.ai/api/coding/paas/v4"

headers = {
    "Content-Type": "application/json",
    "Accept-Language": "en-US,en",
    "Authorization": f"Bearer {API_KEY}",
}


class ContentItem(BaseModel):
    text: str
    type: str


class Message(BaseModel):
    role: str
    content: Union[str, List[ContentItem]]


class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[Message]
    temperature: Optional[float] = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = None
    stream: Optional[bool] = False


def get_proxy_headers(request_headers):
    """Filter out host header from request headers for proxying."""
    return {k: v for k, v in request_headers.items() if k.lower() != "host"}


@app.post("/chat/completions")
async def chat_completion(request: Request):
    json_payload = await request.json()
    validated = ChatCompletionRequest(**json_payload)

    for msg in validated.messages:
        if msg.role == "developer":
            msg.role = "system"

    response = requests.post(
        f"{BASE_URL}/chat/completions",
        headers=get_proxy_headers(request.headers),
        json=validated.model_dump(),
        stream=True,
    )

    def generate():
        for chunk in response.iter_lines():
            if chunk:
                yield chunk.decode() + "\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"},
    )


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_request(request: Request, path: str):
    body = await request.body()

    response = requests.request(
        method=request.method,
        url=f"{BASE_URL}/{path}",
        headers=get_proxy_headers(request.headers),
        data=body if body else None,
        params=request.query_params,
    )

    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers),
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
