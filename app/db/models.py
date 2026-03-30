from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from datetime import datetime
from pgvector.sqlalchemy import Vector

Base = declarative_base()


# -----------------------------
# Chat Table
# -----------------------------
class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    messages = relationship("Message", back_populates="chat", cascade="all, delete")


# -----------------------------
# Messages Table
# -----------------------------
class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), index=True)

    role = Column(String, nullable=False)
    content = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)

    chat = relationship("Chat", back_populates="messages")


# -----------------------------
# Documents (RAG)
# -----------------------------
class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    content = Column(Text)
    embedding = Column(Vector(1536))

    chat_id = Column(Integer, nullable=True)
    user_id = Column(String, nullable=True)

    source = Column(String, nullable=True)
    metadata_json = Column(Text, nullable=True)


# -----------------------------
# Summary Memory (IMPORTANT)
# -----------------------------
class ChatSummary(Base):
    __tablename__ = "chat_summaries"

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey("chats.id"))

    summary = Column(Text)
    updated_at = Column(DateTime, default=datetime.utcnow)