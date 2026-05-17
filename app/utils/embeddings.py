# app/utils/embeddings.py

from typing import List
from groq import AsyncGroq
from app.core.config import settings


class EmbeddingService:
    def __init__(self):
        self.client = AsyncGroq(api_key=settings.GROQ_API_KEY)

    async def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text
        """
        response = await self.client.embeddings.create(
            model="text-embedding-3-small",  # OpenAI-compatible
            input=text
        )
        return response.data[0].embedding

    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Batch embeddings (faster ingestion)
        """
        response = await self.client.embeddings.create(
            model="text-embedding-3-small",
            input=texts
        )
        return [item.embedding for item in response.data]


# Singleton instance
embedding_service = EmbeddingService()


# Convenience functions
async def get_embedding(text: str):
    return await embedding_service.embed_text(text)


async def get_embeddings(texts: List[str]):
    return await embedding_service.embed_batch(texts)