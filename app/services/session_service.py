# app/services/session_service.py

from app.db.repository import ChatRepository


class SessionService:

    def __init__(self, chat_repo: ChatRepository):
        self.chat_repo = chat_repo

    async def create_session(self):
        chat = await self.chat_repo.create_chat()
        return chat

    async def get_session(self, chat_id: int):
        return await self.chat_repo.get_chat(chat_id)

    async def delete_session(self, chat_id: int):
        await self.chat_repo.delete_chat(chat_id)