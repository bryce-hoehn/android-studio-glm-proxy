import uvicorn
from fastapi import FastAPI
from app.routes.chat import router as chat_router
from app.routes.models import router as model_router
from app.config import settings

app = FastAPI()

app.include_router(chat_router)
app.include_router(model_router)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
