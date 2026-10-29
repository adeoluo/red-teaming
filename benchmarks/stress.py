"""A production-style stress benchmark for the red-teaming service.

Drives the full attack handler under sustained, concurrent load over the goal
suite and reports throughput with p50, p95, and p99 latency. Attack search is
the expensive path, so this measures the engine under realistic contention.
Deterministic and offline; run with:

    uv run python benchmarks/stress.py
"""

from __future__ import annotations

import statistics
import time
from concurrent.futures import ThreadPoolExecutor

from red_teaming.data import GOALS
from red_teaming.service import RedTeamService, handle


def _percentile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, int(fraction * len(ordered)))]


def main() -> None:
    service = RedTeamService()
    names = [goal.name for goal in GOALS]
    requests = [{"goal": names[index % len(names)]} for index in range(1000)]

    def one(body: dict[str, str]) -> float:
        start = time.perf_counter()
        handle("POST", "/attack", body, service)
        return (time.perf_counter() - start) * 1000

    print(f"Goals: {len(GOALS)} | Requests: {len(requests)}")
    for workers in (1, 4, 8):
        start = time.perf_counter()
        with ThreadPoolExecutor(max_workers=workers) as pool:
            latencies = list(pool.map(one, requests))
        wall = time.perf_counter() - start
        print(
            f"workers={workers:<2}  "
            f"throughput={len(requests) / wall:>7.0f} req/s  "
            f"p50={statistics.median(latencies):>6.2f} ms  "
            f"p95={_percentile(latencies, 0.95):>6.2f} ms  "
            f"p99={_percentile(latencies, 0.99):>6.2f} ms"
        )


if __name__ == "__main__":
    main()
