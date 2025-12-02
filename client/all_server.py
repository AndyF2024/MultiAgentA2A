# ============================================================
# PHASE 4 — CREATE A2A SERVERS FOR ALL 3 AGENTS
# (using the SAME pattern as quickstart)
# ============================================================

async def run_customer_data_server():
    app = create_agent_a2a_server(customer_data_agent, customer_data_agent_card)
    config = uvicorn.Config(
        app.build(),
        host="127.0.0.1",
        port=10030,
        log_level="warning",
        loop="none",
    )
    server = uvicorn.Server(config)
    await server.serve()


async def run_support_agent_server():
    app = create_agent_a2a_server(support_agent, support_agent_card)
    config = uvicorn.Config(
        app.build(),
        host="127.0.0.1",
        port=10031,
        log_level="warning",
        loop="none",
    )
    server = uvicorn.Server(config)
    await server.serve()


async def run_router_agent_server():
    app = create_agent_a2a_server(router_agent, router_agent_card)
    config = uvicorn.Config(
        app.build(),
        host="127.0.0.1",
        port=10032,
        log_level="warning",
        loop="none",
    )
    server = uvicorn.Server(config)
    await server.serve()


# ============================================================
#  PHASE 4 — START ALL SERVERS TOGETHER (quickstart pattern)
# ============================================================

async def start_all_servers():
    print("Starting all 3 agents...")

    tasks = [
        asyncio.create_task(run_customer_data_server()),
        asyncio.create_task(run_support_agent_server()),
        asyncio.create_task(run_router_agent_server()),
    ]

    await asyncio.sleep(2)

    print("✅ All agent servers started:")
    print("   - Customer Data Agent: http://127.0.0.1:10030")
    print("   - Support Agent:       http://127.0.0.1:10031")
    print("   - Router Agent:        http://127.0.0.1:10032")

    await asyncio.gather(*tasks)


# ============================================================
# RUN SERVERS IN BACKGROUND THREAD (same as quickstart)
# ============================================================

def run_servers_in_background():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_all_servers())

server_thread = threading.Thread(
    target=run_servers_in_background,
    daemon=True
)
server_thread.start()

time.sleep(3)
print("All three A2A servers running.")
