# Multi-Agent Customer Support System (A2A + MCP)

This project implements a multi-agent customer support system using:

- Google ADK for agent-to-agent (A2A) communication
- FastMCP for Model Context Protocol tool integration
- Gemini models for reasoning and routing
- SQLite as a persistent backend
- Custom MCP tools for database operations

The system demonstrates structured multi-agent coordination, multi-step reasoning, 
and tool-calling through a clean JSON-based protocol.

# Overview

The architecture includes three independent agents:

1. Router Agent  
   - Classifies user intent  
   - Routes tasks to Support or Data agents  
   - Coordinates multi-step flows  

2. Support Agent  
   - Handles reasoning, negotiation, and escalation  
   - Determines when more data is needed  
   - Produces final user-facing responses  

3. Customer Data Agent  
   - Executes DB queries via MCP tools  
   - Never generates natural language  
   - Returns structured JSON outputs only  

An MCP server (FastMCP) exposes database tools:
- get_customer
- list_customers
- update_customer
- create_ticket
- get_customer_history

# Project Structure

MultiAgentA2A/
│
├── a2a_runtime/
│   └── run_query.py
│
├── agents/
│   ├── customer_data_agent.py
│   ├── support_agent.py
│   └── router_agent.py
│
├── client/
│   ├── all_server.py
│   └── simpleClient.py
│
├── configuration/
│   ├── config.py
│   └── logging_config.py
│
├── Data/
│   └── database_setup.py
│
├── mcp_server/
│   ├── mcp_server.py
│   └── database_setup.py
│
├── notebook/
│   └── Multi_Agent_HW5.ipynb
│
├── tests/
│   ├── test_manual_agent_flow.py
│   └── test_pipeline.py
│
└── requirements.txt

# Installation

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Running the MCP Server

python mcp_server/mcp_server.py

# Running All A2A Agents

python client/all_server.py

# Running Tests

# Manual multi-agent step-by-step:
python tests/test_manual_agent_flow.py

# Full pipeline tests:
python tests/test_pipeline.py

# Running a Query (via pipeline)

from a2a_runtime.run_query import run_query
import asyncio

asyncio.run(run_query("Get customer information for ID 5"))

# Example Queries

"Get customer information for ID 5"
"I'm customer 3 and need help upgrading my account"
"I've been charged twice — please refund immediately"
"Show me all active customers who have open tickets"

# Notes

The system emphasizes:
- Stable multi-step A2A routing
- Deterministic tool usage through MCPToolset
- Clear separation of reasoning and data access
- Structured JSON state propagation

The Jupyter notebook demonstrates the full setup and execution flow, including 
database initialization, MCP server setup, and multi-agent coordination.
