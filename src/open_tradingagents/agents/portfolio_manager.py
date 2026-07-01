"""Portfolio manager — the final gate.

Approves or rejects the risk-adjusted trade and emits the final call. Its output
format is governed by the ``trade_report`` skill (editable Markdown), not code.
"""
from __future__ import annotations

from langgraph.graph import END
from langgraph.types import Command

from ..config import get_llm
from ..prompts import PORTFOLIO_MANAGER_PROMPT
from ..skills import load_skill


def portfolio_manager(state) -> Command:
    final = get_llm("deep_think").invoke(
        PORTFOLIO_MANAGER_PROMPT.format(
            ticker=state["ticker"],
            skill=load_skill("trade_report"),
            risk_decision=state["risk_debate"]["judge_decision"],
            plan=state["investment_plan"],
        )
    ).content
    return Command(goto=END, update={"final_decision": final})
