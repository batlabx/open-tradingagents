"""Assemble the trading-firm StateGraph.

Analysts run in a fixed sequence (static edges). Everything from the bull
researcher onward routes dynamically via the ``Command(goto=...)`` each node
returns, which is how the two debate loops are expressed.
"""
from __future__ import annotations

import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import START, StateGraph

from .agents.analysts import make_analyst
from .agents.portfolio_manager import portfolio_manager
from .agents.researchers import bear_researcher, bull_researcher, research_manager
from .agents.risk import (neutral_debator, risk_manager, risky_debator,
                          safe_debator)
from .agents.trader import trader
from .state import TradingState

MCP_SERVERS = {
    "prices":       {"command": "python", "args": ["-m", "open_tradingagents.tools.prices_server"],       "transport": "stdio"},
    "fundamentals": {"command": "python", "args": ["-m", "open_tradingagents.tools.fundamentals_server"], "transport": "stdio"},
    "news":         {"command": "python", "args": ["-m", "open_tradingagents.tools.news_server"],         "transport": "stdio"},
    "technicals":   {"command": "python", "args": ["-m", "open_tradingagents.tools.technicals_server"],   "transport": "stdio"},
}


def _load_mcp_tools():
    return asyncio.run(MultiServerMCPClient(MCP_SERVERS).get_tools())


def build_graph(checkpointer=None):
    by = {t.name: t for t in _load_mcp_tools()}

    g = StateGraph(TradingState)

    # 1 · Analyst team (each bound to just the tools it needs)
    g.add_node("market_analyst",       make_analyst("market",       [by["get_prices"], by["get_technicals"]]))
    g.add_node("news_analyst",         make_analyst("news",         [by["get_news"]]))
    g.add_node("fundamentals_analyst", make_analyst("fundamentals", [by["get_fundamentals"]]))
    g.add_node("sentiment_analyst",    make_analyst("sentiment",    [by["get_news"]]))

    # 2 · Research debate  3 · Trader  4 · Risk debate  5 · Portfolio manager
    for name, fn in [
        ("bull_researcher", bull_researcher), ("bear_researcher", bear_researcher),
        ("research_manager", research_manager), ("trader", trader),
        ("risky_debator", risky_debator), ("safe_debator", safe_debator),
        ("neutral_debator", neutral_debator), ("risk_manager", risk_manager),
        ("portfolio_manager", portfolio_manager),
    ]:
        g.add_node(name, fn)

    # Analysts run in sequence; then hand the reports to the research debate.
    g.add_edge(START, "market_analyst")
    g.add_edge("market_analyst", "news_analyst")
    g.add_edge("news_analyst", "fundamentals_analyst")
    g.add_edge("fundamentals_analyst", "sentiment_analyst")
    g.add_edge("sentiment_analyst", "bull_researcher")
    # From here on, routing is dynamic (see each node's Command(goto=...)).

    return g.compile(checkpointer=checkpointer)
