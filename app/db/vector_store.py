# app/db/vector_store.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from sqlalchemy import select
from app.db.models import ChatSummary


class VectorStore:

    def __init__(self, db: AsyncSession):
        self.db = db

    # -----------------------------
    # Store embeddings
    # -----------------------------
    async def add_document(
        self,
        content: str,
        embedding,
        chat_id: int = None,
        user_id: str = None,
        source: str = None
    ):
        sql = text("""
            INSERT INTO documents (content, embedding, chat_id, user_id, source)
            VALUES (:content, :embedding, :chat_id, :user_id, :source)
        """)

        await self.db.execute(sql, {
            "content": content,
            "embedding": embedding,
            "chat_id": chat_id,
            "user_id": user_id,
            "source": source
        })

        await self.db.commit()

    # -----------------------------
    # Similarity Search
    # -----------------------------
    async def similarity_search(self, embedding, k: int = 3):
        sql = text("""
            SELECT content, embedding <-> :embedding AS distance
            FROM documents
            ORDER BY embedding <-> :embedding
            LIMIT :k
        """)

        result = await self.db.execute(sql, {
            "embedding": embedding,
            "k": k
        })

        rows = result.fetchall()

        return [
            {"content": r[0], "distance": r[1]}
            for r in rows
        ]



class SummaryRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_summary(self, chat_id: int):
        result = await self.db.execute(
            select(ChatSummary).where(ChatSummary.chat_id == chat_id)
        )
        return result.scalar_one_or_none()

    async def upsert_summary(self, chat_id: int, summary: str):

        existing = await self.get_summary(chat_id)

        if existing:
            existing.summary = summary
        else:
            self.db.add(ChatSummary(chat_id=chat_id, summary=summary))

        await self.db.commit()