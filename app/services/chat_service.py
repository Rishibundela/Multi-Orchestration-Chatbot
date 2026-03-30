# app/services/chat_service.py

from app.db.repository import MessageRepository
from app.services.agent_service import AgentService


class ChatService:

    def __init__(
        self,
        message_repo: MessageRepository,
        agent_service: AgentService
    ):
        self.message_repo = message_repo
        self.agent_service = agent_service

    # -----------------------------
    # Main Chat Flow
    # -----------------------------
    async def handle_query(self, chat_id: int, query: str):

        # 1. Store user message
        await self.message_repo.add_message(
            chat_id=chat_id,
            role="user",
            content=query
        )

        # 2. Fetch chat history (STM)
        messages = await self.message_repo.get_messages(chat_id)

        # Keep last N messages (important)
        history = [m.content for m in messages[-5:]]

        # 3. Run agent
        response = await self.agent_service.run(query, history)

        # 4. Store assistant response
        await self.message_repo.add_message(
            chat_id=chat_id,
            role="assistant",
            content=response
        )

        return response

    # -----------------------------
    # Streaming Version
    # -----------------------------
    async def stream_query(self, chat_id: int, query: str):

        # Store user message
        await self.message_repo.add_message(
            chat_id=chat_id,
            role="user",
            content=query
        )

        # Fetch history
        messages = await self.message_repo.get_messages(chat_id)
        history = [m.content for m in messages[-5:]]

        # Stream response
        async for chunk in self.agent_service.stream(query, history):
            yield chunk

        # ⚠️ Optional: store final response (requires buffering)