import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# ============================================================
# API KEYS
# ============================================================

try:
    OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
    TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]
except Exception:
    load_dotenv()

    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


# ============================================================
# OPENROUTER
# ============================================================

BASE_URL = "https://openrouter.ai/api/v1"

# Models are tried in this order.
#
# The first successful model is used.
#
# Finance-specific model is placed first because this is a
# Gold Market Agent.
#
# GLM 5.2 is a general reasoning model and is useful as a
# strong fallback.
#
# Ling 3.0 Flash VL is useful as another general/reasoning
# fallback and additionally supports vision.
#
# The remaining models provide additional fallback capacity.

MODELS = [
    "inclusionai/ling-3.0-flash-fin:free",
    "z-ai/glm-5.2:free",
    "inclusionai/ling-3.0-flash-vl:free",

    # Existing fallback models
    "google/gemma-4-26b-a4b-it:free",
    "google/gemma-4-31b-it:free",
    "qwen/qwen3.8-27b:free",

    # Additional fallback models
    "nvidia/nemotron-3.5-lightning:free",
    "nex-agi/nex-n2.5-mini:free",
    "liquid/lfm-2.5-2.6b:free",
]

# Backwards compatibility.
# If another part of the project imports MODEL_NAME,
# it will still work.
MODEL_NAME = MODELS[0]

ENABLE_REASONING = True


# ============================================================
# FALLBACK / RETRY SETTINGS
# ============================================================

# Number of times to retry the SAME model after a temporary
# rate-limit/server error before moving to the next model.
MAX_RETRIES_PER_MODEL = 2

# Default delay between retries when OpenRouter does not
# provide a Retry-After value.
RETRY_DELAY_SECONDS = 3

# Maximum delay we will wait because of Retry-After.
MAX_RETRY_DELAY_SECONDS = 30

# When a model receives a 429, temporarily avoid it.
# This prevents every request from immediately hitting the
# same exhausted free endpoint again.
MODEL_COOLDOWN_SECONDS = 60


# ============================================================
# NEWS
# ============================================================

MAX_NEWS_RESULTS = 5


# ============================================================
# MARKET SYMBOLS
# ============================================================

GOLD_SYMBOL = "GC=F"
DXY_SYMBOL = "DX-Y.NYB"
SILVER_SYMBOL = "SI=F"
OIL_SYMBOL = "CL=F"


# ============================================================
# LANGUAGES
# ============================================================

SUPPORTED_LANGUAGES = ["English", "Persian"]


# ============================================================
# DISCLAIMER
# ============================================================

DISCLAIMER = (
    "This analysis is generated using real-time market data and "
    "recent news. It is intended for informational purposes only "
    "and should not be considered financial advice."
)