# ============================================================
# PHASE 6 — SIMPLE A2A CLIENT + CLEAN OUTPUT EXTRACTION
# ============================================================
from configuration.logging_config import setup_logging

import httpx
import json
from a2a.utils.constants import AGENT_CARD_WELL_KNOWN_PATH
from a2a.client import ClientConfig, ClientFactory, create_text_message_object
from a2a.types import AgentCard, TransportProtocol


# -----------------------------------------------------------
# Helper: Extract structuredContent from ADK task output
# -----------------------------------------------------------
def extract_structured(task):
    """
    Universal extractor for Router, DataAgent, SupportAgent
    Handles:
    - .root.data (DataAgent structured)
    - .root.text containing JSON
    - plain text fallback
    """
    try:
        art = task.artifacts[0]
        part = art.parts[0]
        root = part.root

        # ----------------------------------------------------
        # 1) Case: DataAgent structuredContent
        # ----------------------------------------------------
        if hasattr(root, "data") and isinstance(root.data, dict):
            data = root.data
            if (
                "response" in data
                and isinstance(data["response"], dict)
                and "structuredContent" in data["response"]
            ):
                return data["response"]["structuredContent"]

            # Router sometimes returns dict in .data
            return data

        # ----------------------------------------------------
        # 2) Case: Router/Support: text containing JSON
        # ----------------------------------------------------
        if hasattr(root, "text") and isinstance(root.text, str):
            text = root.text.strip()

            # Remove ```json fences
            if text.startswith("```"):
                text = text.strip("`")
                if text.startswith("json"):
                    text = text[4:].strip()

            # Try JSON decode
            try:
                return json.loads(text)
            except Exception:
                return text  # plain text fallback

    except Exception:
        pass

    return None



# -----------------------------------------------------------
# A2ASimpleClient — fully corrected version
# -----------------------------------------------------------
class A2ASimpleClient:
    def __init__(self, default_timeout: float = 240.0):
        self._agent_info_cache = {}
        self.default_timeout = default_timeout

    async def create_task(self, agent_url: str, message, clean=True):
        """
        agent_url : http://127.0.0.1:PORT
        message   : str OR dict
        clean     : if True, returns structured JSON instead of ADK dump
        """

        timeout_config = httpx.Timeout(
            timeout=self.default_timeout,
            connect=10.0,
            read=self.default_timeout,
            write=10.0,
            pool=5.0,
        )

        async with httpx.AsyncClient(timeout=timeout_config) as httpx_client:

            # ---------------------------
            # Load AgentCard (cached)
            # ---------------------------
            if agent_url not in self._agent_info_cache:
                card_resp = await httpx_client.get(
                    f"{agent_url}{AGENT_CARD_WELL_KNOWN_PATH}"
                )
                self._agent_info_cache[agent_url] = card_resp.json()

            agent_card = AgentCard(**self._agent_info_cache[agent_url])

            # ---------------------------
            # Create A2A client
            # ---------------------------
            config = ClientConfig(
                httpx_client=httpx_client,
                supported_transports=[
                    TransportProtocol.jsonrpc,
                    TransportProtocol.http_json,
                ],
                use_client_preference=True,
            )

            client = ClientFactory(config).create(agent_card)

            # Convert dict → JSON string
            if isinstance(message, dict):
                message = json.dumps(message)

            msg = create_text_message_object(content=message)

            # ---------------------------
            # Send message
            # ---------------------------
            responses = []
            async for response in client.send_message(msg):
                responses.append(response)

            if not responses or not isinstance(responses[0], tuple):
                return "No response received"

            task = responses[0][0]

            # ---------------------------
            # Clean extraction (preferred)
            # ---------------------------
            if clean:
                cleaned = extract_structured(task)
                return cleaned if cleaned is not None else str(task)

            # ---------------------------
            # Raw fallback
            # ---------------------------
            return str(task)


# GLOBAL CLIENT INSTANCE
a2a_client = A2ASimpleClient()
