# ============================================================
# PHASE 2 — CUSTOMER DATA AGENT (MCP-backed)
# ============================================================

# Ensure the DB and MCPServer already exist from earlier cells:
# db = DatabaseSetup("support.db")
# db.connect()
# mcp_server = MCPServer(db)

# ----------------------------
# 1. MCP -> A2A TOOL WRAPPERS
# ----------------------------
def get_customer(customer_id: int):
    return mcp_server.get_customer(customer_id)

def list_customers(status: str, limit: int = 50):
    return mcp_server.list_customers(status, limit)

def update_customer(customer_id: int, data: dict):
    return mcp_server.update_customer(customer_id, data)

def create_ticket(customer_id: int, issue: str, priority: str = "medium"):
    return mcp_server.create_ticket(customer_id, issue, priority)

def get_history(customer_id: int):
    return mcp_server.get_customer_history(customer_id)

def get_billing_context(customer_id: int):
    return mcp_server.get_billing_context(customer_id)


# ----------------------------
# 2. CUSTOMER DATA AGENT
# ----------------------------
customer_data_agent = Agent(
    model="gemini-2.5-pro",
    name="customer_data_agent",
    instruction="""
You are the Customer Data Agent.

RULES:
- You NEVER reason.
- You NEVER infer user intent.
- You ONLY execute database operations through the tools.
- You ALWAYS return raw tool output exactly as given.
""",
    tools=[
        get_customer,
        list_customers,
        update_customer,
        create_ticket,
        get_history,
        get_billing_context,
    ]
)
print("Customer Data Agent created.")


# ----------------------------
# 3. AGENT CARD
# ----------------------------
customer_data_agent_card = AgentCard(
    name="Customer Data Agent",
    url="http://localhost:10030",
    description="Provides direct MCP-backed DB access for customers and tickets.",
    version="1.0",
    capabilities=AgentCapabilities(streaming=False),
    default_input_modes=["text/plain"],
    default_output_modes=["application/json"],
    preferred_transport=TransportProtocol.jsonrpc,
    skills=[
        AgentSkill(
            id="db_access",
            name="Database Access",
            description="Provides customer and ticket access (GET, LIST, UPDATE).",
            tags=["mcp", "database", "customers", "tickets"],
            examples=[
                "get customer 5",
                "list active customers",
                "update customer email",
            ],
        )
    ],
)

print("Customer Data AgentCard created.")