# MultiAgentA2A

Multi-Agent A2A Customer Support System (HW5)

This project implements a three-agent customer support system using Google A2A (Agent-to-Agent) communication and an MCP-backed database. The system demonstrates agent coordination, multi-step reasoning, and multi-message workflows across several realistic customer support scenarios.

==============================================================================================================================================================
# System Overview
1. Customer Data Agent (MCP-Backed)

Executes database operations:

Get customer info

List customers

Get ticket history

Create tickets

Billing placeholder lookup

Never reasons about the query.

Only returns raw data.

2. Support Agent (Reasoning Agent)

Interprets user queries.

Determines what information is needed next.

Uses structured JSON messages:

need: ...

final_message: ...

Never calls tools directly.

3. Router Agent (Coordinator)

Classifies each query into one of three high-level scenarios:

Task Allocation

Negotiation / Escalation

Multi-Step Coordination

Forwards user messages and data between agents.

==============================================================================================================================================================
# Key Features

Full MCP server backing SQLite database

Three independent A2A agent servers

Multi-step coordination loops

Isolation of reasoning vs. execution

Clean message-based interfaces

Notebook demonstrating behavior

The simple scenario (direct customer lookup) runs end-to-end.
More complex multi-step scenarios highlight the difficulty of keeping the Router consistently forwarding intermediate results — an expected challenge of LLM-driven orchestration.

Maintains the multi-turn loop until the Support Agent produces a final answer.

Uses only plain text to communicate (to avoid unintended tool calls).
