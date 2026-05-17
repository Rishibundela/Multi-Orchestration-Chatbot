# app/tools/tools.py

from langchain_core.tools import tool, BaseTool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_openai import ChatOpenAI

from app.tools.mcp_client import mcp_tools
from app.core.config import settings


# -----------------------------
# Base Tools
# -----------------------------
search_tool = DuckDuckGoSearchRun(region="us-en")


@tool
def calculator(first_num: float, second_num: float, operation: str) -> dict:
    """Perform arithmetic: add, sub, mul, div"""
    try:
        if operation == "add":
            return {"result": first_num + second_num}
        elif operation == "sub":
            return {"result": first_num - second_num}
        elif operation == "mul":
            return {"result": first_num * second_num}
        elif operation == "div":
            return {"result": first_num / second_num}
        return {"error": "Invalid operation"}
    except Exception as e:
        return {"error": str(e)}


@tool
def get_stock_price(symbol: str) -> dict:
    """Fetch stock price"""
    import requests
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=demo"
    return requests.get(url).json()


# -----------------------------
# MCP Tools
# -----------------------------
mcp_tools: list[BaseTool] = mcp_tools


# -----------------------------
# Combine All Tools
# -----------------------------
TOOLS: list[BaseTool] = [
    search_tool,
    calculator,
    get_stock_price,
    *mcp_tools
]


# -----------------------------
# LLM with Tools (Groq-compatible)
# -----------------------------
def get_llm_with_tools():
    llm = ChatOpenAI(
        api_key=settings.GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1",
        model="llama-3.1-8b-instant",
        temperature=0
    )

    return llm.bind_tools(TOOLS)