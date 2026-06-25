import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables from .env
load_dotenv()


# API Keys

# Streamlit Cloud secrets support
try:
    import streamlit as st
    OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
    TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]

except Exception:
    # local fallback
    from dotenv import load_dotenv
    load_dotenv()

    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")



# OpenRouter Settings

BASE_URL = "https://openrouter.ai/api/v1"

MODEL_NAME = "openai/gpt-oss-120b:free"

ENABLE_REASONING = True


# News Settings

MAX_NEWS_RESULTS = 5


# Finance Symbols

GOLD_SYMBOL = "GC=F"       # Gold Futures
DXY_SYMBOL = "DX-Y.NYB"   # US Dollar Index
SILVER_SYMBOL = "SI=F"    # Silver Futures
OIL_SYMBOL = "CL=F"       # Crude Oil Futures


# Language Settings

SUPPORTED_LANGUAGES = [
    "English",
    "Persian"
]


# Disclaimer

DISCLAIMER = (
    "This analysis is generated using real-time market data and "
    "recent news. It is intended for informational purposes only "
    "and should not be considered financial advice."
)

BASE_URL = "https://openrouter.ai/api/v1"

MODEL_NAME = "openai/gpt-oss-120b:free"

ENABLE_REASONING = True