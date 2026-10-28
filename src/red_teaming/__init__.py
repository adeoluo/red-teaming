"""Red Teaming - an automated guardrail red-teaming engine built from scratch."""

from __future__ import annotations

from red_teaming.mutators import (
    MUTATOR_NAMES,
    REGISTRY,
    Mutator,
    apply_mutators,
    get_mutator,
)
from red_teaming.target import MODEL_THRESHOLD, evaluate_attack, respond
from red_teaming.types import AttackOutcome, Goal

__version__ = "0.1.0"

__all__ = [
    "MODEL_THRESHOLD",
    "MUTATOR_NAMES",
    "REGISTRY",
    "AttackOutcome",
    "Goal",
    "Mutator",
    "apply_mutators",
    "evaluate_attack",
    "get_mutator",
    "respond",
]
