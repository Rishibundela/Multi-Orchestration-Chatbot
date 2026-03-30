# app/main.py

from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.router import api_router
from app.core.config import settings


# -----------------------------
# Lifespan (startup/shutdown)
# -----------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🔹 Startup tasks
    print(f"🚀 Starting {settings.APP_NAME} ({settings.ENV})")

    # Example future use:
    # - connect Redis
    # - load models
    # - init tools
    # - warm caches

    yield

    # 🔹 Shutdown tasks
    print("🛑 Shutting down application...")


# -----------------------------
# FastAPI App
# -----------------------------
app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Intelligent Multi-Agent Orchestration Engine",
    lifespan=lifespan,
)


# -----------------------------
# Register Routers
# -----------------------------
app.include_router(api_router, prefix="/api/v1")


# -----------------------------
# Root Endpoint
# -----------------------------
@app.get("/")
async def root():
    return {
        "message": f"{settings.APP_NAME} is running 🚀",
        "environment": settings.ENV
    }


# -----------------------------
# Health Check
# -----------------------------
@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }