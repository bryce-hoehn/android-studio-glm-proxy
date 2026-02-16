from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Union


class ContentItem(BaseModel):
    text: str
    type: str


class Message(BaseModel):
    role: str
    content: Union[str, List[ContentItem], None] = None
    tool_calls: Optional[List[dict]] = None
    tool_call_id: Optional[str] = None
    name: Optional[str] = None


class Tool(BaseModel):
    type: str
    function: dict


class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[Message]
    temperature: Optional[float] = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = None
    stream: Optional[bool] = False
    tools: Optional[List[Tool]] = None
    tool_choice: Optional[Union[str, dict]] = None


class McpServerConfig(BaseModel):
    """Configuration for a single MCP server."""

    command: str
    args: List[str] | str
    env: Optional[Dict[str, str]] = None
    alwaysAllow: Optional[List[str]] = None


class McpSettings(BaseModel):
    """MCP settings configuration loaded from mcp_settings.json."""

    mcpServers: Dict[str, McpServerConfig]
