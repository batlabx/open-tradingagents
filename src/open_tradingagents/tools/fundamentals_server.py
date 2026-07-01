"""MCP server: get_fundamentals — valuation, growth, and balance-sheet health.

Open-source swap: replaces SimFin / FinnHub fundamentals (keyed) with yfinance's
free `.info`. A TOOL: network call, typed result.
"""
from __future__ import annotations

import yfinance as yf
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("open-tradingagents-fundamentals")


@mcp.tool()
def get_fundamentals(ticker: str) -> dict:
    """Return key fundamental metrics for `ticker`."""
    info = yf.Ticker(ticker).info
    keys = {
        "sector": "sector",
        "trailing_pe": "trailingPE",
        "forward_pe": "forwardPE",
        "price_to_book": "priceToBook",
        "profit_margin": "profitMargins",
        "revenue_growth": "revenueGrowth",
        "debt_to_equity": "debtToEquity",
        "return_on_equity": "returnOnEquity",
        "market_cap": "marketCap",
    }
    out = {out_key: info.get(src) for out_key, src in keys.items()}
    out["ticker"] = ticker
    out["name"] = info.get("shortName", ticker)
    return out


if __name__ == "__main__":
    mcp.run()
