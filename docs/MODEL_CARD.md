# System Card - Red Teaming Engine

## Overview

- **What it is:** an automated guardrail red-teaming engine - it evolves guardrail-evasion
  attacks, measures attack success rate, and demonstrates a hardened-guard defense.
- **What it is not:** a tool that produces harmful content. All restricted terms are fictional
  and success only yields a marker.
- **Version:** 0.1.0.

## Intended use

- **Primary use cases:** learning and demonstrating automated red teaming and guard hardening;
  a from-scratch reference for evasion search and defense evaluation.
- **Primary users:** safety and security engineers strengthening guardrails.

## Out-of-scope / prohibited use

- Not for attacking real systems or producing real disallowed content.
- Absolute numbers reflect the simulated target, not any deployed guard.

## Performance

See the README report: direct 0.000, single mutator 0.400, evolutionary 1.000, hardened guard
0.000. The meaningful quantities are the relative rates and the defense effect.

## Risks and limitations

- A simulation; it illustrates mechanics rather than attacking any real model.
- Small mutator library and goal suite.

## Safety mitigations

- Fictional restricted terms; no real harmful content is produced or stored.
- Deterministic, offline, reproducible.

## Environmental / cost footprint

Negligible; all in-memory with no model calls.
