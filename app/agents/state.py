# app/agents/state.py

from typing import TypedDict, Annotated, Optional
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

    # planner output
    decision: Optional[str]        # "rag" | "tool" | "direct"
    reasoning: Optional[str]

    # rag
    context: Optional[str]

    # final
    response: Optional[str]