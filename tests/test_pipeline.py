# ============================================================
# Pipeline End-to-End Tests
# ============================================================

import asyncio

from a2a_runtime.run_query import run_query


async def test_pipeline_simple():
    print("\n=== PIPELINE TEST: SIMPLE ===")
    query = "Get customer information for ID 5"
    answer = await run_query(query)
    print("Final Answer:", answer)


async def test_pipeline_negotiation():
    print("\n=== PIPELINE TEST: NEGOTIATION ===")
    query = "I'm customer 5 and need help upgrading my account"
    answer = await run_query(query)
    print("Final Answer:", answer)


async def test_pipeline_emergency():
    print("\n=== PIPELINE TEST: EMERGENCY ===")
    query = "I've been charged twice, please refund immediately!"
    answer = await run_query(query)
    print("Final Answer:", answer)


async def test_pipeline_multi_step():
    print("\n=== PIPELINE TEST: MULTI-STEP ===")
    query = "Show me all active customers who have open tickets"
    answer = await run_query(query)
    print("Final Answer:", answer)


# ============================================================
# Entry Point
# ============================================================

if __name__ == "__main__":
    asyncio.run(test_pipeline_simple())
    asyncio.run(test_pipeline_negotiation())
    asyncio.run(test_pipeline_emergency())
    asyncio.run(test_pipeline_multi_step())
