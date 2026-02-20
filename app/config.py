import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    BASE_URL: str = "https://api.z.ai/api/coding/paas/v4"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    TIMEOUT: int = 60
    HEADERS = {
        "Content-Type": "application/json",
        "Accept-Language": "en-US,en",
        "Authorization": f"Bearer {os.getenv('API_KEY')}",
    }


settings = Settings()
