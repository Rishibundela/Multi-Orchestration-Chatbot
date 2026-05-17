# app/agents/graph.py

from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from app.agents.state import AgentState
from app.agents.nodes import (
    planner_node,
    rag_node,
    executor_node
)
from app.tools.tools import TOOLS


def build_graph(rag_service):

    graph = StateGraph(AgentState)

    # Nodes
    graph.add_node("planner", planner_node)
    graph.add_node("rag", lambda state: rag_node(state, rag_service))
    graph.add_node("executor", executor_node)
    graph.add_node("tools", ToolNode(TOOLS))

    # Entry
    graph.add_edge(START, "planner")

    # -----------------------------
    # Planner Routing
    # -----------------------------
    def route(state):
        decision = state.get("decision", "direct")

        if decision == "rag":
            return "rag"
        elif decision == "tool":
            return "executor"
        else:
            return "executor"

    graph.add_conditional_edges(
        "planner",
        route,
        {
            "rag": "rag",
            "executor": "executor",
        }
    )

    # RAG → Executor
    graph.add_edge("rag", "executor")

    # -----------------------------
    # Tool Loop
    # -----------------------------
    graph.add_conditional_edges("executor", tools_condition)
    graph.add_edge("tools", "executor")

    # Exit
    graph.add_edge("executor", END)

    return graph.compile()