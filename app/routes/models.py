from fastapi import APIRouter
import requests

from app.config import settings

router = APIRouter()


@router.get("/models")
def models():
    response = requests.get(f"{settings.BASE_URL}/models", headers=settings.HEADERS)
    return response.json()
