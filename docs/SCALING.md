# Scaling and Design Tradeoffs - Red Teaming Engine

How the reference design grows, and the tradeoffs taken.

## Reference architecture (today)

A single process runs the evolutionary attack search over an in-memory goal suite and
serves results over a standard-library HTTP service. Shared-nothing and stateless.

## Scaling path

| Stage | Bottleneck | Change |
|---|---|---|
| One process | Search CPU, global interpreter lock | One replica per core |
| One host | Host CPU | Horizontal replicas behind a load balancer |
| Many goals | Sequential search over goals | Fan out goals across workers; combine reports |
| Repeated requests | Re-searching the same goal | Cache by `(goal, seed, hardened)` |
| Larger search space | Bigger mutator library | Parallelize fitness evaluation; prune early |

Because the search is seeded and deterministic, results cache cleanly and replicas share
nothing, so throughput is approximately linear in replica count.

## Substantial tradeoffs

- **Evolutionary search vs exhaustive search.** The genetic algorithm explores
  compositions efficiently and finds attacks no single mutator achieves, at the cost of
  not being provably optimal. Exhaustive search is optimal but exponential in composition
  length.
- **Simulated target vs a hosted model.** The deterministic simulated guard and model keep
  results reproducible, offline, and free of real harmful content; a hosted target would
  be realistic but networked, nondeterministic, and ethically fraught. The target sits
  behind a clear interface.
- **Seeded determinism vs exploration.** A fixed seed makes every finding reproducible and
  cacheable but explores one trajectory; running several seeds trades compute for coverage.
- **Threads vs processes.** The search is pure Python and GIL-bound, so processes, not
  threads, are the unit of scaling. The service is stateless to make that trivial.

## What would change under real load

Fan goals out across workers, cache by search key, run process-per-core replicas, and, to
test a real system, place a model-backed target behind the existing interface. The search
and the defense evaluation are unchanged.
