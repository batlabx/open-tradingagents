"""MCP server: get_news — recent headlines from Google News RSS.

Open-source swap: replaces the FinnHub / Google News *API* (keyed) with the
public Google News *RSS* feed parsed by `feedparser` — no key, no quota. A TOOL:
network call with a typed result (a list of headlines).
"""
from __future__ import annotations

import urllib.parse

import feedparser
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("open-tradingagents-news")


@mcp.tool()
def get_news(query: str, max_items: int = 8) -> list[dict]:
    """Return recent news headlines for a ticker or company name."""
    q = urllib.parse.quote(f"{query} stock")
    url = f"https://news.google.com/rss/search?q={q}&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(url)
    return [
        {"title": e.get("title"),
         "published": e.get("published", ""),
         "source": e.get("source", {}).get("title", "") if e.get("source") else "",
         "link": e.get("link")}
        for e in feed.entries[:max_items]
    ]


if __name__ == "__main__":
    mcp.run()
