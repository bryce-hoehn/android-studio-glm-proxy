import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    BASE_URL: str = "https://api.z.ai/api/coding/paas/v4"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    TIMEOUT: int = 60
    MCP_SETTINGS_PATH: str = os.getenv(
        "MCP_SETTINGS_PATH", "/app/config/mcp_settings.json"
    )
    HEADERS = {
        "Content-Type": "application/json",
        "Accept-Language": "en-US,en",
        "Authorization": f"Bearer {os.getenv('API_KEY')}",
    }


settings = Settings()
