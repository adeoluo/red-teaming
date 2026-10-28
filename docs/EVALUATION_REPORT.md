# Evaluation Report - Red Teaming Engine

> Reproduce with `python -m red_teaming report`. Deterministic and offline.

## Setup

- **Goals:** five, over fictional restricted terms, with guard thresholds from 0.40 to 0.60.
- **Metric:** attack success rate, the fraction of goals jailbroken.
- **Strategies:** the direct control, the best single mutator, the evolutionary search, and
  the evolutionary search against the hardened guard.

## Results

| Strategy | attack success rate |
|---|---:|
| direct (no attack) | 0.000 |
| best single mutator | 0.400 |
| evolutionary search | 1.000 |
| evolutionary vs hardened guard (defense) | 0.000 |

## Interpretation

Direct requests are always blocked (0.000). The strongest single mutator beats only the two
laxest guards (0.400), because no single transform drops detection far enough for a strict
guard without destroying comprehension. The evolutionary search composes mutators and
jailbreaks all five goals (1.000). The hardened guard, which largely sees through obfuscation,
drives the very same evolved attacks back to 0.000. Together these show both the attack and
its defense, measured on held-out difficulty levels.

## Reproducibility

The search is seeded; every number regenerates exactly.
