import yfinance as yf

from config import (
    GOLD_SYMBOL,
    DXY_SYMBOL,
    SILVER_SYMBOL,
    OIL_SYMBOL
)


def get_asset_data(symbol):
    """
    Fetch current price, daily change, and weekly change for an asset.
    """

    try:
        ticker = yf.Ticker(symbol)

        # Last 7 days
        history = ticker.history(period="7d")

        if history.empty:
            raise ValueError(f"No data returned for {symbol}")

        current_price = round(float(history["Close"].iloc[-1]), 2)

        # Daily change
        if len(history) >= 2:
            previous_close = history["Close"].iloc[-2]
            daily_change = round(
                ((current_price - previous_close) / previous_close) * 100,
                2
            )
        else:
            daily_change = 0.0

        # Weekly change
        first_close = history["Close"].iloc[0]

        weekly_change = round(
            ((current_price - first_close) / first_close) * 100,
            2
        )

        return {
            "price": current_price,
            "daily_change_percent": daily_change,
            "weekly_change_percent": weekly_change
        }

    except Exception as e:

        return {
            "price": None,
            "daily_change_percent": None,
            "weekly_change_percent": None,
            "error": str(e)
        }


def get_market_data():
    """
    Fetch all market indicators.
    """

    return {
        "gold": get_asset_data(GOLD_SYMBOL),
        "dxy": get_asset_data(DXY_SYMBOL),
        "silver": get_asset_data(SILVER_SYMBOL),
        "oil": get_asset_data(OIL_SYMBOL)
    }


if __name__ == "__main__":

    data = get_market_data()

    print("\n===== Market Data =====\n")

    for asset_name, asset_data in data.items():

        print(asset_name.upper())

        print(f"Price: {asset_data['price']}")
        print(f"Daily Change (%): {asset_data['daily_change_percent']}")
        print(f"Weekly Change (%): {asset_data['weekly_change_percent']}")

        print("-" * 30)