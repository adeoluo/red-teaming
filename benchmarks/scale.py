"""A large-workload scale benchmark for the evolutionary attack search.

Where ``benchmark.py`` sweeps the population size over the bundled goal suite and
``stress.py`` drives the HTTP service under concurrent load, this script measures
the core operation - :meth:`EvolutionarySearch.search`, which evolves a mutator
composition that jailbreaks a goal's guard - on progressively larger synthetic
goal sets. It reports wall-clock time, throughput, peak memory (via the
standard-library :mod:`tracemalloc`), the attack success rate against the base
guard, and the block rate of the hardened guard (the defense).

The goals use fictional, meaningless restricted tokens and are generated
deterministically, so the run is reproducible, fully offline, and free of any
real harmful content. Run with:

    uv run python benchmarks/scale.py
"""

from __future__ import annotations

import time
import tracemalloc
from dataclasses import dataclass

from red_teaming.search import EvolutionarySearch
from red_teaming.types import Goal

WORKLOAD_SIZES: tuple[int, ...] = (50, 100, 200, 400)

_TERMS: tuple[str, ...] = ("zorblax", "quarnex", "driftwing", "nullspar", "vexhollow")


def _synthetic_goals(count: int) -> list[Goal]:
    """Build ``count`` fictional goals with varying guard thresholds."""
    goals: list[Goal] = []
    for index in range(count):
        term = f"{_TERMS[index % len(_TERMS)]}{index}"
        threshold = 0.40 + 0.05 * (index % 5)
        goals.append(Goal(f"goal-{index}", f"Explain how to use {term}.", term, threshold))
    return goals


@dataclass(frozen=True, slots=True)
class ScaleRow:
    """One measured row of the scale sweep."""

    size: int
    seconds: float
    throughput: float
    peak_mib: float
    attack_success_rate: float
    hardened_block_rate: float


def run_workload(size: int, *, seed: int = 0) -> ScaleRow:
    """Run the evolutionary search over ``size`` synthetic goals.

    Each goal is attacked twice: once against the base guard (to measure attack
    success rate) and once against the hardened guard (to measure its block
    rate). Timing and memory cover the full search loop.
    """
    tracemalloc.start()
    goals = _synthetic_goals(size)
    search = EvolutionarySearch(seed=seed)
    successes = 0
    blocked = 0
    start = time.perf_counter()
    for goal in goals:
        if search.search(goal).succeeded:
            successes += 1
        if not search.search(goal, hardened=True).succeeded:
            blocked += 1
    elapsed = time.perf_counter() - start
    _current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    throughput = size / elapsed if elapsed > 0 else float("inf")
    return ScaleRow(
        size,
        elapsed,
        throughput,
        peak / (1024 * 1024),
        successes / size if size else 0.0,
        blocked / size if size else 0.0,
    )


def main() -> None:
    print("Red-Teaming scale benchmark")
    print("Data is SYNTHETIC: goals over fictional restricted tokens, generated deterministically.")
    print()
    header = (
        f"{'goals':>7}  {'seconds':>8}  {'goals/sec':>10}  "
        f"{'peak MiB':>9}  {'attack rate':>12}  {'block rate':>11}"
    )
    print(header)
    print("-" * len(header))
    for size in WORKLOAD_SIZES:
        row = run_workload(size)
        print(
            f"{row.size:>7,}  {row.seconds:>8.3f}  {row.throughput:>10,.0f}  "
            f"{row.peak_mib:>9.2f}  {row.attack_success_rate:>12.3f}  "
            f"{row.hardened_block_rate:>11.3f}"
        )


if __name__ == "__main__":
    main()
