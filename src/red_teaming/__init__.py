"""Red Teaming - an automated guardrail red-teaming engine built from scratch."""

from __future__ import annotations

from red_teaming.mutators import (
    MUTATOR_NAMES,
    REGISTRY,
    Mutator,
    apply_mutators,
    get_mutator,
)
from red_teaming.search import (
    Attack,
    EvolutionarySearch,
    SearchResult,
    best_single_mutator,
    direct_attack,
)
from red_teaming.target import MODEL_THRESHOLD, evaluate_attack, respond
from red_teaming.types import AttackOutcome, Goal

__version__ = "0.1.0"

__all__ = [
    "MODEL_THRESHOLD",
    "MUTATOR_NAMES",
    "REGISTRY",
    "Attack",
    "AttackOutcome",
    "EvolutionarySearch",
    "Goal",
    "Mutator",
    "SearchResult",
    "apply_mutators",
    "best_single_mutator",
    "direct_attack",
    "evaluate_attack",
    "get_mutator",
    "respond",
]
