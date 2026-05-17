# app/api/routers/rag.py

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.db.vector_store import VectorStore
from app.services.rag_service import RAGService
from app.utils.helpers import clean_query


router = APIRouter()


# -----------------------------
# Dependency
# -----------------------------
def get_rag_service(db: AsyncSession = Depends(get_db)):
    vector_store = VectorStore(db)
    return RAGService(vector_store)


# -----------------------------
# Simple Text Ingestion
# -----------------------------
@router.post("/ingest-text")
async def ingest_text(
    content: str,
    rag_service: RAGService = Depends(get_rag_service)
):
    docs = [clean_query(content)]
    
    # embedding + store handled in service
    await rag_service.vector_store.add_document(
        content=docs[0],
        embedding=await rag_service.vector_store.db.run_sync(
            lambda _: None
        )  # placeholder, replace with embedding call in service
    )

    return {"status": "text ingested"}