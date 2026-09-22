import streamlit as st
import yfinance as yf

from agent import GoldMarketAgent
from market_data import get_market_data
from database import save_chat
from config import GOLD_SYMBOL, DISCLAIMER


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Gold Market AI",
    page_icon="🪙",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main page */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 14px;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.85rem;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.5rem;
    }

    /* Chat messages */
    [data-testid="stChatMessage"] {
        border-radius: 12px;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 8px;
    }

    /* Dividers */
    hr {
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "agent" not in st.session_state:
    st.session_state.agent = GoldMarketAgent()

agent = st.session_state.agent


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def format_price(value):
    """Format a numeric price."""

    if value is None:
        return "—"

    try:
        return f"${float(value):,.2f}"
    except (TypeError, ValueError):
        return "—"


def format_percent(value):
    """Format a percentage with + / - sign."""

    if value is None:
        return "—"

    try:
        value = float(value)
    except (TypeError, ValueError):
        return "—"

    if value > 0:
        return f"+{value:.2f}%"

    return f"{value:.2f}%"


def get_change_color(value):
    """Return a visual indicator for percentage movement."""

    if value is None:
        return "⚪"

    try:
        value = float(value)
    except (TypeError, ValueError):
        return "⚪"

    if value > 0:
        return "🟢"

    if value < 0:
        return "🔴"

    return "⚪"


def detect_detail_mode(question):
    """
    Use the same keywords as agent.py to determine
    whether the response should be detailed.
    """

    detailed_keywords = [
        "analysis",
        "analyze",
        "forecast",
        "outlook",
        "trend",
        "risk",
        "detailed",

        "تحلیل",
        "تحلیل کن",
        "بررسی",
        "چشم انداز",
        "چشم‌انداز",
        "پیش بینی",
        "پیش‌بینی",
        "روند",
        "ریسک",
        "کامل",
    ]

    question_lower = question.lower()

    return any(
        keyword in question_lower
        for keyword in detailed_keywords
    )


def get_asset(market_data, key):
    """Safely retrieve an asset from market data."""

    if not market_data:
        return {}

    asset = market_data.get(key)

    if asset is None:
        asset = market_data.get(key.capitalize())

    if asset is None:
        return {}

    return asset


def render_market_card(label, symbol, data):
    """
    Render one market overview card.
    Uses the exact keys returned by market_data.py.
    """

    if not data:
        st.subheader(label)
        st.metric("Price", "—")
        st.caption("Day: —  •  Week: —")
        return

    price = data.get("price")

    # These are the exact keys from market_data.py
    daily_change = data.get("daily_change_percent")
    weekly_change = data.get("weekly_change_percent")

    day_indicator = get_change_color(daily_change)
    week_indicator = get_change_color(weekly_change)

    day_text = format_percent(daily_change)
    week_text = format_percent(weekly_change)

    st.subheader(label)

    st.metric(
        label="Price",
        value=format_price(price),
    )

    st.caption(
        f"{day_indicator} Day: {day_text}   "
        f"{week_indicator} Week: {week_text}"
    )

    st.caption(symbol)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🪙 Gold Market AI")

    st.caption(
        "AI-powered gold market analysis using "
        "market data, financial indicators, and recent news."
    )

    st.divider()

    st.subheader("Controls")

    if st.button(
        "🔄 Refresh market data",
        use_container_width=True,
    ):
        st.rerun()

    if st.button(
        "🗑️ Clear conversation",
        use_container_width=True,
    ):
        agent.clear_history()
        st.rerun()

    st.divider()

    st.subheader("Response modes")

    st.info(
        "The agent automatically chooses between "
        "Simple and Detailed mode based on your question."
    )

    st.caption(
        "Try words such as "
        "'analysis', 'forecast', 'risk', or "
        "'detailed' for a deeper response."
    )

    st.caption(
        "Persian keywords such as "
        "'تحلیل', 'پیش‌بینی', 'ریسک', and "
        "'کامل' also activate Detailed mode."
    )


# ============================================================
# HEADER
# ============================================================

st.title("Gold Market AI")

st.caption(
    "Real-time market data • Financial news • AI analysis"
)

st.success(
    "Live market data connected"
)


# ============================================================
# MARKET DATA
# ============================================================

with st.spinner("Loading market data..."):
    market_data = get_market_data()


# ============================================================
# MARKET OVERVIEW
# ============================================================

st.divider()

st.subheader("Market Overview")

st.caption(
    "Current prices and recent percentage movements"
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    gold = get_asset(market_data, "gold")

    render_market_card(
        "Gold",
        GOLD_SYMBOL,
        gold,
    )

with col2:
    dxy = get_asset(market_data, "dxy")

    render_market_card(
        "US Dollar Index",
        "DX-Y.NYB",
        dxy,
    )

with col3:
    silver = get_asset(market_data, "silver")

    render_market_card(
        "Silver",
        "SI=F",
        silver,
    )

with col4:
    oil = get_asset(market_data, "oil")

    render_market_card(
        "Crude Oil",
        "CL=F",
        oil,
    )


# ============================================================
# GOLD PRICE CHART
# ============================================================

st.divider()

st.subheader("Gold Price")

chart_col, info_col = st.columns(
    [3, 1]
)

with chart_col:

    chart_period = st.selectbox(
        "Chart period",
        options=[
            "7d",
            "1mo",
            "3mo",
            "6mo",
            "1y",
        ],
        index=0,
    )

    try:

        ticker = yf.Ticker(GOLD_SYMBOL)

        chart_data = ticker.history(
            period=chart_period,
            auto_adjust=False,
        )

        if not chart_data.empty:

            st.line_chart(
                chart_data["Close"],
                height=400,
            )

        else:

            st.warning(
                "No chart data is currently available."
            )

    except Exception as e:

        st.warning(
            f"Unable to load the gold chart: {e}"
        )


with info_col:

    st.subheader("Gold")

    gold_price = gold.get("price")

    st.metric(
        "Current price",
        format_price(gold_price),
    )

    gold_day = gold.get(
        "daily_change_percent"
    )

    gold_week = gold.get(
        "weekly_change_percent"
    )

    st.metric(
        "Daily",
        format_percent(gold_day),
    )

    st.metric(
        "Weekly",
        format_percent(gold_week),
    )

    st.caption(
        f"Yahoo Finance symbol: {GOLD_SYMBOL}"
    )


# ============================================================
# AI ANALYST
# ============================================================

st.divider()

st.subheader("AI Market Analyst")

st.caption(
    "Ask about gold prices, market trends, news, "
    "economic factors, or risk."
)


# ============================================================
# ADAPTIVE MODE EXPLANATION
# ============================================================

with st.expander(
    "✦ How response mode works",
    expanded=False,
):

    st.write(
        "The agent automatically adapts the response "
        "depth to your question."
    )

    st.write(
        "Simple mode: short, direct answers for "
        "straightforward questions."
    )

    st.write(
        "Detailed mode: deeper analysis when you ask "
        "for analysis, forecasts, trends, risks, "
        "or a detailed explanation."
    )


# ============================================================
# CHAT INPUT
# ============================================================

question = st.chat_input(
    "Ask about the gold market..."
)


# ============================================================
# NEW QUESTION
# ============================================================

if question:

    # Display user message
    with st.chat_message("user"):
        st.write(question)

    # Detect response mode
    detailed_mode = detect_detail_mode(question)

    if detailed_mode:
        mode_name = "Detailed analysis"
        mode_icon = "🔎"
    else:
        mode_name = "Simple response"
        mode_icon = "💬"

    st.caption(
        f"{mode_icon} Response mode: {mode_name}"
    )

    # Run agent
    with st.chat_message("assistant"):

        with st.spinner(
            "Analyzing market data and recent news..."
        ):

            response = agent.run(question)

        st.markdown(response)

    # Save conversation
    try:

        save_chat(
            question,
            response,
        )

    except Exception as e:

        # Do not interrupt the user experience
        # if database saving fails.
        st.caption(
            f"Conversation could not be saved: {e}"
        )


# ============================================================
# PREVIOUS CONVERSATION
# ============================================================

history = agent.get_history()

if history:

    st.divider()

    st.subheader("Conversation")

    # Exclude the latest question/answer because
    # they have already been rendered above.
    previous_messages = history[:-2]

    for message in previous_messages:

        role = message.get("role")
        content = message.get("content", "")

        if role == "user":

            with st.chat_message("user"):
                st.write(content)

        elif role == "assistant":

            with st.chat_message("assistant"):
                st.markdown(content)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(DISCLAIMER)

