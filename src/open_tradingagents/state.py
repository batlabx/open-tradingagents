"""Shared graph state for the trading firm.

Two nested debate records (investment + risk) carry the running transcripts and
a round counter, so the debate nodes can loop until a cap is hit and then hand
off to their judge.
"""
from __future__ import annotations

from typing import Annotated, TypedDict

from langgraph.graph.message import add_messages


class InvestDebate(TypedDict):
    bull_history: str      # everything the bull has argued
    bear_history: str      # everything the bear has argued
    rounds: int            # completed bull+bear exchanges
    judge_decision: str    # the research manager's ruling


class RiskDebate(TypedDict):
    risky_history: str
    safe_history: str
    neutral_history: str
    rounds: int
    judge_decision: str    # the risk manager's ruling


class TradingState(TypedDict):
    ticker: str
    trade_date: str
    reports: dict                              # one entry per analyst
    invest_debate: InvestDebate
    investment_plan: str                       # research manager's output
    trader_proposal: str                       # trader's draft
    risk_debate: RiskDebate
    final_decision: str                        # portfolio manager's output
    messages: Annotated[list, add_messages]
