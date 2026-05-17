from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, asc
from app.db.models import Chat, Message

class ChatRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_chat(self, user_id: Optional[str] = None) -> Chat:
        chat = Chat(user_id=user_id)
        self.db.add(chat)
        await self.db.commit()
        # Only refresh if you need the 'created_at' timestamp immediately
        await self.db.refresh(chat) 
        return chat

    async def get_chat(self, chat_id: int) -> Optional[Chat]:
        # Using .get() is faster and cleaner for primary key lookups
        return await self.db.get(Chat, chat_id)

    async def delete_chat(self, chat_id: int) -> None:
        query = delete(Chat).where(Chat.id == chat_id)
        await self.db.execute(query)
        await self.db.commit()

class MessageRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_message(self, chat_id: int, role: str, content: str) -> Message:
        msg = Message(
            chat_id=chat_id,
            role=role,
            content=content
        )
        self.db.add(msg)
        await self.db.commit()
        await self.db.refresh(msg)
        return msg

    async def get_messages(self, chat_id: int) -> List[Message]:
        result = await self.db.execute(
            select(Message)
            .where(Message.chat_id == chat_id)
            .order_by(asc(Message.created_at))
        )
        return list(result.scalars().all())