# ADR-0003: Evolutionary search over mutator compositions

- **Status:** Accepted
- **Date:** 2026-01-01

## Context

The attack space is the set of ordered mutator compositions up to a bounded length, which
grows combinatorially. A strict guard cannot be beaten by any single mutator, so the search
must explore compositions.

## Decision

Use a deterministic, seeded genetic algorithm: a population of attacks, fitness that rewards
success and otherwise the reduction of the detection and comprehension deficits, truncation
selection, single-point crossover, and insert/delete/replace mutation.

## Alternatives considered

- **Exhaustive search.** Optimal but exponential in composition length.
- **Greedy hill climbing.** Cheaper, but prone to local optima when a useful composition
  requires several mutators that are individually unhelpful.

## Consequences

- The search jailbreaks guards that defeat every single mutator.
- A fixed seed makes runs reproducible, which the tests rely on.
- The genetic operators and bounds are simple and inspectable.
