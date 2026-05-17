# app/core/database.py

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from app.core.config import settings

load_dotenv()

DATABASE_URL = settings.DATABASE_URL

# -----------------------------
# Engine
# -----------------------------
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # disable in production
    future=True
)

# -----------------------------
# Session
# -----------------------------
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)

# -----------------------------
# Dependency
# -----------------------------
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session