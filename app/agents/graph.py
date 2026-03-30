# app/agents/graph.py

from langgraph.graph import StateGraph, END

from app.agents.state import AgentState
from app.agents.nodes import (
    planner_node,
    rag_node,
    tool_node,
    reasoning_node,
)

from app.services.rag_service import RAGService


# -----------------------------
# Build Graph
# -----------------------------
def build_graph(rag_service: RAGService):

    graph = StateGraph(AgentState)

    # Nodes
    graph.add_node("planner", planner_node)
    graph.add_node("rag", lambda state: rag_node(state, rag_service))
    graph.add_node("tool", tool_node)
    graph.add_node("reason", reasoning_node)

    # Entry
    graph.set_entry_point("planner")

    # Conditional Routing
    def route(state):
        decision = state["decision"]

        if decision == "rag":
            return "rag"
        elif decision == "tool":
            return "tool"
        else:
            return "reason"

    graph.add_conditional_edges(
        "planner",
        route,
        {
            "rag": "rag",
            "tool": "tool",
            "direct": "reason",
        },
    )

    # Flow
    graph.add_edge("rag", "reason")
    graph.add_edge("tool", "reason")
    graph.add_edge("reason", END)

    return graph.compile()