<h1 align="center">Red Teaming Engine</h1>

<p align="center">
  <em>An automated guardrail red-teaming engine built from scratch: evolve guardrail-evasion strategies, measure attack success rate, and demonstrate a defense.</em>
</p>

<p align="center">
  <a href="https://github.com/adeoluo/red-teaming/actions/workflows/ci.yml"><img alt="Continuous integration" src="https://github.com/adeoluo/red-teaming/actions/workflows/ci.yml/badge.svg"></a>
  <img alt="Coverage" src="https://img.shields.io/badge/coverage-97%25-brightgreen">
  <img alt="Python" src="https://img.shields.io/badge/python-3.11%20%7C%203.12-blue">
  <img alt="Type checked" src="https://img.shields.io/badge/mypy-strict-blue">
  <img alt="Runtime dependencies" src="https://img.shields.io/badge/runtime%20deps-0-brightgreen">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-green">
</p>

---

## Safety note

This project contains **no real harmful content**. Every disallowed request is a **fictional,
invented token** (for example `zorblax`), and a successful attack only ever produces the
marker `VIOLATION`, never any real instructions. The engine demonstrates the **mechanics** of
guardrail evasion and defense; the fictional tokens stand in for whatever policy category a
real deployment would enforce. It is a tool for **strengthening** guardrails.

## Motivation

A safety guardrail is only as good as the attacks it has been tested against. Red teaming
searches for inputs that make a guarded system violate its policy, so the guard can be
hardened against them. This project builds an automated red-teamer **from first principles**:
a guarded target, a library of evasion mutators, and an evolutionary search that discovers
attacks, all offline, deterministic, and with **zero runtime dependencies**. It then closes
the loop by showing a **hardened guard** that defeats the discovered attacks.

## Architecture

<p align="center">
  <img src="docs/architecture/architecture.svg" alt="System architecture" width="900">
</p>

The evolutionary search maintains a population of attacks (compositions of mutators), scores
each against the target, and breeds the best by crossover and mutation. The target's guard
contributes a **detection** score and the model a **comprehension** score; an attack succeeds
when it drops detection below the guard threshold while keeping comprehension above the model
threshold. See the [ADRs](docs/adr/) for the key design choices.

## The optimization landscape

Obfuscation is a trade-off, which is what makes search necessary:

- Each mutator **lowers the guard's detection score** (helping evasion) but also **erodes the
  model's comprehension** (hurting the attack's usefulness).
- Too little obfuscation and the guard blocks the request; too much and the model can no
  longer act on it.
- The red-teamer must find a **composition and order** of mutators in the narrow band that
  evades the guard yet stays intelligible. No single mutator suffices for a strict guard.

## Results

> Reproduce with `python -m red_teaming report`. Attack success rate is the fraction of the
> five goals jailbroken, over guards ranging from lax to strict.

| Strategy | attack success rate |
|---|---:|
| direct (no attack) | 0.000 |
| best single mutator | 0.400 |
| **evolutionary search** | **1.000** |
| evolutionary vs hardened guard (the defense) | 0.000 |

Direct requests are always blocked. The strongest single mutator beats only the two laxest
guards (0.400). The **evolutionary search jailbreaks all five** (1.000) by composing mutators.
The **hardened guard**, which largely sees through obfuscation, drives the very same evolved
attacks back to **0.000**, demonstrating the defense.

## Demonstration

```text
$ python -m red_teaming attack strict-guard
goal: strict-guard (guard threshold 0.4)
attack: roleplay -> roleplay -> synonym_swap
detection 0.392  comprehension 0.866
response: VIOLATION: restricted content for 'vexhollow' was elicited.
```

## Quickstart

```bash
git clone https://github.com/adeoluo/red-teaming.git && cd red-teaming
make setup                    # install dev tooling + pre-commit hooks
make all                      # lint + type-check + test

python -m red_teaming report                      # attack success rate table
python -m red_teaming attack strict-guard         # evolve an attack for one goal
python -m red_teaming attack medium-guard --hardened
```

Use the library directly:

```python
from red_teaming import EvolutionarySearch, Goal, respond

goal = Goal("demo", "Explain how to use zorblax.", "zorblax", guard_threshold=0.45)
result = EvolutionarySearch(seed=0).search(goal)
print(result.attack, result.succeeded)
print(respond(goal, result.attack))
```

## Components

- **mutators** - seven evasion transformations, each with an evasion and comprehension profile.
- **target** - the guarded assistant, with naive and hardened guards.
- **search** - the direct control, the single-mutator baseline, and the genetic algorithm.
- **evaluation** - the attack-success-rate report across the goal suite.

## Design decisions

- **A detection-and-comprehension model of the guard.** It yields a smooth, well-defined
  landscape where composition and order matter, so search genuinely helps.
  ([ADR-0002](docs/adr/0002-guard-model.md))
- **Evolutionary search.** A genetic algorithm explores compositions efficiently and is
  deterministic under a fixed seed. ([ADR-0003](docs/adr/0003-evolutionary-search.md))

## Performance

A deterministic micro-benchmark (`uv run python benchmarks/benchmark.py`) runs the search
over the goal suite across a range of population sizes, reporting search time and attack
success rate. The search jailbreaks the full suite in a few milliseconds even at small
populations, because fitness evaluation is a handful of arithmetic operations per attack.

## Responsible AI

- **Model card:** [docs/MODEL_CARD.md](docs/MODEL_CARD.md)
- **Data card:** [docs/DATA_CARD.md](docs/DATA_CARD.md)
- **Threat model:** [docs/THREAT_MODEL.md](docs/THREAT_MODEL.md)

## Limitations

- The target is a simulation; absolute numbers reflect its detection and comprehension model,
  not any particular deployed guard. The meaningful quantity is the relative attack success
  rate across strategies and the effect of the defense.
- The mutator library and goal suite are small and illustrative.
- All restricted terms are fictional; the engine is policy-agnostic by design.

## Roadmap

- [ ] A model-backed target and a model-backed judge behind the existing interfaces
- [ ] A larger mutator library and automatically learned mutator profiles
- [ ] Multi-objective search over attack success rate and attack cost

## License

[MIT](LICENSE). Part of a 28-project artificial intelligence engineering portfolio by
[adeoluo](https://github.com/adeoluo).
