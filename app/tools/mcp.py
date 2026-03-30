# app/tools/mcp.py

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.tools import BaseTool
import asyncio


# -----------------------------
# Async Runner (like your ref)
# -----------------------------
_ASYNC_LOOP = asyncio.new_event_loop()

def _run_async(coro):
    return _ASYNC_LOOP.run_until_complete(coro)


# -----------------------------
# MCP Client
# -----------------------------
client = MultiServerMCPClient(
    {
        "arith": {
            "transport": "stdio",
            "command": "python3",
            "args": ["./mcp_servers/math_server.py"],  # change path
        },
        "external_api": {
            "transport": "streamable_http",
            "url": "https://example-mcp-server.com/mcp"
        }
    }
)


# -----------------------------
# Load MCP Tools
# -----------------------------
def load_mcp_tools() -> list[BaseTool]:
    try:
        return _run_async(client.get_tools())
    except Exception:
        return []