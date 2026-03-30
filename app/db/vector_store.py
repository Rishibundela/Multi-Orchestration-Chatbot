# app/db/vector_store.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text


class VectorStore:

    def __init__(self, db: AsyncSession):
        self.db = db

    # -----------------------------
    # Store embeddings
    # -----------------------------
    async def add_document(self, content: str, embedding):
        sql = text("""
            INSERT INTO documents (content, embedding)
            VALUES (:content, :embedding)
        """)

        await self.db.execute(sql, {
            "content": content,
            "embedding": embedding
        })

        await self.db.commit()

    # -----------------------------
    # Similarity Search
    # -----------------------------
    async def similarity_search(self, embedding, k: int = 3):
        sql = text("""
            SELECT content
            FROM documents
            ORDER BY embedding <-> :embedding
            LIMIT :k
        """)

        result = await self.db.execute(sql, {
            "embedding": embedding,
            "k": k
        })

        rows = result.fetchall()
        return [r[0] for r in rows]