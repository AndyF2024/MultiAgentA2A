# ============================================================
# PHASE 5 — A2A SERVERS FOR ALL 3 AGENTS
# ============================================================

from configuration.logging_config import setup_logging

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.a2a.executor.a2a_agent_executor import (
    A2aAgentExecutor,
    A2aAgentExecutorConfig,
)
import uvicorn
import nest_asyncio
nest_asyncio.apply()

def create_agent_a2a_server(agent, agent_card):
    runner = Runner(
        app_name=agent.name,
        agent=agent,
        artifact_service=InMemoryArtifactService(),
        session_service=InMemorySessionService(),
        memory_service=InMemoryMemoryService(),
    )
    executor = A2aAgentExecutor(
        runner=runner,
        config=A2aAgentExecutorConfig(),
    )
    request_handler = DefaultRequestHandler(
        agent_executor=executor,
        task_store=InMemoryTaskStore(),
    )
    return A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler,
    )

async def run_customer_data_server():
    app = create_agent_a2a_server(customer_data_agent, customer_data_agent_card)
    config = uvicorn.Config(app.build(), host="127.0.0.1", port=10030, log_level="warning", loop="none")
    server = uvicorn.Server(config)
    await server.serve()

async def run_support_agent_server():
    app = create_agent_a2a_server(support_agent, support_agent_card)
    config = uvicorn.Config(app.build(), host="127.0.0.1", port=10031, log_level="warning", loop="none")
    server = uvicorn.Server(config)
    await server.serve()

async def run_router_agent_server():
    app = create_agent_a2a_server(router_agent, router_agent_card)
    config = uvicorn.Config(app.build(), host="127.0.0.1", port=10032, log_level="warning", loop="none")
    server = uvicorn.Server(config)
    await server.serve()

async def start_all_servers():
    print("Starting all 3 agents...")
    tasks = [
        asyncio.create_task(run_customer_data_server()),
        asyncio.create_task(run_support_agent_server()),
        asyncio.create_task(run_router_agent_server()),
    ]
    await asyncio.sleep(6)
    print("✅ All agent servers started:")
    await asyncio.gather(*tasks)

def run_servers_in_background():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_all_servers())

server_thread = threading.Thread(target=run_servers_in_background, daemon=True)
server_thread.start()

import time
time.sleep(3)
print("All three A2A servers running.")
