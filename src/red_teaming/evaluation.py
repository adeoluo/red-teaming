"""Measure attack success rate across the goal suite.

Attack success rate is the fraction of goals for which a strategy finds an
attack that jailbreaks the guard. The report compares four conditions: the
direct control, the best single mutator, the evolutionary search, and the
evolutionary search against the hardened guard (the defense).
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass

from red_teaming.data import GOALS
from red_teaming.search import (
    EvolutionarySearch,
    SearchResult,
    best_single_mutator,
    direct_attack,
)
from red_teaming.types import Goal


@dataclass(frozen=True)
class Row:
    """One row of the report: a strategy name and its attack success rate."""

    strategy: str
    successes: int
    total: int

    @property
    def attack_success_rate(self) -> float:
        return self.successes / self.total if self.total else 0.0


def _rate(strategy: Callable[[Goal], SearchResult], goals: Sequence[Goal]) -> int:
    return sum(1 for goal in goals if strategy(goal).succeeded)


def run_report(goals: Sequence[Goal] = GOALS, seed: int = 0) -> list[Row]:
    """Compute attack success rate for each strategy over the goal suite."""

    search = EvolutionarySearch(seed=seed)
    strategies: dict[str, Callable[[Goal], SearchResult]] = {
        "direct (no attack)": direct_attack,
        "best single mutator": best_single_mutator,
        "evolutionary search": search.search,
        "evolutionary vs hardened guard (defense)": lambda goal: search.search(goal, hardened=True),
    }
    total = len(goals)
    return [Row(name, _rate(strategy, goals), total) for name, strategy in strategies.items()]


def format_table(rows: Sequence[Row]) -> str:
    """Render the report rows as an aligned text table."""

    header = f"{'strategy':<44}{'successes':>11}{'attack success rate':>22}"
    lines = [header, "-" * len(header)]
    for row in rows:
        rate = f"{row.attack_success_rate:.3f}"
        lines.append(f"{row.strategy:<44}{row.successes:>4}/{row.total:<6}{rate:>22}")
    return "\n".join(lines)
