from datetime import datetime
from sqlalchemy import String, Text, ForeignKey, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector
from app.db.base import Base
from datetime import datetime, timezone

class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))

    messages: Mapped[list["Message"]] = relationship("Message", back_populates="chat", cascade="all, delete")

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"), index=True)
    
    role: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))

    chat: Mapped["Chat"] = relationship("Chat", back_populates="messages")



# -----------------------------
# Documents (RAG)
# -----------------------------
class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    content: Mapped[str] = mapped_column(Text)
    embedding: Mapped[Vector] = mapped_column(Vector(1536))

    chat_id: Mapped[int] = mapped_column(Integer, nullable=True)
    user_id: Mapped[str] = mapped_column(String, nullable=True)

    source: Mapped[str] = mapped_column(String, nullable=True)
    metadata_json: Mapped[str] = mapped_column(Text, nullable=True)


# -----------------------------
# Summary Memory (IMPORTANT)
# -----------------------------
class ChatSummary(Base):
    __tablename__ = "chat_summaries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chat_id: Mapped[int] = mapped_column(Integer, ForeignKey("chats.id"))

    summary: Mapped[str] = mapped_column(Text)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))