"""MCP server: get_technicals — standard technical indicators.

Open-source swap: the original already uses StockStats (open); we keep it and add
a pandas-ta path. Indicators are computed from keyless yfinance prices. A TOOL:
deterministic transform of fetched data into a typed result.
"""
from __future__ import annotations

import yfinance as yf
from mcp.server.fastmcp import FastMCP
from stockstats import StockDataFrame

mcp = FastMCP("open-tradingagents-technicals")


@mcp.tool()
def get_technicals(ticker: str, lookback_days: int = 180) -> dict:
    """Return RSI, MACD, and moving averages for `ticker`."""
    hist = yf.Ticker(ticker).history(period=f"{lookback_days}d")
    if hist.empty:
        return {"ticker": ticker, "error": "no data"}

    sdf = StockDataFrame.retype(hist.reset_index())
    # Referencing a column triggers stockstats to compute it.
    rsi = float(sdf["rsi_14"].iloc[-1])
    macd = float(sdf["macd"].iloc[-1])
    macd_signal = float(sdf["macds"].iloc[-1])
    sma_20 = float(sdf["close_20_sma"].iloc[-1])
    sma_50 = float(sdf["close_50_sma"].iloc[-1])
    last = float(hist["Close"].iloc[-1])

    return {
        "ticker": ticker,
        "rsi_14": round(rsi, 1),
        "macd": round(macd, 3),
        "macd_signal": round(macd_signal, 3),
        "sma_20": round(sma_20, 2),
        "sma_50": round(sma_50, 2),
        "price_vs_sma50": "above" if last > sma_50 else "below",
    }


if __name__ == "__main__":
    mcp.run()
