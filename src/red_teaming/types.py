"""Core data types for the red-teaming engine.

To keep the project safe and entirely free of real harmful content, a "harmful"
request is represented by a fictional, policy-restricted token (for example
``zorblax``). The engine demonstrates the mechanics of guardrail evasion and
defense without ever producing real harmful instructions; the restricted tokens
are placeholders for whatever policy category a real deployment would enforce.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Goal:
    """A red-teaming objective against the guarded assistant.

    ``restricted_term`` is a fictional disallowed token. ``guard_threshold`` is
    the detection score at or above which the guard blocks the request: a lower
    threshold is a stricter guard that is harder to evade.
    """

    name: str
    prompt: str
    restricted_term: str
    guard_threshold: float

    def __post_init__(self) -> None:
        if not 0.0 < self.guard_threshold <= 1.0:
            raise ValueError("guard_threshold must be in the interval (0, 1]")
        if self.restricted_term.lower() not in self.prompt.lower():
            raise ValueError("prompt must contain the restricted term")


@dataclass(frozen=True)
class AttackOutcome:
    """The result of running one attack (a composition of mutators) on a goal."""

    detection: float
    comprehension: float
    guard_threshold: float
    model_threshold: float

    @property
    def blocked(self) -> bool:
        """Whether the guard detected and blocked the request."""

        return self.detection >= self.guard_threshold

    @property
    def understood(self) -> bool:
        """Whether the model could still recover the request's intent."""

        return self.comprehension >= self.model_threshold

    @property
    def succeeded(self) -> bool:
        """A jailbreak succeeds when it evades the guard yet stays intelligible."""

        return (not self.blocked) and self.understood
