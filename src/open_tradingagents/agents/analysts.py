"""Analyst team — four tool-using ReAct agents.

Each analyst is the same shape (LLM + prompt + tools); only the prompt and the
bound tools differ. That uniformity is the point: a "specialist" is just a
different tool loadout, not a different code path.
"""
from __future__ import annotations

from langgraph.prebuilt import create_react_agent

from ..config import get_llm
from ..prompts import ANALYST_PROMPTS


def make_analyst(name: str, tools):
    """Factory: return a graph node for the named analyst bound to `tools`."""
    agent = create_react_agent(
        get_llm("quick_think"),
        tools=tools,
        prompt="You are a rigorous financial analyst. Call the tools you are "
               "given, cite concrete numbers, and end with a one-line bias.",
    )

    def node(state):
        task = ANALYST_PROMPTS[name].format(
            ticker=state["ticker"], date=state["trade_date"]
        )
        result = agent.invoke({"messages": [("user", task)]})
        report = result["messages"][-1].content

        reports = dict(state.get("reports") or {})
        reports[name] = report
        return {"reports": reports}  # static edge routes to the next analyst

    return node
