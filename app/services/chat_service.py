# app/services/chat_service.py

from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from typing import List, AsyncGenerator

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
    # Helper: Convert DB → Messages
    # -----------------------------
    def _build_messages(self, db_messages, query: str) -> List[BaseMessage]:

        messages: List[BaseMessage] = []

        # Convert last N messages (STM)
        for m in db_messages[-5:]:
            if m.role == "user":
                messages.append(HumanMessage(content=m.content))
            else:
                messages.append(AIMessage(content=m.content))

        # Add current user query
        messages.append(HumanMessage(content=query))

        return messages

    # -----------------------------
    # Main Chat Flow
    # -----------------------------
    async def handle_query(self, chat_id: int, query: str) -> str:

        # 1. Store user message
        await self.message_repo.add_message(
            chat_id=chat_id,
            role="user",
            content=query
        )

        # 2. Fetch history from DB (LTM → STM)
        db_messages = await self.message_repo.get_messages(chat_id)

        # 3. Build LangGraph-compatible messages
        messages = self._build_messages(db_messages, query)

        # 4. Run agent
        response = await self.agent_service.run(messages)

        # 5. Store assistant response
        await self.message_repo.add_message(
            chat_id=chat_id,
            role="assistant",
            content=response
        )

        return response

    # -----------------------------
    # Streaming Chat Flow
    # -----------------------------
    async def stream_query(
        self, chat_id: int, query: str
    ) -> AsyncGenerator[str, None]:

        # 1. Store user message
        await self.message_repo.add_message(
            chat_id=chat_id,
            role="user",
            content=query
        )

        # 2. Fetch history
        db_messages = await self.message_repo.get_messages(chat_id)

        # 3. Build messages
        messages = self._build_messages(db_messages, query)

        # 4. Stream response
        full_response = ""

        async for chunk in self.agent_service.stream(messages):
            full_response += chunk
            yield chunk

        # 5. Store final response
        await self.message_repo.add_message(
            chat_id=chat_id,
            role="assistant",
            content=full_response
        )