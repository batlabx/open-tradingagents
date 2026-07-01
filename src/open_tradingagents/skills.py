"""Skills = editable Markdown playbooks the agents load at runtime.

Tool vs skill, applied to a trading firm:
  * "Fetch AAPL's price history"  -> a TOOL. API boundary, side effect, a
    verifiable typed result. Belongs behind MCP.
  * "How a bull should argue" or "how to format the final call" -> a SKILL.
    Pure reasoning guidance, no side effects, no correct return value. A
    portfolio manager (not an engineer) should be able to edit it.
"""
from __future__ import annotations

from pathlib import Path

SKILLS_DIR = Path(__file__).parent / "skills"


def load_skill(name: str) -> str:
    path = SKILLS_DIR / f"{name}.md"
    if not path.exists():
        raise FileNotFoundError(f"No such skill: {name} ({path})")
    return path.read_text(encoding="utf-8")
