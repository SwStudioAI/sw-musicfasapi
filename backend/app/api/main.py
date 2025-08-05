from fastapi import APIRouter

from app.api.routes import items, login, private, users, utils, vertex_ai, google_ai
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)
api_router.include_router(items.router)
api_router.include_router(vertex_ai.router, prefix="/ai", tags=["AI/Vertex"])
api_router.include_router(google_ai.router, prefix="/google-ai", tags=["Google Cloud AI"])


if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)
