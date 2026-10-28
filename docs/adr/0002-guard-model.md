# ADR-0002: A detection-and-comprehension model of the guard

- **Status:** Accepted
- **Date:** 2026-01-01

## Context

To make red-teaming search meaningful and reproducible, the target must respond to attacks in
a way that creates a non-trivial optimization landscape, without any real harmful content or
network dependency.

## Decision

Model the guard with a **detection score** that each mutator multiplies down, and the model
with a **comprehension score** that each mutator also multiplies down. An attack succeeds when
detection falls below the guard threshold while comprehension stays above the model threshold.
Obfuscation therefore trades evasion against intelligibility.

## Alternatives considered

- **A hosted model and real policy categories.** Realistic, but networked, nondeterministic,
  and would involve generating real disallowed content, which this project deliberately avoids.
- **A binary keyword guard.** Deterministic, but any single evasion defeats it, so there is
  nothing for a search to optimize.

## Consequences

- Composition and order of mutators matter, so evolutionary search genuinely helps.
- The hardened guard is modelled by strongly attenuating each mutator's evasion, giving a
  clean defense story.
- Absolute numbers reflect the model, not any deployed guard; relative rates are the point.
