# Threat Model - Red Teaming Engine

## Assets

- Integrity of the attack-success-rate measurements and the defense evaluation.

## Trust boundaries

- **Goals, mutators, and attacks are untrusted text.** They are transformed and scored, never
  executed; there is no path from text to execution.

## Threats and mitigations

| Threat | Vector | Impact | Mitigation |
|---|---|---|---|
| Producing real harmful content | Realistic restricted terms | Misuse | Restricted terms are fictional; success yields only a marker |
| Irreproducible results | An unseeded search | Flaky measurements | Deterministic, seeded genetic algorithm |
| Overstated attack success | Evaluating only lax guards | Misleading rates | The suite spans lax to strict guards and reports per strategy |
| Supply-chain compromise | Malicious dependency | Code execution | Zero runtime dependencies; Dependabot and CodeQL in continuous integration |

## Residual risk

The target is a simulation, so results do not transfer verbatim to a deployed guard. The
project's value is the reproducible methodology: search for evasions, measure attack success
rate, and verify that a hardened guard defeats the discovered attacks.
