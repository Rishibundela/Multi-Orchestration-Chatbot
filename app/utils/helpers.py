# app/utils/helpers.py

from typing import List


# -----------------------------
# Chat Formatting
# -----------------------------
def format_messages(messages: List[str]) -> str:
    """
    Convert message list into readable context
    """
    return "\n".join(messages)


# -----------------------------
# Sliding Window Memory
# -----------------------------
def get_recent_messages(messages: List, limit: int = 5):
    """
    Return last N messages (STM)
    """
    return messages[-limit:]


# -----------------------------
# Safe Join (avoid None issues)
# -----------------------------
def safe_join(items: List[str]) -> str:
    return "\n".join([i for i in items if i])


# -----------------------------
# Basic Query Cleaner
# -----------------------------
def clean_query(query: str) -> str:
    return query.strip().lower()


# -----------------------------
# Simple Token Estimation
# -----------------------------
def estimate_tokens(text: str) -> int:
    """
    Rough token estimation (1 token ≈ 4 chars)
    """
    return len(text) // 4


# -----------------------------
# Context Builder
# -----------------------------
def build_context(summary: str, recent: List[str], rag: str) -> str:
    """
    Combine all memory sources
    """
    parts = []

    if summary:
        parts.append(f"Summary:\n{summary}")

    if recent:
        parts.append(f"Recent:\n{format_messages(recent)}")

    if rag:
        parts.append(f"Knowledge:\n{rag}")

    return "\n\n".join(parts)