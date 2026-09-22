import yfinance as yf

from config import (
    GOLD_SYMBOL,
    DXY_SYMBOL,
    SILVER_SYMBOL,
    OIL_SYMBOL,
)


def get_asset_data(symbol):
    """
    Fetch current price, daily percentage change,
    and weekly percentage change for an asset.
    """

    try:
        ticker = yf.Ticker(symbol)

        # Fetch approximately one week of market data
        history = ticker.history(period="7d", auto_adjust=False)

        if history.empty:
            raise ValueError(f"No data returned for {symbol}")

        # Remove rows where Close is missing
        close_prices = history["Close"].dropna()

        if close_prices.empty:
            raise ValueError(f"No closing prices returned for {symbol}")

        # Current/latest price
        current_price = float(close_prices.iloc[-1])

        # ---------------------------------------------------------
        # Daily change
        # ---------------------------------------------------------
        if len(close_prices) >= 2:
            previous_close = float(close_prices.iloc[-2])

            if previous_close != 0:
                daily_change = (
                    (current_price - previous_close)
                    / previous_close
                ) * 100
            else:
                daily_change = None
        else:
            daily_change = None

        # ---------------------------------------------------------
        # Weekly change
        # ---------------------------------------------------------
        if len(close_prices) >= 2:
            first_close = float(close_prices.iloc[0])

            if first_close != 0:
                weekly_change = (
                    (current_price - first_close)
                    / first_close
                ) * 100
            else:
                weekly_change = None
        else:
            weekly_change = None

        return {
            "price": round(current_price, 2),
            "daily_change_percent": (
                round(daily_change, 2)
                if daily_change is not None
                else None
            ),
            "weekly_change_percent": (
                round(weekly_change, 2)
                if weekly_change is not None
                else None
            ),
            "error": None,
        }

    except Exception as e:
        return {
            "price": None,
            "daily_change_percent": None,
            "weekly_change_percent": None,
            "error": str(e),
        }


def get_market_data():
    """
    Fetch all market indicators.
    """

    return {
        "gold": get_asset_data(GOLD_SYMBOL),
        "dxy": get_asset_data(DXY_SYMBOL),
        "silver": get_asset_data(SILVER_SYMBOL),
        "oil": get_asset_data(OIL_SYMBOL),
    }


if __name__ == "__main__":

    data = get_market_data()

    print("\n===== Market Data =====\n")

    for asset_name, asset_data in data.items():

        print(asset_name.upper())

        print(f"Price: {asset_data['price']}")

        print(
            f"Daily Change (%): "
            f"{asset_data['daily_change_percent']}"
        )

        print(
            f"Weekly Change (%): "
            f"{asset_data['weekly_change_percent']}"
        )

        if asset_data.get("error"):
            print(f"Error: {asset_data['error']}")

        print("-" * 30)
