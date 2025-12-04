import google.adk.tools.mcp_tool.mcp_toolset
import google.adk.tools.mcp_tool
import google.adk.tools.mcp_tool.mcp_session_manager

#Run this to install necessary packages
#%pip install --upgrade -q google-adk google-genai a2a-sdk==0.3.0 python-dotenv aiohttp uvicorn requests mermaid-python nest-asyncio

# Targeted workaround for google-adk==1.9.0 compatibility with a2a-sdk==0.3.0
# This cell shall be removed when google-adk releases the version next to >1.9.0
# (after https://github.com/google/adk-python/pull/2297)


import sys

from a2a.client import client as real_client_module
from a2a.client.card_resolver import A2ACardResolver


class PatchedClientModule:
    def __init__(self, real_module) -> None:
        for attr in dir(real_module):
            if not attr.startswith('_'):
                setattr(self, attr, getattr(real_module, attr))
        self.A2ACardResolver = A2ACardResolver


patched_module = PatchedClientModule(real_client_module)
sys.modules['a2a.client.client'] = patched_module  # type: ignore


import asyncio
import logging
import os
import sys
import threading
import time

from typing import Any

import httpx
import nest_asyncio
import uvicorn

from a2a.client import ClientConfig, ClientFactory, create_text_message_object
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
    TransportProtocol,
)
from a2a.utils.constants import AGENT_CARD_WELL_KNOWN_PATH
from dotenv import load_dotenv
from google.adk.a2a.executor.a2a_agent_executor import (
    A2aAgentExecutor,
    A2aAgentExecutorConfig,
)
from google.adk.agents import Agent, SequentialAgent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search

from mcp import types as mcp_types
from mcp.server.lowlevel import Server
from mcp.server.models import InitializationOptions

from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.mcp_tool.conversion_utils import adk_to_mcp_tool_type

# Set Google Cloud Configuration
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"      # use Generative AI API, not Vertex endpoint
os.environ["GOOGLE_CLOUD_PROJECT"] = "multiagenta2a"   # <-- your project id here, NO brackets
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"    # same as in the notes

load_dotenv()
from google.colab import userdata

os.environ['GOOGLE_API_KEY'] = userdata.get('GOOGLE_API_KEY')

print('Environment variables configured:')
print(f'GOOGLE_GENAI_USE_VERTEXAI: {os.environ["GOOGLE_GENAI_USE_VERTEXAI"]}')
print(f'GOOGLE_CLOUD_PROJECT: {os.environ["GOOGLE_CLOUD_PROJECT"]}')
print(f'GOOGLE_CLOUD_LOCATION: {os.environ["GOOGLE_CLOUD_LOCATION"]}')

# Authenticate your notebook environment (Colab only)
if 'google.colab' in sys.modules:
    from google.colab import auth

    auth.authenticate_user(project_id=os.environ['GOOGLE_CLOUD_PROJECT'])

LOG_LEVEL = "warning"

# Install fastmcp
#!pip install fastmcp