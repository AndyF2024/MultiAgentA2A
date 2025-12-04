import logging
import warnings

# ======================================================================
#  BASE LOGGING CONFIG — suppress almost everything
# ======================================================================
logging.basicConfig(
    level=logging.CRITICAL,        # CRITICAL = only show catastrophic errors
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

# ======================================================================
#  SILENCE all noisy subsystems (ADK, aiohttp, httpx, jupyter, asyncio)
# ======================================================================
noisy_modules = [
    "google.adk", "google_adk",
    "google.genai", "google_genai",
    "aiohttp", "httpx",
    "anyio", "urllib3",
    "jupyter_client", "asyncio",
    "mcp", "MCPTool"
]

for module in noisy_modules:
    logging.getLogger(module).setLevel(logging.CRITICAL)

# ======================================================================
#  SILENCE Python warnings (Deprecation, Runtime, FutureWarning, etc.)
# ======================================================================
warnings.filterwarnings("ignore")

# EXTRA: reduce asyncio debug noise
logging.getLogger("asyncio").setLevel(logging.CRITICAL)
