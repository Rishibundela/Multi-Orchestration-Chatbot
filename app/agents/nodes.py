from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
import json

from app.core.config import settings
from app.tools.tools import get_llm_with_tools


planner_llm = ChatOpenAI(
    api_key=settings.GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
    model="llama-3.1-8b-instant",
    temperature=0
)


PLANNER_PROMPT = """
You are an intelligent AI planner.

Your job:
1. Understand user intent
2. Decide how to solve it

You MUST return JSON:

{
  "decision": "rag" | "tool" | "direct",
  "reasoning": "short explanation"
}

Guidelines:
- Use "rag" if question requires external knowledge or documents
- Use "tool" if calculation, API, search, or external action is needed
- Use "direct" if you can answer directly

Be precise. Do not explain outside JSON.
"""


async def planner_node(state: dict):

    user_message = state["messages"][-1]

    response = await planner_llm.ainvoke([
        SystemMessage(content=PLANNER_PROMPT),
        user_message
    ])

    try:
        parsed = json.loads(response.content)
        state["decision"] = parsed.get("decision", "direct")
        state["reasoning"] = parsed.get("reasoning", "")
    except:
        state["decision"] = "direct"

    return state

async def rag_node(state: dict, rag_service):

    query = state["messages"][-1].content
    docs = await rag_service.retrieve(query)

    context = "\n".join(docs) if docs else ""
    state["context"] = context

    if context:
        state["messages"].append(
            SystemMessage(content=f"Context:\n{context}")
        )

    return state

executor_llm = get_llm_with_tools()


async def executor_node(state: dict):

    messages = state["messages"]

    response = await executor_llm.ainvoke(messages)

    state["messages"].append(response)
    state["response"] = response.content

    return state