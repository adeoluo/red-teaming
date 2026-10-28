"""A micro-benchmark for the evolutionary attack search.

Measures search time and attack success rate for the goal suite across a range
of population sizes, so the README can quote concrete numbers. Deterministic and
offline; run with:

    uv run python benchmarks/benchmark.py
"""

from __future__ import annotations

import time

from red_teaming.data import GOALS
from red_teaming.search import EvolutionarySearch


def main() -> None:
    print(f"Goals: {len(GOALS)}\n")
    print(f"{'population':>12}{'search (ms)':>14}{'attack success rate':>22}")
    print("-" * 48)

    for population in (4, 8, 16, 32):
        search = EvolutionarySearch(population_size=population, seed=0)
        start = time.perf_counter()
        successes = sum(1 for goal in GOALS if search.search(goal).succeeded)
        elapsed_ms = (time.perf_counter() - start) * 1000
        rate = successes / len(GOALS)
        print(f"{population:>12}{elapsed_ms:>14.1f}{rate:>22.3f}")


if __name__ == "__main__":
    main()
