"""CLI entry point.

    python -m open_tradingagents.main NVDA --date 2026-01-15

Runs the full firm and prints the final call. State is checkpointed in memory;
swap MemorySaver for SqliteSaver to get the original's resume-after-crash.

⚠️  EDUCATIONAL / RESEARCH ONLY — NOT INVESTMENT ADVICE. The "decision" is an
illustration of multi-agent reasoning, not a recommendation to trade anything.
"""
from __future__ import annotations

import argparse
import datetime as dt

from langgraph.checkpoint.memory import MemorySaver

from .graph import build_graph

DISCLAIMER = (
    "\n⚠️  EDUCATIONAL / RESEARCH ONLY — NOT INVESTMENT ADVICE.\n"
    "    Do not use this output to make real trading decisions.\n"
)


def _initial_state(ticker: str, date: str) -> dict:
    empty_invest = {"bull_history": "", "bear_history": "", "rounds": 0,
                    "judge_decision": ""}
    empty_risk = {"risky_history": "", "safe_history": "", "neutral_history": "",
                  "rounds": 0, "judge_decision": ""}
    return {
        "ticker": ticker.upper(),
        "trade_date": date,
        "reports": {},
        "invest_debate": empty_invest,
        "investment_plan": "",
        "trader_proposal": "",
        "risk_debate": empty_risk,
        "final_decision": "",
        "messages": [],
    }


def run(ticker: str, date: str) -> str:
    print(DISCLAIMER)
    graph = build_graph(MemorySaver())
    cfg = {"configurable": {"thread_id": f"{ticker}-{date}"}}

    for event in graph.stream(_initial_state(ticker, date), cfg):
        print("·", next(iter(event)))

    final = graph.get_state(cfg).values["final_decision"]
    print("\n===== FINAL CALL (illustrative only) =====\n")
    print(final)
    print(DISCLAIMER)
    return final


def main() -> None:
    ap = argparse.ArgumentParser(description="Open-TradingAgents (educational)")
    ap.add_argument("ticker", help="e.g. NVDA")
    ap.add_argument("--date", default=dt.date.today().isoformat(),
                    help="as-of date YYYY-MM-DD (default: today)")
    args = ap.parse_args()
    run(args.ticker, args.date)


if __name__ == "__main__":
    main()
