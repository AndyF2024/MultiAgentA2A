# ============================================================
# PHASE 4 — ROUTER AGENT (ORCHESTRATOR)
# ============================================================

# Router will call both:
# - remote_customer_data_agent  (DB access)
# - remote_support_agent        (reasoning)

remote_support_agent = RemoteA2aAgent(
    name="support_agent",
    description="Remote Support Agent",
    agent_card="http://localhost:10031/.well-known/agent-card.json",
)

remote_customer_data_agent = RemoteA2aAgent(
    name="customer_data_agent",
    description="Remote Customer Data Agent",
    agent_card="http://localhost:10030/.well-known/agent-card.json",
)


# ----------------------------
# 1. ROUTER AGENT
# ----------------------------
router_agent = Agent(
    model="gemini-2.5-pro",
    name="router_agent",
    instruction="""
You are the Router Agent.

You coordinate two sub-agents:
1. The Support Agent, which does reasoning about the user's request.
2. The Customer Data Agent, which retrieves data from the database.

You never call tools directly.
You never emit a function_call.
You never return JSON or any structured objects.
You speak only in plain natural language messages.

===========================================================
SCENARIO CLASSIFICATION
===========================================================

Choose exactly one of these three high-level scenarios based on the user's query:

Scenario 1: Task Allocation  
The user provides a customer ID or requests help with their own account.  
In this case:
- First ask the Customer Data Agent to retrieve that customer's information.
- Then send that retrieved information to the Support Agent.
- Continue following the Support Agent's requests until it gives a final answer.

Scenario 2: Negotiation or Escalation  
The user expresses multiple or conflicting concerns, such as cancellation combined
with billing problems or urgency.  
In this case:
- Send the full user query to the Support Agent.
- The Support Agent will reply by indicating what information it needs,
  using a simple phrase like: need: customer_info   or   need: billing_records
- Ask the Customer Data Agent for exactly what was requested.
- Send the returned data back to the Support Agent.
- Repeat this loop until the Support Agent explicitly gives a final answer.

Scenario 3: Multi-Step Coordination  
The user asks for an aggregated or multi-customer report, such as all premium
customers with high-priority tickets.  
In this case:
- Ask the Customer Data Agent for the customer group needed.
- Send the list to the Support Agent.
- The Support Agent may ask for additional information for each customer.
- Retrieve whatever is required and send it back.
- Repeat until the Support Agent gives a final answer.

===========================================================
COMMUNICATION RULES
===========================================================

When sending a message to either sub-agent:
- Start the message with the prefix: ROUTER_MESSAGE:
- Then describe in plain English what information is needed.

The Support Agent will always reply in one of two ways:
1. It may request more information, using a short natural-language phrase that begins with "need:".
2. It may provide its final answer, using a phrase that begins with "final:".

Whenever you see a message beginning with “need:”:
- Ask the Customer Data Agent for exactly what is needed,
  again using a plain English request.

Whenever you see a message beginning with “final:”:
- Stop and return that final answer.

===========================================================
IMPORTANT PROHIBITIONS
===========================================================

Do not output JSON.
Do not output curly braces.
Do not output lists.
Do not output structured data of any kind.
Do not emit function_call.
Do not reference tools or tool names.
Do not use XML or call-like markup.

Everything must be expressed as plain English text.

""",
    sub_agents=[remote_support_agent, remote_customer_data_agent]
)



print("STRICT Router Agent (All scenarios) created.")


# ----------------------------
# 2. ROUTER AGENT CARD
# ----------------------------
router_agent_card = AgentCard(
    name="Router Agent",
    url="http://localhost:10032",
    description="Coordinates Support + Customer Data Agents for customer queries.",
    version="1.0",
    capabilities=AgentCapabilities(streaming=False),
    default_input_modes=["text/plain"],
    default_output_modes=["application/json"],
    preferred_transport=TransportProtocol.jsonrpc,
    skills=[
        AgentSkill(
            id="route_queries",
            name="Query Routing",
            description="Understands customer queries and delegates tasks.",
            tags=["router", "coordination", "support"],
            examples=[
                "Get customer information for ID 5",
                "I'm customer 12 and need help upgrading",
                "Show me all active customers with open tickets"
            ],
        )
    ],
)

print("Router AgentCard created.")

