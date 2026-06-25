import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import yfinance as yf

from agent import GoldMarketAgent
from market_data import get_asset_data
from config import GOLD_SYMBOL
from database import (
    create_database,
    save_chat,
    get_chat_history,
    clear_history
)


create_database()


st.set_page_config(page_title="Gold AI Agent", layout="wide")

st.title("🪙 Gold Market AI Agent")


# Initialize Agent
if "agent" not in st.session_state:
    st.session_state.agent = GoldMarketAgent()

if "chat" not in st.session_state:
    st.session_state.chat = []


# Sidebar - Gold Chart
st.sidebar.header("📊 Gold Price Chart")

gold = yf.Ticker(GOLD_SYMBOL)

data = gold.history(period="1mo")

current_price = round(data["Close"].iloc[-1], 2)

daily_change = round(
    (
        (data["Close"].iloc[-1] - data["Close"].iloc[-2])
        / data["Close"].iloc[-2]
    ) * 100,
    2
)

st.sidebar.metric(
    "Gold Price",
    f"${current_price}",
    f"{daily_change}%"
)

def plot_gold():

    data = yf.Ticker(GOLD_SYMBOL).history(period="3mo")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Close"],
            mode="lines",
            name="Gold Price"
        )
    )

    fig.update_layout(
        title="Gold Price (Last 3 Months)",
        xaxis_title="Date",
        yaxis_title="USD",
        height=450
    )

    st.sidebar.plotly_chart(
        fig,
        use_container_width=True
    )


plot_gold()


# Chat Input
user_input = st.text_input("Ask your question about gold:")


if user_input:

    with st.spinner("Analyzing market..."):

        response = st.session_state.agent.run(user_input)

        save_chat(
            user_input,
            response
        )

        # Save chat
        st.session_state.chat.append((user_input, response))


# Chat History Display
st.subheader("💬 Chat History")

history = get_chat_history()

for user, assistant, timestamp in history:

    st.markdown(
        f"**🕒 {timestamp}**"
    )

    st.markdown(
        f"**You:** {user}"
    )

    st.markdown(
        f"**AI:** {assistant}"
    )

    st.markdown("---")


if st.sidebar.button("🗑️ Clear History"):

    clear_history()

    st.rerun()