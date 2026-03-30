# app/api/routers/health.py

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def health_check():
    return {
        "status": "ok",
        "message": "System is running 🚀"
    }