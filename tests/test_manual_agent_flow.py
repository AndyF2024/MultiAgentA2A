# ============================================================
# Manual A2A Flow Test (No Pipeline)
# ============================================================

import asyncio

from client.simpleClient import a2a_client
from configuration.config import ROUTER_URL, DATA_URL, SUPPORT_URL


async def test_simple_scenario():
    print("\n=== Manual Test: SIMPLE Scenario ===")

    # 1) Router receives user input
    router_1 = await a2a_client.create_task(
        ROUTER_URL,
        "Get customer information for ID 5"
    )
    print("ROUTER →", router_1)

    # 2) Support interprets request
    support_1 = await a2a_client.create_task(
        SUPPORT_URL,
        router_1
    )
    print("SUPPORT →", support_1)

    # 3) Router translates support_response → task
    router_2 = await a2a_client.create_task(
        ROUTER_URL,
        support_1
    )
    print("ROUTER →", router_2)

    # 4) Data Agent fetches customer info
    data_1 = await a2a_client.create_task(
        DATA_URL,
        router_2
    )
    print("DATA →", data_1)

    # 5) Router passes data back to Support
    router_3 = await a2a_client.create_task(
        ROUTER_URL,
        data_1
    )
    print("ROUTER →", router_3)

    # 6) Support produces final answer
    support_2 = await a2a_client.create_task(
        SUPPORT_URL,
        router_3
    )
    print("SUPPORT →", support_2)

    # 7) Router returns final answer
    router_final = await a2a_client.create_task(
        ROUTER_URL,
        support_2
    )
    print("FINAL ROUTER →", router_final)

    print("\nFinal Answer:", router_final.get("final_answer"))


async def test_negotiation():
    print("\n=== Manual Test: NEGOTIATION Scenario ===")

    msg = "I'm customer 5 and need help upgrading my account"

    router_1 = await a2a_client.create_task(ROUTER_URL, msg)
    print("ROUTER →", router_1)

    support_1 = await a2a_client.create_task(SUPPORT_URL, router_1)
    print("SUPPORT →", support_1)

    router_2 = await a2a_client.create_task(ROUTER_URL, support_1)
    print("ROUTER →", router_2)

    data_1 = await a2a_client.create_task(DATA_URL, router_2)
    print("DATA →", data_1)

    router_3 = await a2a_client.create_task(ROUTER_URL, data_1)
    print("ROUTER →", router_3)

    support_2 = await a2a_client.create_task(SUPPORT_URL, router_3)
    print("SUPPORT →", support_2)

    router_final = await a2a_client.create_task(ROUTER_URL, support_2)
    print("FINAL ROUTER →", router_final)

    print("\nFinal Answer:", router_final.get("final_answer"))


async def test_emergency():
    print("\n=== Manual Test: EMERGENCY Scenario ===")

    msg = "I've been charged twice, please refund immediately!"

    router_1 = await a2a_client.create_task(ROUTER_URL, msg)
    print("ROUTER →", router_1)

    support_1 = await a2a_client.create_task(SUPPORT_URL, router_1)
    print("SUPPORT →", support_1)

    router_final = await a2a_client.create_task(ROUTER_URL, support_1)
    print("FINAL ROUTER →", router_final)

    print("\nFinal Answer:", router_final.get("final_answer"))


async def test_multi_step():
    print("\n=== Manual Test: MULTI-STEP Scenario ===")

    msg = "Show me all active customers who have open tickets"

    router_1 = await a2a_client.create_task(ROUTER_URL, msg)
    print("ROUTER →", router_1)

    support_1 = await a2a_client.create_task(SUPPORT_URL, router_1)
    print("SUPPORT →", support_1)

    router_2 = await a2a_client.create_task(ROUTER_URL, support_1)
    print("ROUTER →", router_2)

    data_1 = await a2a_client.create_task(DATA_URL, router_2)
    print("DATA →", data_1)

    router_3 = await a2a_client.create_task(ROUTER_URL, data_1)
    print("ROUTER →", router_3)

    support_2 = await a2a_client.create_task(SUPPORT_URL, router_3)
    print("SUPPORT →", support_2)

    router_4 = await a2a_client.create_task(ROUTER_URL, support_2)
    print("ROUTER →", router_4)

    data_2 = await a2a_client.create_task(DATA_URL, router_4)
    print("DATA →", data_2)

    router_5 = await a2a_client.create_task(ROUTER_URL, data_2)
    print("ROUTER →", router_5)

    support_3 = await a2a_client.create_task(SUPPORT_URL, router_5)
    print("SUPPORT →", support_3)

    router_final = await a2a_client.create_task(ROUTER_URL, support_3)
    print("FINAL ROUTER →", router_final)

    print("\nFinal Answer:", router_final.get("final_answer"))


# ============================================================
# Entry
# ============================================================

if __name__ == "__main__":
    asyncio.run(test_simple_scenario())
    asyncio.run(test_negotiation())
    asyncio.run(test_emergency())
    asyncio.run(test_multi_step())
