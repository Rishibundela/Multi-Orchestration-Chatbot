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
    def _build_messages(self, db_messages) -> List[BaseMessage]:
    # 🔹 LIMIT TO THE LAST 6 MESSAGES (3 rounds of Q&A)
    # This prevents the list from growing indefinitely in the Agent's prompt.
        limited_history = db_messages[-8:] 
        
        messages: List[BaseMessage] = []
        for m in limited_history:
            if m.role == "user":
                messages.append(HumanMessage(content=m.content))
            else:
                messages.append(AIMessage(content=m.content))
                
        return messages

    # -----------------------------
    # Main Chat Flow
    # -----------------------------
    # app/services/chat_service.py

    async def handle_query(self, chat_id: int, query: str) -> str:
        # 1. Save the new message to DB first
        await self.message_repo.add_message(
            chat_id=chat_id, 
            role="user", 
            content=query
        )

        # 2. Fetch history (THIS NOW INCLUDES THE QUERY ABOVE)
        db_messages = await self.message_repo.get_messages(chat_id)

        # 3. Convert ONLY what is in the DB to LangChain objects
        # Note: We don't pass 'query' here anymore!
        messages = self._build_messages(db_messages)

        # 4. Run the agent
        response = await self.agent_service.run(messages)

        # 5. Save the AI response
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
        messages = self._build_messages(db_messages)

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