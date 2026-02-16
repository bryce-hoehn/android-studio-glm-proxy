import asyncio
import json
from collections.abc import AsyncGenerator

from fastapi import APIRouter, FastAPI
from fastapi.responses import StreamingResponse

from app.config import settings
from app.types import McpServerConfig, McpSettings

router = APIRouter(prefix="/mcp", tags=["mcp"])


def load_mcp_servers() -> dict[str, McpServerConfig]:
    """Load MCP server configurations from JSON file."""
    try:
        with open(settings.MCP_SETTINGS_PATH, "r") as file:
            data = json.load(file)
        return McpSettings(**data).mcpServers
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


async def stream_subprocess(
    command: str, args: str | list[str]
) -> AsyncGenerator[str, None]:
    """Stream subprocess output line by line."""
    args_list = [args] if isinstance(args, str) else list(args)
    process = await asyncio.create_subprocess_exec(
        command,
        *args_list,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    if process.stdout is None:
        raise RuntimeError("Failed to create subprocess stdout pipe")

    try:
        async for line in process.stdout:
            yield line.decode("utf-8", errors="replace")
    finally:
        await process.wait()


def register_mcp_routes(app: FastAPI):
    """Register MCP server routes from configuration file."""
    for server_name, config in load_mcp_servers().items():
        # Capture config values in closure using default arguments
        async def handler(
            cmd: str = config.command,
            args: str | list[str] = config.args,
        ) -> StreamingResponse:
            return StreamingResponse(
                stream_subprocess(cmd, args),
                media_type="text/plain",
            )

        app.get(f"/mcp/{server_name}")(handler)
