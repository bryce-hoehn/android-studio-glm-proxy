import uvicorn
from fastapi import FastAPI
from app.routes.chat import router as chat_router
from app.routes.mcp import router as mcp_router, register_mcp_routes
from app.routes.models import router as model_router
from app.config import settings

app = FastAPI()

app.include_router(chat_router)
app.include_router(mcp_router)
app.include_router(model_router)

# Register dynamic MCP routes from configuration
register_mcp_routes(app)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
