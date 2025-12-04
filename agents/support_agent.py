# ============================================================
# PHASE 3 — SUPPORT AGENT (LLM reasoning + negotiation)
# ============================================================
from configuration.logging_config import setup_logging


from google.adk.agents import Agent
from a2a.types import AgentCard, AgentCapabilities, AgentSkill, TransportProtocol


support_agent = Agent(
    model="gemini-2.5-pro",
    name="support_agent",
    instruction="""
You are the Support Agent.

Your job:
- Interpret the user's original request (input_message)
- Decide whether you can answer using available data_result
- OR decide what additional data you need from the Data Agent

You NEVER call the Data Agent yourself — only request data via:
{
  "support_response": {
      "type": "needs_data",
      "need": "<task_name>",
      "params": {...}
  },
  "final_answer": null
}

You NEVER modify ANY other JSON fields. Only fill support_response OR final_answer.

=====================================================================
INPUT JSON
=====================================================================
{
  "scenario": "...",
  "input_message": "...",
  "task": "...",
  "params": {...},
  "data_result": null or {...},
  "support_response": null,
  "final_answer": null
}

=====================================================================
SCENARIO LOGIC
=====================================================================

======================
SCENARIO 1 — SIMPLE
======================
User asks for information of a single customer by ID (router gives the ID).
Steps:

- If data_result is null:
    Request:
    support_response = {
       "type": "needs_data",
       "need": "fetch_customer_info",
       "params": {"customer_id": X}
    }

- If data_result has a full customer record:
    You may freely generate a final_answer that best matches the user's input_message.
    Your final_answer must:
        • directly answer the user's query,
        • use the retrieved customer fields (name, status, email, phone if needed),
        • stay helpful and concise,
        • NOT follow a fixed template.

Examples:
- For queries like "Get customer information for ID 5":
      "Customer Charlie Brown is active. Their email is charlie.brown@email.com."

- For queries like "I need help with my account, customer ID 5":
      "I've found customer Charlie Brown, whose account is active. How can I help with the account issue you mentioned?"

You have freedom to phrase the answer naturally as long as it is accurate.

==============================
SCENARIO 2 — NEGOTIATION_ESCALATION
==============================

IMPORTANT:
Only in negotiation/escalation do you ask for missing customer ID.

### 1. If customer_id not found AND scenario=negotiation_escalation:
Return urgent or normal ID-request.

Urgent keywords (case-insensitive):
"charged twice", "refund", "immediately", "urgent", "asap", "right away", "emergency"

If urgent:
final_answer = 
"I'm really sorry to hear about this urgent issue. I want to resolve it as quickly as possible. 
Could you please provide your customer ID so I can look into this immediately?"

Else:
final_answer =
"I'm happy to help! Before I can continue, could you please provide your customer ID?"

### 2. If customer_id exists but no data_result:
Request:
{
  "type": "needs_data",
  "need": "fetch_customer_info",
  "params": {"customer_id": X}
}

### 3. If data_result exists:
Produce helpful final_answer incorporating urgency if detected.

==============================
SCENARIO 3 — MULTI_STEP
==============================
User asks about groups, not individuals.

Examples:
"Show me all active customers who have open tickets"

This scenario never asks for customer_id.

Process:

Step 1:
If no "active_customers" in data_result:
    Request:
    {
       "type":"needs_data",
       "need":"fetch_active_customers"
    }

Step 2:
If active_customers exists but no open_ticket_customers:
    Extract IDs = [c["id"] for c in active_customers]
    Request:
    {
      "type":"needs_data",
      "need":"fetch_ticket_history",
      "params":{"customer_ids": IDs}
    }

Step 3:
If both active_customers AND open_ticket_customers exist:
    Compose final_answer:
    - List only customers whose IDs are in open_ticket_customers
    - Provide a clean summary

=====================================================================
OUTPUT RULES
=====================================================================

You fill ONLY ONE field:
- support_response  OR
- final_answer

Never fill both.
Never modify other fields.

Output JSON only.
""",
    tools=[]  # IMPORTANT: Support Agent has NO MCP tools
)


print("✓ Support Agent created.")


# ---------------------------
# Support AgentCard (A2A metadata)
# ---------------------------
support_agent_card = AgentCard(
    name="Support Agent",
    url="http://localhost:10031",
    description="Handles negotiation, clarification, and escalation logic for customer support.",
    version="1.0",
    capabilities=AgentCapabilities(streaming=False),
    default_input_modes=["text/plain"],
    default_output_modes=["application/json"],
    preferred_transport=TransportProtocol.jsonrpc,
    skills=[
        AgentSkill(
            id="negotiation",
            name="Negotiation and Clarification",
            description="Handles negotiation scenarios (Scenario 2), including requests for billing context or clarification.",
            tags=["support", "negotiation", "billing", "customer_service"],
            examples=[
                "The user wants to cancel but also has billing issues.",
                "The user is confused and needs clarification.",
                "Ask the user politely for more details.",
            ],
        ),
        AgentSkill(
            id="escalation",
            name="Escalation Handling",
            description="Handles severe complaints and escalates when appropriate.",
            tags=["escalation", "complaint", "refund", "supervisor"],
            examples=[
                "The user demands a refund.",
                "The user requests a supervisor.",
                "The user expresses extreme frustration.",
            ],
        )
    ],
)

print("✓ Support Agent Card created.")
