"""Risk-management team — three stances debate, then a manager rules.

Risky -> Safe -> Neutral, repeating for ``max_risk_rounds`` before the risk
manager issues the risk-adjusted trade. Same debate machinery as the research
team, different personas — again, no new control-flow code.
"""
from __future__ import annotations

from langgraph.types import Command

from ..config import CONFIG, get_llm
from ..prompts import (NEUTRAL_PROMPT, RISK_MANAGER_PROMPT, RISKY_PROMPT,
                       SAFE_PROMPT)


def risky_debator(state) -> Command:
    r = state["risk_debate"]
    text = get_llm("deep_think").invoke(
        RISKY_PROMPT.format(proposal=state["trader_proposal"])
    ).content
    r = {**r, "risky_history": r["risky_history"] + "\n[RISKY] " + text}
    return Command(goto="safe_debator", update={"risk_debate": r})


def safe_debator(state) -> Command:
    r = state["risk_debate"]
    text = get_llm("deep_think").invoke(
        SAFE_PROMPT.format(proposal=state["trader_proposal"])
    ).content
    r = {**r, "safe_history": r["safe_history"] + "\n[SAFE] " + text}
    return Command(goto="neutral_debator", update={"risk_debate": r})


def neutral_debator(state) -> Command:
    r = state["risk_debate"]
    text = get_llm("deep_think").invoke(
        NEUTRAL_PROMPT.format(proposal=state["trader_proposal"],
                              risky=r["risky_history"], safe=r["safe_history"])
    ).content
    rounds = r["rounds"] + 1
    r = {**r, "neutral_history": r["neutral_history"] + "\n[NEUTRAL] " + text,
         "rounds": rounds}
    goto = "risky_debator" if rounds < CONFIG.max_risk_rounds else "risk_manager"
    return Command(goto=goto, update={"risk_debate": r})


def risk_manager(state) -> Command:
    r = state["risk_debate"]
    decision = get_llm("deep_think").invoke(
        RISK_MANAGER_PROMPT.format(
            ticker=state["ticker"], risky=r["risky_history"],
            safe=r["safe_history"], neutral=r["neutral_history"],
        )
    ).content
    r = {**r, "judge_decision": decision}
    return Command(goto="portfolio_manager", update={"risk_debate": r})
