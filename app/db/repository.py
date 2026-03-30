# app/db/repository.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.db.models import Chat, Message


# -----------------------------
# Chat Repository
# -----------------------------
class ChatRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_chat(self):
        chat = Chat()
        self.db.add(chat)
        await self.db.commit()
        await self.db.refresh(chat)
        return chat

    async def get_chat(self, chat_id: int):
        result = await self.db.execute(
            select(Chat).where(Chat.id == chat_id)
        )
        return result.scalar_one_or_none()

    async def delete_chat(self, chat_id: int):
        await self.db.execute(
            delete(Chat).where(Chat.id == chat_id)
        )
        await self.db.commit()


# -----------------------------
# Message Repository
# -----------------------------
class MessageRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_message(self, chat_id: int, role: str, content: str):
        msg = Message(
            chat_id=chat_id,
            role=role,
            content=content
        )
        self.db.add(msg)
        await self.db.commit()

    async def get_messages(self, chat_id: int):
        result = await self.db.execute(
            select(Message).where(Message.chat_id == chat_id)
        )
        return result.scalars().all()