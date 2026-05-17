# app/api/router.py

from fastapi import APIRouter

# Import individual routers
from app.api.routers import chat, rag, session, health

# -----------------------------
# Main API Router
# -----------------------------
api_router = APIRouter()

# -----------------------------
# Register Sub-Routers
# -----------------------------

# Chat routes
api_router.include_router(
    chat.router,
    prefix="/chat",
    tags=["Chat"]
)

# RAG routes (ingestion only)
api_router.include_router(
    rag.router,
    prefix="/rag",
    tags=["RAG"]
)

# Session routes
api_router.include_router(
    session.router,
    prefix="/session",
    tags=["Session"]
)

# Health routes
api_router.include_router(
    health.router,
    prefix="/health",
    tags=["Health"]
)