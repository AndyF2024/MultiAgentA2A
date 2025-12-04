# ============================================================
# PHASE 4 — ROUTER AGENT
# ============================================================
from configuration.logging_config import setup_logging


from google.adk.agents import Agent
from a2a.types import AgentCard, AgentCapabilities, AgentSkill, TransportProtocol
import re
import json


router_agent = Agent(
    model="gemini-2.5-pro",
    name="router_agent",
    instruction="""
You are the Router Agent.

Your job: **coordinate all other agents** (SUPPORT and DATA) by:
1. Identifying the scenario type (simple, negotiation_escalation, multi_step)
2. Delegating to SUPPORT when interpretation is needed
3. Delegating to DATA when structured data is needed
4. NEVER answering the user yourself
5. NEVER deleting or altering any JSON fields other than `task` and `params`

=====================================================================
INPUT JSON (from user or another agent)
=====================================================================
{
  "scenario": null or "simple" or "negotiation_escalation" or "multi_step",
  "input_message": "...original user query...",
  "task": null,
  "params": {},
  "data_result": null,
  "support_response": null,
  "final_answer": null
}

You must ALWAYS return the **entire JSON**, preserving all fields.

=====================================================================
SCENARIO DETECTION RULES (FIRST PASS ONLY)
=====================================================================

If scenario is null (first run):

- SIMPLE:
    Triggered when user asks:
      - "Get customer information for ID X"
      - "What is the info for customer X?"

- NEGOTIATION_ESCALATION:
    Triggered for:
      - refund requests
      - cancellation + billing
      - account upgrade help
      - customer-specific issues requiring ID

    Examples:
      "I'm customer 5 and need help upgrading my account"
      "I've been charged twice, please refund immediately!"
      "I want to cancel my subscription but I'm having billing issues"

- MULTI_STEP:
    Triggered for queries asking about:
      - sets of customers
      - aggregate conditions
      - multi-stage data retrieval

    Examples:
      "Show me all active customers who have open tickets"
      "What's the status of all high-priority tickets for premium customers?"

Router must set scenario accordingly.

=====================================================================
ROUTER LOGIC
=====================================================================

### 1. If final_answer is already filled:
Return JSON unchanged.

### 2. If support_response exists:
Router must translate support_response into a DATA AGENT request.

Support will produce:
{
  "type": "needs_data",
  "need": "<data_task_name>",
  "params": {...optional...}
}

Router must translate it into:

task = support_response.need
params = support_response.params or {}

Examples:
- need: "fetch_customer_info"  → task="fetch_customer_info"
- need: "fetch_active_customers" → task="fetch_active_customers"
- need: "fetch_ticket_history" → task="fetch_ticket_history"

Router NEVER chooses data tasks itself.

### 3. After receiving DATA_RESULT from Data Agent:
Do NOT modify data_result.
Instead:
- Reset support_response to null
- Set task to: 
  "Check whether you now have enough data to answer the user's input_message. 
   If not, say what you still need."

Then send back to SUPPORT unchanged.

=====================================================================
OUTPUT FORMAT
=====================================================================

You must always return JSON in the following format:

{
  "scenario": "...",
  "input_message": "...same...",
  "task": "...possibly updated...",
  "params": { ...possibly updated... },
  "data_result": ...preserved or updated...,
  "support_response": null or { ... },
  "final_answer": null or "...string..."
}

Return ONLY JSON — no explanations.
"""
)


print("✓ Router Agent created.")


# ---------------------------
# Router AgentCard (A2A metadata)
# ---------------------------
router_agent_card = AgentCard(
    name="Router Agent",
    description="Routes user queries to Data or Support agents based on scenario.",
    url="http://localhost:10032",
    version="1.0",
    capabilities=AgentCapabilities(streaming=False),
    default_input_modes=["text/plain"],
    default_output_modes=["application/json"],
    preferred_transport=TransportProtocol.jsonrpc,
    skills=[
        AgentSkill(
            id="intent_detection",
            name="Intent Detection",
            description="Classifies queries for routing to Data or Support agents.",
            tags=["routing", "intent", "classification"],
            examples=[
                "Show me customer 3",
                "Find all active users",
                "I want to cancel my subscription but I also have billing issues",
                "This is ridiculous! I want a refund now!"
            ]
        )
    ],
)


print("✓ Router Agent Card created.")

#print("MCP server restarting...")
# Use ONLY the test toolset for notebook checks
# tools = await test_mcp_tools.get_tools()
# print("✔ Tools loaded from MCP (notebook test):")
# tools
