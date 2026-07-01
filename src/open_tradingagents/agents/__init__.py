"""Agent nodes for the trading firm.

Analyst nodes return plain state updates and are wired with static edges (they
always run in sequence). The debate nodes (bull/bear, risk) return ``Command``
objects so they can loop for N rounds before handing off to their judge.
"""
