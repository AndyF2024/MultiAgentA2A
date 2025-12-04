import sqlite3
import asyncio
from fastmcp import FastMCP
from configuration.config import MCP_PORT, DATABASE_PATH
from google.adk.tools.mcp_tool import McpToolset, StreamableHTTPConnectionParams

connection_params = StreamableHTTPConnectionParams(
    url="http://127.0.0.1:8001/mcp"
)

# Instance used ONLY for notebook tests, never passed to agents
test_mcp_tools = McpToolset(connection_params=connection_params)

# Separate fresh instance passed into ADK agents
agent_mcp_tools = McpToolset(connection_params=connection_params)


# MCP APP
mcp_app = FastMCP("SupportMCP")


# -----------------------------
# Database Connection
# -----------------------------
def get_conn():
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


# -----------------------------
# MCP TOOLS
# -----------------------------
@mcp_app.tool()
def get_customer(customer_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM customers WHERE id=?", (customer_id,))
    row = cur.fetchone()
    conn.close()
    return {"customer": dict(row) if row else None}


@mcp_app.tool()
def list_customers(status: str = "active", limit: int = 50):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM customers WHERE status=? LIMIT ?", (status, limit))
    rows = cur.fetchall()
    conn.close()
    return {"customers": [dict(r) for r in rows]}


@mcp_app.tool()
def update_customer(customer_id: int, data: dict):
    conn = get_conn()
    cur = conn.cursor()
    for key, value in data.items():
        cur.execute(f"UPDATE customers SET {key}=? WHERE id=?", (value, customer_id))
    conn.commit()
    conn.close()
    return {"updated": True}


@mcp_app.tool()
def create_ticket(customer_id: int, issue: str, priority: str = "medium"):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO tickets (customer_id, issue, status, priority)
        VALUES (?, ?, 'open', ?)
    """, (customer_id, issue, priority))
    conn.commit()
    conn.close()
    return {"ticket_created": True}


@mcp_app.tool()
def get_customer_history(customer_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tickets WHERE customer_id=?", (customer_id,))
    rows = cur.fetchall()
    conn.close()
    return {"history": [dict(r) for r in rows]}


# -----------------------------
# Run MCP Server
# -----------------------------
def start_fast_mcp():
    asyncio.run(
        mcp_app.run_async(
            transport="http",
            host="127.0.0.1",
            port=MCP_PORT
        )
    )

# Test if tools are set up correctly
# from google.adk.tools.mcp_tool import MCPTool
# import inspect
#
# print("=== MCPTool methods ===")
# for name, func in inspect.getmembers(MCPTool, inspect.isfunction):
#     print("-", name)
#
# print("\n=== MCPTool attributes ===")
# print([a for a in dir(MCPTool) if not a.startswith("_")])

#Test MCP Connection
# import asyncio
#
# async def test_mcp_connection():
#     print("Testing MCPToolset → FastMCP connection…")
#
#     # Load tools from MCP server
#     tools = await test_mcp_tools.get_tools()
#
#     print(f"✔ Loaded {len(tools)} tools from MCP server")
#     for t in tools:
#         print(" -", t.name)
#
#     # Try calling one tool
#     for t in tools:
#         if t.name == "list_customers":
#             print("\nCalling list_customers(status='active', limit=3)…")
#             result = await t.run_async(
#                 args={"status": "active", "limit": 3},
#                 tool_context=None
#             )
#             print("Result:", result)
#             break
#
# await test_mcp_connection()

if __name__ == "__main__":
    start_fast_mcp()

