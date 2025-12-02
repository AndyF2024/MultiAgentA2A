# ============================================================
# PHASE 3 — SUPPORT AGENT (LLM reasoning only)
# ============================================================

# ----------------------------
# SUPPORT AGENT (REASONING ONLY)
# ----------------------------
support_agent = Agent(
    model="gemini-2.5-pro",
    name="support_agent",
    instruction="""
You are the Support Agent.

Your responsibilities:
- Interpret the customer's query.
- Determine what information is needed from the Customer Data Agent.
- Request data via JSON instructions.
- Produce a final helpful support response ONLY once all information is available.

IMPORTANT RULES:
- You DO NOT use tools.
- You NEVER trigger function calls.
- You ALWAYS output clean JSON.
- JSON must be in one of two forms:

1. REQUEST FOR MORE DATA
{
  "need": "<one_of: customer_info, ticket_history, list_customers, update_customer, create_ticket, billing_context>",
  "customer_id": <optional>,
  "data": <optional>,
  "status": <optional>,
  "reason": "<why you need this>"
}

2. FINAL ANSWER
{
  "final_message": "<short user-facing message>"
}

Avoid chain-of-thought. Only provide the result.
""",
    tools=[]  # Support agent MUST have no tools
)

print("Support Agent created.")


# ----------------------------
# 2. SUPPORT AGENT CARD
# ----------------------------
support_agent_card = AgentCard(
    name="Support Agent",
    url="http://localhost:10031",
    description="Provides LLM-based customer support reasoning.",
    version="1.0",
    capabilities=AgentCapabilities(streaming=False),
    default_input_modes=["text/plain"],
    default_output_modes=["application/json"],
    preferred_transport=TransportProtocol.jsonrpc,
    skills=[
        AgentSkill(
            id="support_reasoning",
            name="Support Reasoning",
            description="Interprets and helps with support-related queries.",
            tags=["support", "billing", "account", "troubleshooting"],
            examples=[
                "I want to upgrade my account",
                "I need help with billing issues",
                "Why can't I log in?"
            ],
        )
    ],
)

print("Support AgentCard created.")
