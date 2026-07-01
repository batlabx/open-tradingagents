"""Trader — turns the research manager's plan into a concrete trade proposal."""
from __future__ import annotations

from langgraph.types import Command

from ..config import get_llm
from ..prompts import TRADER_PROMPT


def trader(state) -> Command:
    proposal = get_llm("deep_think").invoke(
        TRADER_PROMPT.format(ticker=state["ticker"], plan=state["investment_plan"])
    ).content
    return Command(goto="risky_debator", update={"trader_proposal": proposal})
