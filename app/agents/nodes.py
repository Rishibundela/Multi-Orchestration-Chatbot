# app/agents/nodes.py

from app.services.rag_service import RAGService
from app.tools.tools import tool_executor


# -----------------------------
# Planner Node
# -----------------------------
async def planner_node(state: dict):

    query = state["query"].lower()

    # VERY SIMPLE LOGIC (upgrade later with LLM)
    if "calculate" in query or "math" in query:
        state["decision"] = "tool"

    elif "what" in query or "explain" in query:
        state["decision"] = "rag"

    else:
        state["decision"] = "direct"

    return state


# -----------------------------
# RAG Node
# -----------------------------
async def rag_node(state: dict, rag_service: RAGService):

    docs = await rag_service.retrieve(state["query"])

    state["context"] = "\n".join(docs) if docs else ""
    return state


# -----------------------------
# Tool Node
# -----------------------------
async def tool_node(state: dict):

    result = await tool_executor(state["query"])
    state["tool_result"] = result

    return state


# -----------------------------
# Reasoning Node (LLM Placeholder)
# -----------------------------
async def reasoning_node(state: dict):

    query = state["query"]
    context = state.get("context", "")
    tool_result = state.get("tool_result", "")

    # Replace with real LLM later
    response = f"""
Query: {query}

Context:
{context}

Tool Result:
{tool_result}

Final Answer:
Processed intelligently.
"""

    state["response"] = response
    return state