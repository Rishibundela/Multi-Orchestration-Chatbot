# app/services/rag_service.py

from app.db.vector_store import VectorStore
from app.utils.embeddings import get_embedding


class RAGService:

    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store

    async def retrieve(self, query: str, k: int = 3):
        embedding = await get_embedding(query)
        docs = await self.vector_store.similarity_search(embedding, k)
        return docs