# app/agents/state.py

from typing import TypedDict, List, Optional


class AgentState(TypedDict):
    # User input
    query: str

    # Chat history (STM)
    messages: List[str]

    # RAG context
    context: Optional[str]

    # Tool output
    tool_result: Optional[str]

    # Planner decision
    decision: Optional[str]

    # Final response
    response: Optional[str]