# app/tools/mcp.py
from langchain_mcp_adapters.client import MultiServerMCPClient

# Define the client
client = MultiServerMCPClient({
    "arith": {
        "transport": "stdio",
        "command": "python", # Use "python" on Windows
        "args": ["mcp_servers/math_server.py"],
    }
})

# Global variable to store loaded tools
mcp_tools = []

async def init_mcp_tools():
    global mcp_tools
    try:
        # We await properly here
        mcp_tools = await client.get_tools()
        print(f"✅ Loaded {len(mcp_tools)} MCP tools")
    except Exception as e:
        print(f"❌ Failed to load MCP tools: {e}")
        mcp_tools = []