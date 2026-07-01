"""Research team — bull vs bear debate, then a manager rules.

The bull and bear take turns appending to a shared transcript. After
``max_debate_rounds`` complete exchanges the bear routes to the research
manager, who reads the whole debate (plus lessons from memory) and issues the
investment plan.
"""
from __future__ import annotations

from langgraph.types import Command

from ..config import CONFIG, get_llm
from ..memory import recall
from ..prompts import BEAR_PROMPT, BULL_PROMPT, RESEARCH_MANAGER_PROMPT
from ..skills import load_skill


def _reports(state) -> str:
    return "\n\n".join(f"## {k} analyst\n{v}" for k, v in state["reports"].items())


def bull_researcher(state) -> Command:
    d = state["invest_debate"]
    text = get_llm("deep_think").invoke(
        BULL_PROMPT.format(
            ticker=state["ticker"], skill=load_skill("bull_bear_debate"),
            reports=_reports(state), bear=d["bear_history"] or "(bear has not spoken)",
        )
    ).content
    d = {**d, "bull_history": d["bull_history"] + "\n[BULL] " + text}
    return Command(goto="bear_researcher", update={"invest_debate": d})


def bear_researcher(state) -> Command:
    d = state["invest_debate"]
    text = get_llm("deep_think").invoke(
        BEAR_PROMPT.format(
            ticker=state["ticker"], skill=load_skill("bull_bear_debate"),
            reports=_reports(state), bull=d["bull_history"] or "(bull has not spoken)",
        )
    ).content
    rounds = d["rounds"] + 1
    d = {**d, "bear_history": d["bear_history"] + "\n[BEAR] " + text, "rounds": rounds}
    # Loop for another round, or send the debate to the judge.
    goto = "bull_researcher" if rounds < CONFIG.max_debate_rounds else "research_manager"
    return Command(goto=goto, update={"invest_debate": d})


def research_manager(state) -> Command:
    d = state["invest_debate"]
    decision = get_llm("deep_think").invoke(
        RESEARCH_MANAGER_PROMPT.format(
            ticker=state["ticker"], bull=d["bull_history"], bear=d["bear_history"],
            memory=recall(state["ticker"]),
        )
    ).content
    d = {**d, "judge_decision": decision}
    return Command(goto="trader",
                   update={"invest_debate": d, "investment_plan": decision})
