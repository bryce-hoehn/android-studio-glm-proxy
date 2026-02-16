import json
import os
from fastapi.responses import StreamingResponse
import requests
import uvicorn
from fastapi import FastAPI, Request
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


@app.get("/models")
def models():
    response = requests.get(f"{BASE_URL}/models", headers=headers)
    return response.json()


@app.post("/chat/completions")
async def chat_completion(request: Request):
    json_payload = await request.json()
    validated = ChatCompletionRequest(**json_payload)

    for msg in validated.messages:
        if msg.role == "developer":
            msg.role = "system"

    response = requests.post(
        f"{BASE_URL}/chat/completions",
        headers=headers,
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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
