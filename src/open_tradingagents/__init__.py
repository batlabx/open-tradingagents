"""Open-TradingAgents — an open-source rewrite of TauricResearch/TradingAgents.

A multi-agent "trading firm" (analysts -> bull/bear research debate -> trader ->
risk debate -> portfolio manager) built on LangGraph, with every paid data feed
and cloud model swapped for a free / local one:

    GPT / Claude        -> Ollama (Qwen2.5 / Llama-3.1)
    FinnHub / SimFin    -> yfinance (keyless prices + fundamentals)
    Google News API     -> Google News RSS (feedparser)
    Reddit API          -> news-derived sentiment (no key)
    StockStats          -> StockStats / pandas-ta (already open)

⚠️  EDUCATIONAL / RESEARCH SOFTWARE ONLY. This is a reference architecture for
studying multi-agent systems. It is NOT investment advice and must not be used
to make real trading decisions. See the disclaimer in the README.
"""
__version__ = "0.1.0"
