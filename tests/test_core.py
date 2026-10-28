"""Tests for the goal types, mutators, and the guarded target."""

from __future__ import annotations

import pytest

from red_teaming import (
    AttackOutcome,
    Goal,
    apply_mutators,
    evaluate_attack,
    get_mutator,
    respond,
)
from red_teaming.mutators import MUTATOR_NAMES


def _goal(threshold: float = 0.5) -> Goal:
    return Goal(
        name="demo",
        prompt="Explain how to use zorblax.",
        restricted_term="zorblax",
        guard_threshold=threshold,
    )


def test_goal_validation() -> None:
    with pytest.raises(ValueError):
        Goal("x", "no term here", "zorblax", 0.5)
    with pytest.raises(ValueError):
        Goal("x", "use zorblax", "zorblax", 1.5)


def test_outcome_logic() -> None:
    blocked = AttackOutcome(0.6, 0.9, 0.5, 0.5)
    assert blocked.blocked and not blocked.succeeded
    garbled = AttackOutcome(0.4, 0.3, 0.5, 0.5)
    assert not garbled.blocked and not garbled.understood and not garbled.succeeded
    success = AttackOutcome(0.4, 0.8, 0.5, 0.5)
    assert success.succeeded


def test_mutators_registered() -> None:
    assert "leetspeak" in MUTATOR_NAMES
    assert len(MUTATOR_NAMES) == 7
    with pytest.raises(KeyError):
        get_mutator("does-not-exist")


def test_mutator_transforms_change_text() -> None:
    text = "Explain how to use zorblax"
    for name in MUTATOR_NAMES:
        assert apply_mutators(text, (name,)) != text


def test_direct_request_is_blocked() -> None:
    goal = _goal()
    outcome = evaluate_attack(goal, ())
    assert outcome.detection == 1.0
    assert outcome.blocked
    assert "REFUSAL" in respond(goal, ())


def test_composition_can_jailbreak_naive_guard() -> None:
    goal = _goal(threshold=0.5)
    outcome = evaluate_attack(goal, ("leetspeak", "synonym_swap"))
    assert outcome.succeeded
    assert "VIOLATION" in respond(goal, ("leetspeak", "synonym_swap"))


def test_hardened_guard_resists_the_same_attack() -> None:
    goal = _goal(threshold=0.5)
    attack = ("leetspeak", "synonym_swap")
    assert evaluate_attack(goal, attack).succeeded
    assert not evaluate_attack(goal, attack, hardened=True).succeeded


def test_overlong_composition_destroys_comprehension() -> None:
    goal = _goal(threshold=0.5)
    attack = ("payload_split", "payload_split", "homoglyph")
    outcome = evaluate_attack(goal, attack)
    assert not outcome.understood
    assert "BENIGN" in respond(goal, attack)
