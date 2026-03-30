# app/services/agent_service.py

from typing import List, AsyncGenerator
from pydantic import BaseModel
from groq import AsyncGroq

from app.agents.graph import build_graph
from app.services.rag_service import RAGService
from app.core.config import settings


# -----------------------------
# Request Schema (Optional)
# -----------------------------
class AgentRequest(BaseModel):
    query: str
    messages: List[str]


# -----------------------------
# Singleton Agent Service
# -----------------------------
class AgentService:

    _instance = None  # Singleton instance

    def __new__(cls, rag_service: RAGService):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, rag_service: RAGService):
        if hasattr(self, "_initialized"):
            return

        self.rag_service = rag_service

        # Build graph ONLY ONCE
        self.graph = build_graph(rag_service)

        # Groq client
        self.llm = AsyncGroq(api_key=settings.GROQ_API_KEY)

        self._initialized = True

    # -----------------------------
    # Normal Response
    # -----------------------------
    async def run(self, query: str, chat_history: List[str]):

        state = {
            "query": query,
            "messages": chat_history,
            "context": "",
            "tool_result": "",
            "decision": "",
            "response": ""
        }

        result = await self.graph.ainvoke(state)

        return result["response"]

    # -----------------------------
    # Streaming Response
    # -----------------------------
    async def stream(
        self, query: str, chat_history: List[str]
    ) -> AsyncGenerator[str, None]:

        # Step 1: Run graph FIRST (planner + rag + tool)
        state = {
            "query": query,
            "messages": chat_history,
            "context": "",
            "tool_result": "",
            "decision": "",
            "response": ""
        }

        result = await self.graph.ainvoke(state)

        # Step 2: Build final prompt
        prompt = f"""
User Query:
{query}

Context:
{result.get("context", "")}

Tool Output:
{result.get("tool_result", "")}

Answer clearly:
"""

        # Step 3: Stream from Groq
        stream = await self.llm.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt},
            ],
            stream=True,
        )

        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content