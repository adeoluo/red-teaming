# Operations Guide - Red Teaming Engine

The operational contract of the red-teaming service.

## Safety note

Every restricted term is fictional and a successful attack only ever returns the marker
`VIOLATION`. The service never produces real harmful content. It is a tool for
**strengthening** guardrails, and should be run against systems you own.

## Running the service

```bash
uv run python -m red_teaming serve --host 0.0.0.0 --port 8000
```

A standard-library HTTP server with **zero runtime dependencies**.

## Endpoints

| Method | Path | Body | Success |
|---|---|---|---|
| GET | `/health` | none | `{"status": "ok", "goals": N}` |
| GET | `/ready` | none | readiness of the engine |
| GET | `/metrics` | none | per-route request, error, and latency metrics (Prometheus text) |
| GET | `/report` | none | attack success rate per strategy |
| POST | `/attack` | `{"goal", "seed"?, "hardened"?}` | evolved attack, success, response |

Errors return JSON `{"error": ...}` with a 4xx status. `goal` must name a bundled goal,
`seed` is bounded, and `hardened` is a boolean.

## Service level objectives

Measured by `benchmarks/stress.py` on a developer laptop:

| Objective | Target | Observed (single worker) |
|---|---|---|
| Attack latency p50 | < 2 ms | about 0.6 ms |
| Attack latency p99 | < 2 ms at concurrency 1 | about 0.8 ms |
| Throughput | > 1000 searches/second/core | about 1700 searches/second |

Illustrative targets for the reference implementation.

## Operational constraints

- **Attack search is the expensive path and is CPU bound.** It holds the global
  interpreter lock, so throughput is flat across threads and the p99 tail grows with
  concurrency (measured: about 0.8 ms at one worker to tens of milliseconds at eight).
  Scale with **processes**, not threads.
- **Search is seeded and deterministic**, so results are reproducible and cacheable by
  `(goal, seed, hardened)`.
- **Requests are bounded**: only named goals are accepted and the seed is capped, so a
  request cannot ask for unbounded work.
- **No persistence, no authentication.** Front the service with a gateway, and restrict
  access since this is an offensive-security tool.

## Failure modes and responses

| Symptom | Likely cause | Response |
|---|---|---|
| Rising p99 under load | Concurrency above one worker per core | Add replicas; cap concurrency |
| `succeeded: false` on every goal | `hardened` is set (the defense) | Expected; the hardened guard resists |
| `400` on attack | Unknown goal or bad seed | Inspect the `error` field |

## Capacity planning

Throughput is approximately linear in shared-nothing replicas. For `R` searches per
second, provision about `ceil(R / 1700)` single-core replicas plus tail headroom.
