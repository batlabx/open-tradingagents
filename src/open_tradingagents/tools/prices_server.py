"""MCP server: get_prices — OHLCV price history.

Open-source swap: the original pulls from FinnHub / Yahoo behind API keys. We
use `yfinance`, which is keyless. A TOOL because it is a network call with a
typed, verifiable result (a price series).
"""
from __future__ import annotations

import yfinance as yf
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("open-tradingagents-prices")


@mcp.tool()
def get_prices(ticker: str, lookback_days: int = 180) -> dict:
    """Return a compact price summary for `ticker` over the lookback window."""
    hist = yf.Ticker(ticker).history(period=f"{lookback_days}d")
    if hist.empty:
        return {"ticker": ticker, "error": "no data"}

    close = hist["Close"]
    last = float(close.iloc[-1])
    first = float(close.iloc[0])
    return {
        "ticker": ticker,
        "last_close": round(last, 2),
        "pct_change_window": round((last / first - 1) * 100, 2),
        "period_high": round(float(hist["High"].max()), 2),
        "period_low": round(float(hist["Low"].min()), 2),
        "avg_volume": int(hist["Volume"].mean()),
        "last_5_closes": [round(float(x), 2) for x in close.tail(5)],
    }


if __name__ == "__main__":
    mcp.run()
