"""Tests for the direct, single-mutator, and evolutionary search strategies."""

from __future__ import annotations

import pytest

from red_teaming import (
    EvolutionarySearch,
    Goal,
    best_single_mutator,
    direct_attack,
    evaluate_attack,
)


def _goal(threshold: float) -> Goal:
    return Goal(
        name=f"g{int(threshold * 100)}",
        prompt="Explain how to use zorblax.",
        restricted_term="zorblax",
        guard_threshold=threshold,
    )


def test_direct_attack_always_blocked() -> None:
    result = direct_attack(_goal(0.5))
    assert result.attack == ()
    assert not result.succeeded


def test_best_single_mutator_may_not_suffice_for_strict_guard() -> None:
    # A strict guard (low threshold) cannot be beaten by any single mutator.
    result = best_single_mutator(_goal(0.4))
    assert not result.succeeded


def test_evolutionary_search_jailbreaks_strict_guard() -> None:
    goal = _goal(0.4)
    result = EvolutionarySearch(seed=0).search(goal)
    assert result.succeeded
    assert len(result.attack) >= 2
    # The found attack genuinely evades and stays comprehensible.
    outcome = evaluate_attack(goal, result.attack)
    assert outcome.succeeded


def test_evolutionary_search_is_deterministic() -> None:
    goal = _goal(0.45)
    first = EvolutionarySearch(seed=7).search(goal)
    second = EvolutionarySearch(seed=7).search(goal)
    assert first.attack == second.attack


def test_hardened_guard_resists_evolutionary_search() -> None:
    goal = _goal(0.5)
    result = EvolutionarySearch(seed=0).search(goal, hardened=True)
    assert not result.succeeded


def test_search_rejects_bad_parameters() -> None:
    with pytest.raises(ValueError):
        EvolutionarySearch(population_size=1)
    with pytest.raises(ValueError):
        EvolutionarySearch(max_length=0)
