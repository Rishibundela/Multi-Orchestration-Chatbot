# app/core/database.py

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

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
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# -----------------------------
# Dependency
# -----------------------------
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session