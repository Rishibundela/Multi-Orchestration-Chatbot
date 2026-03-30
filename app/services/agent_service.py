# app/services/agent_service.py

from typing import List, AsyncGenerator
from langchain_core.messages import BaseMessage

from app.agents.graph import build_graph
from app.services.rag_service import RAGService


class AgentService:

    _instance = None

    def __new__(cls, rag_service: RAGService):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, rag_service: RAGService):
        if hasattr(self, "_initialized"):
            return

        self.graph = build_graph(rag_service)
        self._initialized = True

    # -----------------------------
    # Normal Run
    # -----------------------------
    async def run(self, messages: List[BaseMessage]) -> str:

        state = {
            "messages": messages
        }

        result = await self.graph.ainvoke(state)

        # last message is the answer
        return result["messages"][-1].content

    # -----------------------------
    # Streaming Run
    # -----------------------------
    async def stream(
        self, messages: List[BaseMessage]
    ) -> AsyncGenerator[str, None]:

        state = {
            "messages": messages
        }

        # LangGraph streaming
        async for event in self.graph.astream(state):

            # extract tokens/messages
            if "messages" in event:
                last_msg = event["messages"][-1]

                if hasattr(last_msg, "content") and last_msg.content:
                    yield last_msg.content