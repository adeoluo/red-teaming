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
| Supply-chain compromise | Malicious dependency | Code execution | No third-party runtime packages; development tools pinned in `uv.lock`; CodeQL in continuous integration |

## Standards mapping

The technique the engine simulates and the repository's own risks are mapped to the OWASP Top
10 for LLM Applications 2026 and MITRE ATLAS v2026.10 (IDs and names checked against
`ATLAS.yaml` from the
[v2026.10 release of mitre-atlas/atlas-data](https://github.com/mitre-atlas/atlas-data/releases)).
The OWASP Top 10 for Agentic Applications 2026 is not mapped: the target is a single guarded
assistant with no tools or memory.

| What | OWASP LLM 2026 | MITRE ATLAS v2026.10 | Role of this project |
|---|---|---|---|
| Guardrail evasion with role-play and prefix-injection mutators | LLM01:2026 Prompt Injection | AML.T0054 LLM Jailbreak; AML.T0065 LLM Prompt Crafting | Simulates and measures attack success rate |
| Guardrail evasion with leetspeak, separator, homoglyph, payload-split and synonym mutators | LLM01:2026 Prompt Injection | AML.T0068 LLM Prompt Obfuscation | Simulates and measures attack success rate |
| Evolutionary search against the guard's score | LLM01:2026 Prompt Injection | AML.T0043.001 Craft Adversarial Data: Black-Box Optimization; AML.T0042 Verify Attack | Implements the search |
| The hardened guard | LLM01:2026 Prompt Injection | AML.M0020 Generative AI Guardrails | Implements and verifies against the discovered attacks |
| The engine as a whole | | AML.M0035 AI Red Team | Implements the practice offline |
| Malicious dependency | LLM04:2026 Supply Chain | AML.T0010.001 Supply Chain Compromise: Software | Mitigates with no runtime dependencies and CodeQL |

Producing real harmful content has no OWASP 2026 entry of its own; the fictional terms keep the
project clear of it. In NIST AI 600-1 (Generative AI Profile) terms the project addresses the
Information Security risk.

## Residual risk

The target is a simulation, so results do not transfer verbatim to a deployed guard. The
project's value is the reproducible methodology: search for evasions, measure attack success
rate, and verify that a hardened guard defeats the discovered attacks.
