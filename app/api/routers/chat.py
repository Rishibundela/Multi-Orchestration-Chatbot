# app/api/routers/chat.py

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.core.database import get_db
from app.db.repository import MessageRepository
from app.db.vector_store import VectorStore
from app.services.chat_service import ChatService
from app.services.agent_service import AgentService
from app.services.rag_service import RAGService


router = APIRouter()


# -----------------------------
# Request Schema
# -----------------------------
class ChatRequest(BaseModel):
    query: str


# -----------------------------
# Dependency Builder
# -----------------------------
def get_chat_service(db: AsyncSession = Depends(get_db)):

    # DB layer
    message_repo = MessageRepository(db)
    vector_store = VectorStore(db)

    # Services
    rag_service = RAGService(vector_store)
    agent_service = AgentService(rag_service)

    return ChatService(message_repo, agent_service)


# -----------------------------
# Normal Chat Endpoint
# -----------------------------
@router.post("/{chat_id}/query")
async def chat(
    chat_id: int,
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service)
):
    response = await chat_service.handle_query(
        chat_id=chat_id,
        query=request.query
    )

    return {"response": response}


# -----------------------------
# Streaming Chat Endpoint
# -----------------------------
@router.post("/{chat_id}/stream")
async def stream_chat(
    chat_id: int,
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service)
):

    async def generator():
        async for chunk in chat_service.stream_query(
            chat_id=chat_id,
            query=request.query
        ):
            yield chunk

    return StreamingResponse(generator(), media_type="text/plain")