# app/api/routers/session.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.db.repository import ChatRepository
from app.services.session_service import SessionService


router = APIRouter()


# -----------------------------
# Dependency
# -----------------------------
def get_session_service(db: AsyncSession = Depends(get_db)):
    chat_repo = ChatRepository(db)
    return SessionService(chat_repo)


# -----------------------------
# Create Chat Session
# -----------------------------
@router.post("/create")
async def create_session(
    session_service: SessionService = Depends(get_session_service)
):
    chat = await session_service.create_session()
    return {"chat_id": chat.id}


# -----------------------------
# Get Chat Session
# -----------------------------
@router.get("/{chat_id}")
async def get_session(
    chat_id: int,
    session_service: SessionService = Depends(get_session_service)
):
    chat = await session_service.get_session(chat_id)
    return {"chat": chat}


# -----------------------------
# Delete Chat Session
# -----------------------------
@router.delete("/{chat_id}")
async def delete_session(
    chat_id: int,
    session_service: SessionService = Depends(get_session_service)
):
    await session_service.delete_session(chat_id)
    return {"status": "deleted"}