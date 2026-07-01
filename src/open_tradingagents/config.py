"""Configuration. Two model tiers (like the original's deep_think / quick_think),
both pointed at a local Ollama server by default. No API keys anywhere.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass
class LLMConfig:
    provider: str = os.getenv("LLM_PROVIDER", "ollama")
    base_url: str = os.getenv("LLM_BASE_URL", "http://localhost:11434")
    # "deep_think" does the heavy reasoning (debates, final calls);
    # "quick_think" handles cheaper summarisation / tool orchestration.
    deep_think_model: str = os.getenv("DEEP_THINK_MODEL", "qwen2.5:14b-instruct")
    quick_think_model: str = os.getenv("QUICK_THINK_MODEL", "llama3.1:8b-instruct")
    temperature: float = float(os.getenv("LLM_TEMPERATURE", "0.3"))


@dataclass
class AppConfig:
    llm: LLMConfig = field(default_factory=LLMConfig)
    max_debate_rounds: int = int(os.getenv("MAX_DEBATE_ROUNDS", "2"))
    max_risk_rounds: int = int(os.getenv("MAX_RISK_ROUNDS", "1"))
    lookback_days: int = int(os.getenv("LOOKBACK_DAYS", "180"))
    memory_db: str = os.getenv("MEMORY_DB", "trading_memory.sqlite")


CONFIG = AppConfig()


def get_llm(tier: str = "deep_think"):
    """Return a LangChain chat model. Only the Ollama path is implemented — that
    is the whole point of the rewrite — but the switch shows where a cloud
    provider would slot back in."""
    if CONFIG.llm.provider == "ollama":
        from langchain_ollama import ChatOllama

        model = (CONFIG.llm.deep_think_model if tier == "deep_think"
                 else CONFIG.llm.quick_think_model)
        return ChatOllama(model=model, base_url=CONFIG.llm.base_url,
                          temperature=CONFIG.llm.temperature)
    raise ValueError(f"Unsupported provider: {CONFIG.llm.provider}")
