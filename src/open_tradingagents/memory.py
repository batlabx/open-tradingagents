"""Reflection memory — the firm's "lessons learned".

The original TradingAgents keeps a financial-situation memory in a vector store
so the research manager can recall how similar setups played out. We implement a
dependency-light SQLite version (swap in ChromaDB for real embeddings). It is
NOT a tool the model calls — it is infrastructure the graph reads/writes around
the agents, so it lives here rather than under tools/.
"""
from __future__ import annotations

import sqlite3
from datetime import datetime

from .config import CONFIG


def _conn():
    conn = sqlite3.connect(CONFIG.memory_db, check_same_thread=False)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS reflections ("
        "  id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "  ticker TEXT, situation TEXT, lesson TEXT, created TEXT)"
    )
    return conn


def add_reflection(ticker: str, situation: str, lesson: str) -> None:
    """Store a lesson learned after an outcome is known."""
    with _conn() as conn:
        conn.execute(
            "INSERT INTO reflections (ticker, situation, lesson, created) "
            "VALUES (?,?,?,?)",
            (ticker, situation, lesson, datetime.utcnow().isoformat()),
        )


def recall(ticker: str, limit: int = 3) -> str:
    """Return recent lessons for this ticker (naive recency retrieval).

    A real system would embed ``situation`` and do vector similarity; the shape
    of the call is identical, so the upgrade is a drop-in.
    """
    with _conn() as conn:
        rows = conn.execute(
            "SELECT lesson FROM reflections WHERE ticker=? "
            "ORDER BY id DESC LIMIT ?",
            (ticker, limit),
        ).fetchall()
    if not rows:
        return "(no prior lessons for this ticker)"
    return "\n".join(f"- {r[0]}" for r in rows)
